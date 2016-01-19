"""
 breakout.py
 Author: Leonel Machava <leonelmachava@gmail.com>
 Edited by James Richter
 Class: CS 499, Twitchell/Burton
 Last Updated: 1/6/2016

 A breakout clone.  I have made alterations so that 
 the ball speeds up over time, and so that a glancing hit
 will make the ball go at a different angle than a straight-on
 hit.  Also, the score decreases with each frame so that the
 program will time out if the paddle doesn't launch the ball.
"""
import sys
import pygame
import random

# the paddle is controlled by a "joystick."
# these threshold values represent the value of
# the input needed to press the button
# (i.e., to press left the value must be above
# LEFT_THRESHOLD.  To press right the value must be 
# below RIGHT_THRESHOLD.)
LEFT_THRESHOLD = 0.0000001
RIGHT_THRESHOLD = -0.0000001
SPACE_THRESHOLD = 0.0

# Game dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE   = SCREEN_WIDTH, SCREEN_HEIGHT

# Object dimensions
BRICK_WIDTH   = 64
BRICK_HEIGHT  = 15
PADDLE_WIDTH  = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS   = BALL_DIAMETER / 2

# speed constants
PADDLE_SPEED = 10
SPEED_MULTIPLIER = 1.025
MAX_BALL_SPEED = 200
MIN_BALL_SPEED = 30

# starting score
POINTS = 300

# boundaries
MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (000,200,0)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3

class Bricka:
    """A game of Breakout."""
    def __init__(self):
        """Initialize the pygame module."""
        pygame.init()
        self.inputs = [0,0,0]
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("bricka")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()
        self.state = STATE_GAME_OVER


    def init_game(self, startingScore = 0):
        """Initialize the game of Breakout."""
        self.lives = 1
        self.score = startingScore
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,
                                    BALL_DIAMETER,BALL_DIAMETER)

        self.ball_vel = [5,-5]

        self.create_bricks()


    def create_bricks(self):
        """Create the bricks in the Breakout game."""
        y_ofs = 35
        self.bricks = []
        self.brick_exists = []
        for i in range(7):
            x_ofs = 0
            for j in range(10):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,
                                               BRICK_WIDTH,BRICK_HEIGHT))
                self.brick_exists.append(1)
                x_ofs += BRICK_WIDTH
            y_ofs += BRICK_HEIGHT

    def draw_bricks(self):
        """Draw the bricks in the Breakout game."""
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    def check_input(self):
        """Check the input coming from the computer."""
        inputs = self.inputs
        if inputs[0] >= LEFT_THRESHOLD:
            self.paddle.left -= PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        elif inputs[0] <= RIGHT_THRESHOLD:
            self.paddle.left += PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if inputs[1] > SPACE_THRESHOLD \
            and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [5,-5]
            self.state = STATE_PLAYING
        elif self.state == STATE_WON:
            self.init_game(self.score)

    def move_ball(self):
        """Move the ball on the screen, according to its velocity."""
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        """
        Handle collisions between the ball and the paddle, bricks, and 
        walls.  The ball used to move at a constant speed regardless
        of where it bounced off the paddle, but I added some code to
        make a "glancing blow" give a different angle than a "direct hit."
        I also made it so that the ball speeds up over time.
        """
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += POINTS
                self.ball_vel[1] = -self.ball_vel[1]
                self.brick_exists[self.bricks.index(brick)] = 0
                self.bricks.remove(brick)
                
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON

        if self.ball.colliderect(self.paddle):
            if self.ball_vel[0]**2 + self.ball_vel[1]**2 > MAX_BALL_SPEED:
               self.ball_vel[0] *= 0.9
               self.ball_vel[1] *= 0.95
            if self.ball_vel[0]**2 < MIN_BALL_SPEED:
               self.ball_vel[0] *= 1.15
            if self.ball_vel[1]**2 < MIN_BALL_SPEED:
               self.ball_vel[1] *= 1.15
            self.ball.top = PADDLE_Y - BALL_DIAMETER

            ## self.ball.x - self.paddle.x goes from 59 to -12
            angle = self.ball.x - self.paddle.x
            direction = (self.ball_vel[1] > 0) + 0.5
            if angle <= 2:
               self.ball_vel[1] /= -1 * SPEED_MULTIPLIER
               self.ball_vel[0] *= SPEED_MULTIPLIER ** 2
            elif angle >= 45:
               self.ball_vel[1] /= -1 * SPEED_MULTIPLIER
               self.ball_vel[0] *= SPEED_MULTIPLIER ** 2
            elif angle >= 16 and angle <= 30:
               self.ball_vel[1] *= -1 * SPEED_MULTIPLIER ** 2
               self.ball_vel[0] /= SPEED_MULTIPLIER
            else:
               self.ball_vel[0] *= SPEED_MULTIPLIER
               self.ball_vel[1] = -self.ball_vel[1] * SPEED_MULTIPLIER
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        """Display the fitness score."""
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score),
                                            False, WHITE)
            self.screen.blit(font_surface, (255,5))

    def run(self):
        """
        Run the Breakout game.
        
        This is a special generator function that is used to return
        the positions of the ball and paddle while the game is playing.

        Yields:
           None: when the simulation is over
           self.score: when the game is over, it reports its fitness score
           a tuple containing the relative x distance from the ball to the
           paddle, the x velocity of the ball, and the y velocity of the 
           ball: every clock cycle, so that the neural network can perform
           the next immediate action.
        """
        self.done = False
        while not self.done:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = STATE_GAME_OVER
                    self.done = True
                    yield None
            self.clock.tick(50)
            self.score -= 1
            self.screen.fill(BLACK)
            self.check_input()

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_GAME_OVER:
                yield self.score
                self.init_game()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
            elif self.state == STATE_WON:
                yield None
            self.draw_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, 
                               (self.ball.left + BALL_RADIUS,
                                self.ball.top + BALL_RADIUS), 
                                BALL_RADIUS)

            self.show_stats()
            
            pygame.display.flip()
            
            if self.score <= -100:
               yield self.score
               self.init_game()
            bx, by = self.ball.center
            px, py = self.paddle.center
            yield ((bx - px)/float(SCREEN_WIDTH), \
                   self.ball_vel[0] / 100., \
                   self.ball_vel[1] / 100., \
                   )
if __name__ == "__main__":
    Bricka().run()
    pygame.quit()