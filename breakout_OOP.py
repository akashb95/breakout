from pygame.locals import *
from components import *
import time
import sys
from vectors import Vector


class Game:
    DIFFICULTY = 1
    WIDTH = 500
    HEIGHT = 600
    ROW = 5
    COLUMN = 5
    SCORE = 0
    LIVES = 2

    def __init__(self, difficulty):
        if difficulty:
            self.DIFFICULTY = difficulty
        self.window = pg.display.set_mode([self.WIDTH, self.HEIGHT])
        pg.display.set_caption("Basic Breakout")
        pg.init()
        self.run()
        return

    def run(self):

        # Initial coordinates of paddle.
        p_init_coords = Vector(int(0.3 * self.window.get_width()), self.window.get_height() - 20)

        # Initialising ball.
        ball = Ball(self.window, 7,
                    Vector(self.window.get_width()/2, int(((49/50) * self.window.get_height()) - 37)),
                    Vector(0, 0))

        # Initialising paddle.
        paddle = Paddle(self.window, p_init_coords)

        # Initialising bricks.
        bricks = Bricks(self.window, RED, self.ROW, self.COLUMN)

        while self.LIVES - ball.restarts >= 0:
            for event in pg.event.get():
                # Exits if close button pressed.
                if event.type == QUIT:
                    pg.display.quit()
                    sys.exit(0)

                # Exits if escape key pressed.
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pg.display.quit()
                    sys.exit(0)

                # Give ball an initial velocity when space key is pressed.
                if not ball.moving:
                    ball.follow_mouse(paddle)
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        ball.start_move(self.DIFFICULTY)
                        ball.moving = True
                break

            if len(bricks.bricks) == 0:
                ball.velocity = Vector(0, 0)
                self.won()

            # Make screen blank.
            self.window.fill(BLACK)
            self.update_score()
            self.update_lives(ball.restarts)

            # Move objects on screen.
            if ball.moving:
                ball.move()
                ball.collision_paddle(paddle)

                # Accessing list of bricks in object 'bricks'.
                for brick in bricks.bricks:
                    # Check if collision has happened.
                    if ball.collision_bricks(brick):
                        # Removing brick ball collided with.
                        bricks.bricks.remove(brick)
                        # Updating score.
                        self.SCORE += 1

            paddle.move()

            # Draw objects on screen.
            ball.draw()
            bricks.draw()
            paddle.draw()

            # Update graphical contents of the window.
            pg.display.update()
            time.sleep(0.02)

        if self.LIVES - ball.restarts < 0:
            self.lost()

        return

    def lost(self):
        time.sleep(1)
        self.window.fill(BLACK)
        font = pg.font.SysFont('liberationserif', 100)
        gameover = font.render('You Lost. :/', True, BLUE, BLACK)
        self.window.blit(gameover, (70, 200))
        pg.display.update()
        time.sleep(5)
        pg.quit()

        # Window closes
        sys.exit()

    def won(self):
        font = pg.font.SysFont('liberationserif', 100)
        gameover = font.render('You Won!', True, GREEN, BLACK)
        self.window.blit(gameover, (100, 200))
        pg.display.update()
        time.sleep(5)
        pg.quit()

        # Window closes
        sys.exit()

    def update_score(self):
        font = pg.font.SysFont('liberationserif', 30)
        scoreboard = font.render("score: " + str(self.SCORE), True, BLUE)
        self.window.blit(scoreboard, (int(self.window.get_width()/2.25), self.window.get_height()/2))
        return

    def update_lives(self, num_restarts):
        font = pg.font.SysFont('liberationserif', 30)
        lifeboard = font.render("<3 : " + str(self.LIVES - num_restarts), True, RED)
        self.window.blit(lifeboard, (int(self.window.get_width() / 2.15), self.window.get_height() / 1.8))
        return
