# File: Breakout.py

"""
This program (once you have finished it) implements the Breakout game.
"""

from pgl import GWindow, GOval, GRect, GLabel
import random

# Constants

GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
N_ROWS = 10                       # Number of brick rows
N_COLS = 10                       # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 2       # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3     # Ratio of brick to paddle width
BRICK_SEP = 2                     # Separation between bricks
TOP_FRACTION = 0.1                # Fraction of window above bricks
BOTTOM_FRACTION = 0.05            # Fraction of window below paddle
N_BALLS = 3                       # Number of balls in a game
TIME_STEP = 10                    # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0          # Starting y velocity downward
MIN_X_VELOCITY = 1.0              # Minimum random x velocity
MAX_X_VELOCITY = 3.0              # Maximum random x velocity
LABEL_WIN = "YOU WIN!"            # If you win the game
LABEL_LOSE = "YOU LOSE!"          # If you lose the game

# Derived constants

BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO

# Function: Breakout

def Breakout():
    """
    The main program for the Breakout game.
    """
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    def brick(): 
        for i in range(N_ROWS):
            for j in range(N_COLS):
                COLOR = ["red","orange", "green", "cyan", "blue"]
                xRect = j*(BRICK_WIDTH + BRICK_SEP)
                yRect = (GWINDOW_HEIGHT*TOP_FRACTION) + (i*(BRICK_HEIGHT+BRICK_SEP))
                rect = GRect(xRect, yRect, BRICK_WIDTH, BRICK_HEIGHT)
                rect.setColor (COLOR[(i // 2)])
                rect.setFilled(True)
                gw.add(rect)
                
    def paddle():
        nonlocal paddle
        paddle = GRect((GWINDOW_WIDTH/2) - (PADDLE_WIDTH/2), (GWINDOW_HEIGHT*(1-BOTTOM_FRACTION)) - PADDLE_HEIGHT ,PADDLE_WIDTH, PADDLE_HEIGHT)
        paddle.setFilled(True)
        gw.add(paddle)
        return paddle
        
    def mousemoveAction(e):
        xLoc = paddle.getX()
        paddle.move(e.getX() - xLoc - PADDLE_WIDTH/2 , 0)
    
    ball = None
    def makeBall():
        nonlocal ball
        ball = GOval((GWINDOW_WIDTH/2)-BALL_SIZE/2,GWINDOW_HEIGHT/2-BALL_SIZE/2, BALL_SIZE, BALL_SIZE)
        ball.setFilled(True)
        gw.add(ball)
    
    def step():
        nonlocal ball
        nonlocal vx
        nonlocal vy
        nonlocal lives
        nonlocal started
        nonlocal bricksLeft
        nonlocal timer
        collider = getCollidingObject()
        if collider != None:
            vy = -vy
            if collider != paddle:
                gw.remove(collider)
                bricksLeft -= 1
            if bricksLeft == 0:
                timer.stop()
                label = GLabel (LABEL_WIN)
                label.setFont ("bold 28px 'Helvetica Neue', 'Arial', 'Sans-Serif'")
                label.setColor ("Green")
                labelX = ((GWINDOW_WIDTH/3)-BALL_SIZE/2)
                labelY = (GWINDOW_HEIGHT/2-BALL_SIZE/2)
                gw.add(label, labelX, labelY)
                gw.remove(ball)
                
                
                
                
        if started:
            ball.move(vx,vy)
        if ball.getX() < 0 or ball.getX() > GWINDOW_WIDTH - BALL_SIZE:
            vx = -vx
        if ball.getY() < 0:
            vy = -vy
        if ball.getY() > GWINDOW_HEIGHT:
            if lives > 1:
                lives = lives - 1
                ball.setLocation((GWINDOW_WIDTH/2)-BALL_SIZE/2,GWINDOW_HEIGHT/2-BALL_SIZE/2)
                started = False
            else:
                label = GLabel (LABEL_LOSE)
                label.setFont ("bold 28px 'Helvetica Neue', 'Arial', 'Sans-Serif'")
                label.setColor ("Red")
                labelX = ((GWINDOW_WIDTH/3)-BALL_SIZE/2)
                labelY = ((GWINDOW_HEIGHT/2)-BALL_SIZE/2)
                gw.add(label, labelX, labelY)
            
    def getCollidingObject():
        nonlocal ball
        if gw.getElementAt(ball.getX(), ball.getY()) != None:
            return gw.getElementAt(ball.getX(), ball.getY())
        if gw.getElementAt(ball.getX()+ BALL_SIZE, ball.getY()) != None:
            return gw.getElementAt(ball.getX()+ BALL_SIZE, ball.getY())
        if gw.getElementAt(ball.getX(), ball.getY() + BALL_SIZE) != None:
            return gw.getElementAt(ball.getX(), ball.getY() + BALL_SIZE)
        if gw.getElementAt(ball.getX() + BALL_SIZE, ball.getY() + BALL_SIZE) != None:
            return gw.getElementAt(ball.getX() + BALL_SIZE, ball.getY() + BALL_SIZE)
        
    
    def clickAction(e):
        nonlocal started, ball
        started = True
        
    
    
    bricksLeft = N_ROWS*N_COLS 
    lives = N_BALLS
    gw.addEventListener("click", clickAction)    
    gw.addEventListener("mousemove", mousemoveAction)    
    paddle()  
    brick()
    makeBall()        
    started = False
    
    timer = gw.setInterval(step, TIME_STEP)
    vx = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
    if random.uniform(0, 1) < 0.5:
        vx = -vx
    else:
        vx = vx
    vy = INITIAL_Y_VELOCITY
    # You fill in the rest of this function along with any additional
    # helper and callback functions you need.
    

# Startup code

if __name__ == "__main__":
    Breakout()
