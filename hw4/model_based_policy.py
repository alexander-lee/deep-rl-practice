import tensorflow as tf
import numpy as np

import utils


class ModelBasedPolicy(object):

    def __init__(self,
                 env,
                 init_dataset,
                 horizon=15,
                 num_random_action_selection=4096,
                 nn_layers=1):
        self._cost_fn = env.cost_fn
        self._state_dim = env.observation_space.shape[0]
        self._action_dim = env.action_space.shape[0]
        self._action_space_low = env.action_space.low
        self._action_space_high = env.action_space.high
        self._init_dataset = init_dataset
        self._horizon = horizon
        self._num_random_action_selection = num_random_action_selection
        self._nn_layers = nn_layers
        self._learning_rate = 1e-3

        self._sess, self._state_ph, self._action_ph, self._next_state_ph,\
            self._next_state_pred, self._loss, self._optimizer, self._best_action = self._setup_graph()

    def _setup_placeholders(self):
        """
            Creates the placeholders used for training, prediction, and action selection

            returns:
                state_ph: current state
                action_ph: current_action
                next_state_ph: next state

            implementation details:
                (a) the placeholders should have 2 dimensions,
                    in which the 1st dimension is variable length (i.e., None)
        """
        # Added: Placeholders
        state_ph = tf.placeholder(shape=[None, self._state_dim], name="state", dtype=tf.float32)
        action_ph = tf.placeholder(shape=[None, self._action_dim], name="ac", dtype=tf.float32)
        next_state_ph = tf.placeholder(shape=[None, self._state_dim], name="next_state", dtype=tf.float32)

        return state_ph, action_ph, next_state_ph

    def _dynamics_func(self, state, action, reuse):
        """
            Takes as input a state and action, and predicts the next state

            returns:
                next_state_pred: predicted next state

            implementation details (in order):
                (a) Normalize both the state and action by using the statistics of self._init_dataset and
                    the utils.normalize function
                (b) Concatenate the normalized state and action
                (c) Pass the concatenated, normalized state-action tensor through a neural network with
                    self._nn_layers number of layers using the function utils.build_mlp. The resulting output
                    is the normalized predicted difference between the next state and the current state
                (d) Unnormalize the delta state prediction, and add it to the current state in order to produce
                    the predicted next state

        """
        # Added: Implementation of dynamics function
        dataset = self._init_dataset
        state = tf.dtypes.cast(state, dtype=tf.float32)
        action = tf.dtypes.cast(action, dtype=tf.float32)

        normalized_state = utils.normalize(state, dataset.state_mean, dataset.state_std)
        normalized_action = utils.normalize(action, dataset.action_mean, dataset.action_std)

        state_action = tf.concat([normalized_state, normalized_action], axis=1)
        normalized_pred_diff = utils.build_mlp(
            input_layer=tf.dtypes.cast(state_action, dtype=tf.float32),
            output_dim=self._state_dim,
            scope="state_ac_nn",
            n_layers=self._nn_layers,
            reuse=reuse
        )

        pred_diff = utils.unnormalize(normalized_pred_diff, dataset.delta_state_mean, dataset.delta_state_std)
        next_state_pred = state + pred_diff
        return next_state_pred

    def _setup_training(self, state_ph, next_state_ph, next_state_pred):
        """
            Takes as input the current state, next state, and predicted next state, and returns
            the loss and optimizer for training the dynamics model

            returns:
                loss: Scalar loss tensor
                optimizer: Operation used to perform gradient descent

            implementation details (in order):
                (a) Compute both the actual state difference and the predicted state difference
                (b) Normalize both of these state differences by using the statistics of self._init_dataset and
                    the utils.normalize function
                (c) The loss function is the mean-squared-error between the normalized state difference and
                    normalized predicted state difference
                (d) Create the optimizer by minimizing the loss using the Adam optimizer with self._learning_rate

        """
        # Added: Loss and Optimizer
        dataset = self._init_dataset
        state_diff = utils.normalize(next_state_ph - state_ph, dataset.state_mean, dataset.state_std)
        pred_state_diff = utils.normalize(next_state_pred - state_ph, dataset.state_mean, dataset.state_std)

        loss = tf.losses.mean_squared_error(tf.stop_gradient(state_diff), pred_state_diff)
        optimizer = tf.train.AdamOptimizer(self._learning_rate).minimize(loss)

        return loss, optimizer

    def _setup_action_selection(self, state_ph):
        """
            Computes the best action from the current state by using randomly sampled action sequences
            to predict future states, evaluating these predictions according to a cost function,
            selecting the action sequence with the lowest cost, and returning the first action in that sequence

            returns:
                best_action: the action that minimizes the cost function (tensor with shape [self._action_dim])

            implementation details (in order):
                (a) We will assume state_ph has a batch size of 1 whenever action selection is performed
                (b) Randomly sample uniformly self._num_random_action_selection number of action sequences,
                    each of length self._horizon
                (c) Starting from the input state, unroll each action sequence using your neural network
                    dynamics model
                (d) While unrolling the action sequences, keep track of the cost of each action sequence
                    using self._cost_fn
                (e) Find the action sequence with the lowest cost, and return the first action in that sequence

            Hints:
                (i) self._cost_fn takes three arguments: states, actions, and next states. These arguments are
                    2-dimensional tensors, where the 1st dimension is the batch size and the 2nd dimension is the
                    state or action size
                (ii) You should call self._dynamics_func and self._cost_fn a total of self._horizon times
                (iii) Use tf.random_uniform(...) to generate the random action sequences

        """
        # Added: Action Selection

        batch_size = self._num_random_action_selection
        first_actions = None  # Shape: (batch_size, action_dim)

        states = tf.tile(state_ph, [batch_size, 1])
        seq_costs = np.zeros((batch_size, ), dtype=np.float32)

        # Run this batch-wise for batch_size times
        for state_idx in range(self._horizon):
            random_actions = tf.random_uniform(
                shape=[batch_size, self._action_dim],
                minval=self._action_space_low,
                maxval=self._action_space_high
            )
            next_states = self._dynamics_func(
                state=states,
                action=random_actions,
                reuse=tf.AUTO_REUSE
            )

            seq_costs += self._cost_fn(states, random_actions, next_states)
            states = next_states

            # Update first_actions for the first set of actions generated
            if state_idx == 0:
                first_actions = random_actions

        best_action = first_actions[tf.argmin(seq_costs)]
        return best_action

    def _setup_graph(self):
        """
        Sets up the tensorflow computation graph for training, prediction, and action selection

        The variables returned will be set as class attributes (see __init__)
        """
        sess = tf.Session()

        # Added: Setup variables
        state_ph, action_ph, next_state_ph = self._setup_placeholders()
        next_state_pred = self._dynamics_func(state_ph, action_ph, reuse=tf.AUTO_REUSE)
        loss, optimizer = self._setup_training(state_ph, next_state_ph, next_state_pred)

        # Added: Call to _setup_action_selection
        best_action = self._setup_action_selection(state_ph)

        sess.run(tf.global_variables_initializer())

        return sess, state_ph, action_ph, next_state_ph, \
            next_state_pred, loss, optimizer, best_action

    def train_step(self, states, actions, next_states):
        """
        Performs one step of gradient descent

        returns:
            loss: the loss from performing gradient descent
        """
        # Added: Use session to perform single step of optimizer
        _, loss = self._sess.run([self._optimizer, self._loss], {
            self._state_ph: states,
            self._action_ph: actions,
            self._next_state_ph: next_states
        })

        return loss

    def predict(self, state, action):
        """
        Predicts the next state given the current state and action

        returns:
            next_state_pred: predicted next state

        implementation detils:
            (i) The state and action arguments are 1-dimensional vectors (NO batch dimension)
        """
        assert np.shape(state) == (self._state_dim,)
        assert np.shape(action) == (self._action_dim,)

        # Added: Use session to find prediction
        next_state_pred = self._sess.run(self._dynamics_func(
            tf.expand_dims(state, axis=0),
            tf.expand_dims(action, axis=0),
            reuse=tf.AUTO_REUSE
        ))
        next_state_pred = next_state_pred[0]  # Originally in a batch of size 1

        assert np.shape(next_state_pred) == (self._state_dim,)
        return next_state_pred

    def get_action(self, state):
        """
        Computes the action that minimizes the cost function given the current state

        returns:
            best_action: the best action
        """
        assert np.shape(state) == (self._state_dim,)

        # Added: Use session to run the self._best_action operation
        best_action = self._sess.run(self._best_action, {
            self._state_ph: [state]  # Not using expand_dims because placeholder input cannot be a tensor
        })

        assert np.shape(best_action) == (self._action_dim,)
        return best_action
