import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np



#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    DOWN = 1
    UP = 2

Point = namedtuple('Point', 'x, y')
pygame.init()
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# rgb colors
black = (0,0,0)
white = (255,255,255)
bg_color = pygame.Color('white')

BLOCK_SIZE = 20
SPEED = 60

class PongGameAI:

    def __init__(self, w=1200, h=720):

        self.screen_width = w
        self.screen_height = h

        # init display
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption('Pong')
        pygame.mixer.pre_init(44100,-16,1, 1024)
        pygame.init()
        self.clock = pygame.time.Clock()

        #Game Rctangles
        self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 20, self.screen_height / 2 - 70, 10,140)
        self.opponent = pygame.Rect(10, self.screen_height / 2 - 70, 10,140)

        #gamevars
        self.ball_speed_x = 7 * random.choice((1,-1))
        self.ball_speed_y = 7 * random.choice((1,-1))
        self.player_speed = 0
        self.opponent_speed = 7
        self.ball_moving = False
        self.score_time = 0
        self.direction = Direction.UP
        self.frame_iteration = 0
        self.rebounds= 0

        #sound
        self.plob_sound = pygame.mixer.Sound("pong.ogg")
        self.score_sound = pygame.mixer.Sound("score.ogg")

        #scores
        self.player_score = 0
        self.opponent_score = 0
        self.reward = 0
        self.score = 0
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.UP



        self.player_score = 0
        self.opponent_score = 0
        self.frame_iteration = 0
        self.game_over = False

        self.rebounds = 0

        self.reward= 0





    def ball_start(self):
        global ball_speed_x, ball_speed_y, ball_moving, score_time

        self.ball.center = (self.screen_width/2, self.screen_height/2)
        current_time = pygame.time.get_ticks()


        if current_time - self.score_time < 700:
            number_three = basic_font.render("3",False,white)
            self.display.blit(number_three,(self.screen_width/2 - 10, self.screen_height/2 + 20))
        if 700 < current_time - self.score_time < 1400:
            number_two = basic_font.render("2",False,white)
            self.display.blit(number_two,(self.screen_width/2 - 10, self.screen_height/2 + 20))
        if 1400 < current_time - self.score_time < 2100:
            number_one = basic_font.render("1",False,white)
            self.display.blit(number_one,(self.screen_width/2 - 10, self.screen_height/2 + 20))

        if current_time - self.score_time < 2100:
            ball_speed_y, ball_speed_x = 0,0
        else:
            ball_speed_x = 1 * random.randint(0,50)
            #ball_speed_y = 1 * random.randint(-50,0)
            score_time = None

    def playerScore(self):
        pygame.mixer.Sound.play(self.score_sound)
        self.score_time = pygame.time.get_ticks()
        self.player_score += 1


    def opponentScore(self):
        pygame.mixer.Sound.play(self.score_sound)
        self.score_time = pygame.time.get_ticks()
        self.opponent_score += 1
        self.game_over = True
        self.reward = -30
        




    def ball_animation(self):
        global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            pygame.mixer.Sound.play(self.plob_sound)
            self.ball_speed_y *= -1

        # Player Score
        if self.ball.left <= 0:
            self.playerScore()
            self.ball_start()


        # Opponent Score
        if self.ball.right >= self.screen_width:
            self.opponentScore()
            self.ball_start()



        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            pygame.mixer.Sound.play(self.plob_sound)
            if abs(self.ball.right - self.player.left) < 10:
                self.ball_speed_x *= -1
            elif abs(self.ball.bottom - self.player.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            elif abs(self.ball.top - self.player.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1
            self.reward =  50
            self.rebounds += 1


        if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
            pygame.mixer.Sound.play(self.plob_sound)
            if abs(self.ball.left - self.opponent.right) < 10:
                self.ball_speed_x *= -1
            elif abs(self.ball.bottom - self.opponent.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            elif abs(self.ball.top - self.opponent.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

        return self.reward, self.score

    def player_animation(self):
        self.player.y += self.player_speed

        if self.player.top <= 0:
            self.player.top = 0
            self.reward = -1




        elif self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height
            self.reward = -1






    def opponent_ai(self):
        # if opponent.top < ball.y:
        # 	opponent.y += opponent_speed
        # if opponent.bottom > ball.y:
        # 	opponent.y -= opponent_speed

        self.opponent.y = self.ball.y
        # if opponent.top <= 0:
        # 	opponent.top = 0
        # if opponent.bottom >= screen_height:
        # 	opponent.bottom = screen_height

    def _update_ui(self):

        self.display.fill(black)

        pygame.draw.rect(self.display, white, self.player)
        pygame.draw.rect(self.display, white, self.opponent)
        pygame.draw.ellipse(self.display, white, self.ball)
        pygame.draw.aaline(self.display, white, (self.screen_width / 2, 0),(self.screen_width / 2, self.screen_height))

        player_text = basic_font.render(f'{self.player_score}',False,white)
        self.display.blit(player_text,(630,360))

        opponent_text = basic_font.render(f'{self.opponent_score}',False,white)
        self.display.blit(opponent_text,(570,360))

        pygame.display.flip()
        pygame.display.update()



    def play_step(self, action):
        self.frame_iteration += 1
        self.reward = 0
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.opponent_ai()
        self.player_animation()
        self.ball_animation()

        # 2. move
        self._move(action) # update the head


        # 3. check if game over

        game_over = False


        # 4. place new food or just move


        # 5. update ui and clock
        self._update_ui()

        if self.opponent_score == 5:
            game_over = True


        if self.player_score == 5:
            game_over = True


        self.clock.tick(SPEED)

        # 6. return game over and score
        return game_over, self.rebounds, self.reward


    def _move(self, action):
        # [straight, right, left]

        # clock_wise = [ Direction.DOWN, Direction.UP, None]
        # idx = clock_wise.index(self.direction)

        # if np.array_equal(action, [1, 0, 0]):
        #     new_dir = clock_wise[idx] # no change
        # elif np.array_equal(action, [0, 1, 0]):
        #     next_idx = (idx + 1) % 2
        #     new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        # elif np.array_equal(action, [0, 0, 1]): # [0, 0, 1]
        #     next_idx = (idx - 1) % 2
        #     new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        # self.direction = new_dir



        # if self.direction == Direction.DOWN:
        #     self.player_speed += 6
        # elif self.direction == Direction.UP:
        #    self.player_speed -= 6
        # else:
        #     self.player_speed = 0
        if action == [1,0,0]:
            self.player_speed = 6
        elif action == [0,1,0]:
           self.player_speed = -6 
        elif action == [0,0,1]:
           self.player_speed = 0 
        

if __name__ == '__main__':
    game = PongGameAI()

    # game loop
    while True:
        game_over, rebounds, reward = game.play_step()
