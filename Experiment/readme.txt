
We used the code from https://github.com/initial-h/AlphaZero_Gomoku_MPI

We modified the train.py, game_board.py and the network.py in the train model folder:

Train.py -- Used to train AlphaZero; borrowed from the Git repo above, slightly modified to use our hyper parameters and print more logging info. We set the init_model to use the pre-trained model for transfer learning.

game_board.py -- Used to record the previous moves, we changed the self.feature_planes to be 0,1,3 to set the number of previous moves used.

network.py -- we changed self.planes_num to be 1,3,7 to set the input dimision for the network. 


The instructions below are written by the original author:

## Installation Dependencies
* Python3
* tensorflow>=1.8.0
* tensorlayer=1.9.1
* mpi4py (parallel train and play)
* pygame (GUI)

## How to Install

> tensorflow/tensorlayer/pygame install : 
```
pip install tensorflow
pip install tensorlayer
pip install pygame
```

> mpi4py install [click here](https://www.jianshu.com/p/ba6f7c9415a0)
>
> mpi4py on windows [click here](https://blog.csdn.net/mengmengz07/article/details/70163140)

## How to Run
* Play with AI
```
python human_play.py
```
* Play with parallel AI (-np : set number of processings, take care of OOM !)
```
mpiexec -np 3 python -u human_play_mpi.py 
```
* Train from scratch
```
python train.py
```
* Train in parallel
```
mpiexec -np 43 python -u train_mpi.py
```