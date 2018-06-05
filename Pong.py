import pygame, sys
from pygame.locals import *
from random import randint

posOne = 0
posTwo = 0
gameOver = False
fps = pygame.time.Clock()

WIDTH = 810
HEIGHT = 610
PADDLE = 100
PADDLEWIDTH = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,128,0)

# Draws the window for the game.
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pong")

def drawBoard ():
    # Draw the board
    pygame.draw.rect(WINDOW, WHITE, (5, 5, 800, 600))

    # Draws the lines around the board and through the middle
    pygame.draw.line(WINDOW, BLACK, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 5)
    pygame.draw.line(WINDOW, BLACK, (0, 0), (0, HEIGHT), 8)
    pygame.draw.line(WINDOW, BLACK, (0, 0), (WIDTH, 0), 8)
    pygame.draw.line(WINDOW, BLACK, (WIDTH, 0), (WIDTH, HEIGHT), 11)
    pygame.draw.line(WINDOW, BLACK, (0, HEIGHT-3), (WIDTH, HEIGHT-3), 5)


class Paddle:
    velOne = 0
    velTwo = 0
    posOne = 0
    posTwo = 0
    def movePaddle1():
        # Left paddle, player 1 (RED)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Paddle.posOne += -5
                Paddle.velOne = (Paddle.velOne - 10)/2
                if Paddle.posOne < -405:
                    Paddle.posOne == -405
            if event.key == pygame.K_s:
                Paddle.posOne += 5
                Paddle.velOne = (Paddle.velOne + 10)/2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                Paddle.velOne = 0
            if event.key == pygame.K_s:
                Paddle.velOne = 0
        pygame.draw.rect(WINDOW, RED, (5, Paddle.posOne-PADDLE/2, 5 + PADDLEWIDTH, PADDLE))

    def movePaddle2():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Paddle.posTwo += -5
                Paddle.velTwo = (Paddle.velTwo - 10)/2
            if event.key == pygame.K_DOWN:
                Paddle.posTwo += 5
                Paddle.velTWO = (Paddle.velTwo + 10)/2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                Paddle.velTwo = 0
            if event.key == pygame.K_DOWN:
                Paddle.velTwo = 0

        pygame.draw.rect(WINDOW, BLUE,(WIDTH - 10 - PADDLEWIDTH, Paddle.posTwo-PADDLE/2, 5 + PADDLEWIDTH, PADDLE))

# Picks a value between 0 and 1 to decide who goes first.
def whoGoesFirst():
    x= randint(0, 1)== 0
    if x == 0:
        print("Player One goes first")
        print("Press 'SPACE' to launch the ball")
        return 1
    else:
        print("Player Two goes first")
        print("Press 'SPACE' to launch the ball")
        return -1

RAND = whoGoesFirst()

class Ball:
    posx = 0
    posy = 0
    vel = (0, 0)
    def drawCircle(posx, posy):
        pygame.draw.circle(WINDOW, GREEN, (posx, posy), 10, 0)

# Checks to see of the position of the ball is in the range of the paddle.
# If the ball does collide with the paddle then the x velocity of the ball is reversed and
# the velocity of the paddle is added to the y velocity of the ball.
def paddleCollision():
    upperL = int(Paddle.posOne - PADDLE/2)
    lowerL = int(Paddle.posOne + PADDLE/2)
    upperR = int(Paddle.posTwo -  PADDLE/2)
    lowerR = int(Paddle.posTwo + PADDLE/2)

    if Ball.posx >=2 and Ball.posx <10:
        if Ball.posy >= upperL and Ball.posy <= lowerL:
            if Ball.vel[0] < 0:
                Ball.vel = [-1 * Ball.vel[0], Ball.vel[1] + Paddle.velOne]
    elif Ball.posx >= 800 and Ball.posx <= 808 :
        if Ball.posy >= upperR and Ball.posy <= lowerR:
            if Ball.vel[0] > 0:

                Ball.vel = [-1*Ball.vel[0], Ball.vel[1]+Paddle.velTwo]

# Checks to see if the ball hits the top or bottom boundary. If it does then the y velocity
# gets reversed while the x velocity stays the same.
def boundaryCollision():
    if Ball.posy < 5:
        Ball.vel = [Ball.vel[0], -1*Ball.vel[1]]
    elif Ball.posy > HEIGHT-5:
        Ball.vel = [Ball.vel[0], -1*Ball.vel[1]]

# Checks to see if the ball has passed the side boundaries.
def getScore():
    if Ball.posx < 2:
        print("Player Two wins!")
        pygame.quit()
    elif Ball.posx > 808:
        print("Player One wins!")
        pygame.quit()

# Loop for launching the ball. The ball will follow the paddle until it is launched
# By pressing the space bar.
space_pressed = False
drawBoard()
Paddle.posOne = HEIGHT / 2
Paddle.posTwo = HEIGHT / 2
while not space_pressed:

    for event in pygame.event.get():
        if RAND == 1:
            Ball.posy = Paddle.posOne
            Ball.posx = 10+PADDLEWIDTH
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Ball.posy = Paddle.posOne
                    Ball.drawCircle(int(Ball.posx), int(Ball.posy + Paddle.velOne))
                    Ball.vel = [RAND * 50, Paddle.velOne]
                    space_pressed = True
        if RAND == -1:
            Ball.posy = Paddle.posTwo
            Ball.posx = WIDTH - 10 - PADDLEWIDTH
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Ball.posy = Paddle.posTwo
                    Ball.drawCircle(int(Ball.posx), int(Ball.posy + Paddle.velTwo))
                    Ball.vel = [RAND * 50, Paddle.velTwo]
                    space_pressed = True
    if Paddle.posOne > HEIGHT-PADDLE/2:
        Paddle.posOne = HEIGHT - PADDLE / 2
    if Paddle.posOne < 5 + PADDLE/2:
        Paddle.posOne = 5 + PADDLE / 2

    if Paddle.posTwo > HEIGHT - PADDLE/2:
        Paddle.posTwo = HEIGHT - PADDLE / 2
    if Paddle.posTwo < 5 + PADDLE/2:
        Paddle.posTwo = 5 + PADDLE / 2
    drawBoard()
    Ball.drawCircle(int(Ball.posx), int(Ball.posy))
    Paddle.movePaddle1()
    Paddle.movePaddle2()
    pygame.display.update()
    fps.tick(120)

# Main game loop.
while not gameOver:

    for event in pygame.event.get():
        if event.type == QUIT:
            gameOver = True

    drawBoard()
    if Paddle.posOne > HEIGHT-PADDLE/2:
        Paddle.posOne = HEIGHT - PADDLE / 2
    if Paddle.posOne < 5 + PADDLE/2:
        Paddle.posOne = 5 + PADDLE / 2

    if Paddle.posTwo > HEIGHT - PADDLE/2:
        Paddle.posTwo = HEIGHT - PADDLE / 2
    if Paddle.posTwo < 5 + PADDLE/2:
        Paddle.posTwo = 5 + PADDLE / 2

    Ball.posx += Ball.vel[0]*.1
    Ball.posy += Ball.vel[1]*.1
    paddleCollision()
    Ball.drawCircle(int(Ball.posx), int(Ball.posy))
    Paddle.movePaddle1()
    Paddle.movePaddle2()
    getScore()
    paddleCollision()
    boundaryCollision()
    pygame.display.update()
    fps.tick(120)