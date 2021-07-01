import torch
import random
import numpy as np
from collections import deque
from game import PongGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.0001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 2 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(3, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        cury = game.ball.y,
        curx = game.ball.x,

        ball_y = cury[0]
        ball_x = curx[0]

        # dir_u = game.direction == Direction.UP
        # dir_d = game.direction == Direction.DOWN

        playerstate = game.player.y

        







        state = [
            # Move direction
            ball_y,
            ball_x,

            # Ball location
            # dir_u,
            # dir_d
            playerstate

            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
        


    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        
        self.epsilon = 140 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:

            move = random.randint(0, 2)
            final_move[move] = 1
            print(final_move)
        else:

            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            print(final_move)

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = PongGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)
       


        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            

            if game.rebounds > record:
                record = game.rebounds
                agent.model.save()
                print("Model saved")

            print('Game', agent.n_games, 'Score', game.rebounds, 'Record:', record, 'Reward:', reward)

            plot_scores.append(game.rebounds)
            total_score += game.rebounds
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()