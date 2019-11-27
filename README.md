# RoboCup Rescue Simulator(RCRS)-Gym Integration
 
(Linux) Instructions to download, build and run the RoboCup Rescue Simulator (RCRS) integrated with OpenAI Gym. OpenAI Gym is a toolkit for developing and comparing reinforcement learning algorithms.

## 1. Software Pre-Requisites

* Git
* Gradle 3.4+
* OpenJDK Java 8+
* Python 3.5+
* Openai Gym
* Stable Baselines
* Tensorboard 1.14 (Note: Stable baselines does not run with Tensorboard 2.0) 

## 2. Download project from GitHub

`$ git clone https://github.com/animeshgoyal9/RoboCup-Gym.git` 

## 3. Compile

Open a terminal window, navigate to the `rcrs-server-master` root directory and compile 

`$ ./gradlew clean`

`$ ./gradlew completeBuild`

Open another terminal window, navigate to the `rcrs-adf-sample-master` root directory and compile 

`$ ./clean`

`$ ./compile.sh`

Close the second terminal

## 4. Execute

In the first terminal, navigate to the boot folder in  `rcrs-server-master` directory and run the following python file 

`$ testing.py`

## 5. Visualization

To visualize the reward over time, losses etc, you can use tensorboard. 

Open a new terminal window and run the following bash command

`tensorboard --logdir ./ppo2_RoboCupGym_tensorboard/`










