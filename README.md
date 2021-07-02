# PongAI
Credit for Basis of QLearning Framework to: https://github.com/python-engineer/snake-ai-pytorch  
(I changed Network Architecture and Fitted the logic to Pong. This was a great starting Point.)

Credit for Pong Basis to: https://github.com/clear-code-projects/Pong_in_Pygame  
(I rewrote the Code so its Object Oriented and added the Rule Based Opponent.) 

# How to run?
To play the Pong Game yourself, run "game_manual.py".
To se the learning Process run "agent.py".

# How do rewards work?
The Agent is rewarded for hitting the Ball and returning it to the Opponent. It gathers negative Rewards for hitting the Edges of the Screen and for letting the Enemy Score a Point. 

# How do the Iterations Work?
One Iteration spans five Points to be scored. After that the Game resets, Variables are cleared and a Graph ist plotted. The Graph is intended for User Reference and Performance Review. It shows the Amount of returned Balls per Iteration. Rewards are not shown and may therefore be negative in a seemingly great iteration (Because of the Screen Edges and the opponent scoring)
