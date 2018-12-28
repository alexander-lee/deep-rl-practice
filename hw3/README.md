# HW 3: Deep Q-Learning & Actor-Critic

### Dependencies
 * Python **3.5**
 * Numpy version **1.14.5**
 * TensorFlow version **1.10.5**
 * MuJoCo version **1.50** and mujoco-py **1.50.1.56**
 * OpenAI Gym version **0.10.5**
 * seaborn
 * Box2D==**2.3.2**
 * OpenCV
 * ffmpeg

## Deep Q-Learning
### Lunar Lander
![LunarLander](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/LunarLander.png?raw=true)
‎

### Pong
#### After ~4000000 Time Steps:
![PongGame](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/Pong.gif?raw=true)
![Pong](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/Pong_DQN.png?raw=true)
‎

### Double DQN vs. Normal DQN
![Double DQN vs. Normal DQN](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/LunarLander_Normal_vs_Double_DQN.png?raw=true)


## Actor Critic
### Comparing different Target Update Rates with Number of Gradient Steps
![Actor Critic Target Update Comparison](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/ActorCritic_TargetGradientUpdate_Comparison.png?raw=true)

* Each line is labeled `a_b` where `a` is the number of target updates, and `b` is the number of gradient steps per target update.
* From this graph, it seemed like `10_10` performed the best.
‎

### Inverted Pendulum (Actor Critic vs. Policy Gradient)
![InvertedPendulum](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/InvertedPendulum_AC_PG.png?raw=true)
‎

### Half Cheetah (Actor Critic vs. Policy Gradient)
![HalfCheetah](https://github.com/alexander-lee/deep-rl-practice/blob/master/hw3/graphs/HalfCheetah_AC_PG.png?raw=true)
