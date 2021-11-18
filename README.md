#  Connect-4 AI

A Connect-4 game with an AI player. The AI uses alpha beta pruning with a max depth for finding it's best move.

## Introduction
I had always been interested in machine intelligence and learning and I made this small project after I started
learning about artificial intelligence. This AI uses a simple adversarial algorithm called **minimax** in which two players
try to minimize the other player's heuristic while maximizing their own. It is made efficient by using **alpha beta pruning**,
using which we decrease the number of nodes that are evaluated by the minimax algorithm in its search tree.

The winning condition is checked by checking a **convolution** of the board matrix and the smaller winning matrices that represent
4 pieces in a row, column or a diagonal. 

This is an initial version of the game runnable in the terminal. I intend on making a GUI using pygame to make it more interactive.

## Getting started
1. Check if python3 is installed. If not alredy installed, install python3 from https://www.python.org
```
python3 --version
```

2. Clone the repository in the directory of your choice

* For HTTPS:
```
git clone https://github.com/akshatayush/connect4-ai.git
```
* For SSH:
```
git clone git@github.com:akshatayush/connect4-ai.git
```

3. Go into the project directory and install the required packages
```
cd connect4-ai
pip3 install -r requirements.txt
```
4. Run the game
```
python3 game.py
```

## Screenshots
<p align='center'>
  <img src='/img/one.png' style='width: 35%;' />
  <br/>
  <img src='/img/two.png' style='width: 35%;' />
</p>
