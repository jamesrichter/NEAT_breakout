"""
 bricka (a breakout clone)
 Developed by Leonel Machava <leonelmachava@gmail.com>
 Modifications by James Richter
 http://codeNtronix.com
"""
import sys
import pygame

# speed constants
SPEED_MULTIPLIER = 1.025
MAX_BALL_SPEED = 200
MIN_BALL_SPEED = 30

SCREEN_SIZE   = 640,480

POINTS = 300

# Object dimensions
BRICK_WIDTH   = 64
BRICK_HEIGHT  = 15
PADDLE_WIDTH  = 60
PADDLE_HEIGHT = 12
PADDLE_SPEED = 10
BALL_DIAMETER = 16
BALL_RADIUS   = BALL_DIAMETER / 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (200,0,200)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3

class Bricka:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("bricka (a breakout clone by codeNtronix.com)")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()


    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

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
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [5,-5]
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()

    def move_ball(self):
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
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))


    def run(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill(BLACK)
            self.check_input()

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")

            self.draw_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

            self.show_stats()

            pygame.display.flip()

if __name__ == "__main__":
    Bricka().run()