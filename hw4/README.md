# HW 4: Model-Based Reinforcement Learning

### Dependencies
 * Python **3.5**
 * Numpy version **1.14.5**
 * TensorFlow version **1.10.5**
 * MuJoCo version **1.50** and mujoco-py **1.50.1.56**
 * OpenAI Gym version **0.10.5**
 * pandas
 * matplotlib

## Dynamics Model State Predictions vs. Actual
![State Predictions](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw4/graphs/HalfCheetah_StatePredictions.jpg?raw=true)

## Half Cheetah Model-Based RL
### Random Policy
| **Average Returns**  | **Std Returns** |
| :---:  | :---:  |
| -139.57 | 34.32 |

### Trained Policy
| **Average Returns**  | **Std Returns** |
| :---:  | :---:  |
| 56.68 | 29.22 |

![Half Cheetah Default](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw4/graphs/HalfCheetah_ModelBased?raw=true)

## Half Cheetah Hyperparameter Tuning
### Random Action Selection Size
* The number of random action sequences taken before taking the best action
![Half Cheetah Action Comparison](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw4/graphs/HalfCheetah_RandomActionComparison?raw=true)

### Model Predictive Control (MPC) Horizon Size
* The length of each action sequence (horizon) before taking the best action (similar to a lookahead)
![Half Cheetah Horizon Comparison](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw4/graphs/HalfCheetah_HorizonComparison?raw=true)


### Number of Hidden Layers
* The number of hidden layers in the dynamics prediction network
![Half Cheetah Hidden Layers](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw4/graphs/HalfCheetah_LayerComparison?raw=true)
