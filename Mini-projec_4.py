################################################
# Mini-proj_4.py
# author: DWE
# date: 14NOV2012
# author's OS: Linux Ubuntu 12.04
# author's browser: Chrome
# note: Pong Game
# brief: 
# url: http://www.codeskulptor.org/
################################################
# Implementation of classic arcade game Pong

import simplegui
import random
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD_LEFT_X  = HALF_PAD_WIDTH
PAD_RIGHT_X = WIDTH  - HALF_PAD_WIDTH
PAD_MAX_Y   = HEIGHT - PAD_HEIGHT
PAD_VEL = 5
BALL_START  = [WIDTH/2, HEIGHT/2] # center of the field
BALL_HOR  = [-1,  1]
BALL_VER  = [ 1, -1]

pad_vel_left = 0
pad_vel_right = 0
pad_left_y  = HEIGHT/2 - HALF_PAD_HEIGHT
pad_right_y = HEIGHT/2 - HALF_PAD_HEIGHT
ball_pos  = BALL_START
ball_vel  = [ 1,  1] #pixels per second, [X, Y]
score_left = 0
score_right = 0

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists    
    ball_pos = BALL_START
    rand_vel = [random.randrange(120, 240), random.randrange(60, 180)]
    ball_vel = [a*b for a,b in zip(rand_vel,BALL_HOR)] if not right else rand_vel
    pass
# define event handlers
def init():
    global pad_left_y, pad_right_y, pad_vel_left, pad_vel_right  # these are floats
    global score_left, score_right  # these are ints
    ball_init(random.randint(0, 1))
    pad_left_y  = HEIGHT/2 - HALF_PAD_HEIGHT
    pad_right_y = HEIGHT/2 - HALF_PAD_HEIGHT
    pad_vel_left = 0
    pad_vel_right = 0
    score_left = 0
    score_right = 0
    timer.start()
    pass
def draw(c):
    global score1, score2, ball_pos, ball_vel, pad_left_y, pad_right_y
    # update paddle's vertical position, keep paddle on the screen
    pad_right_y += pad_vel_right	
    pad_left_y += pad_vel_left
    if pad_right_y    < 0: pad_right_y = 0
    elif pad_left_y   < 0: pad_left_y  = 0
    if pad_right_y   > PAD_MAX_Y: pad_right_y = PAD_MAX_Y
    elif pad_left_y  > PAD_MAX_Y: pad_left_y  = PAD_MAX_Y	
    # draw mid line and gutters -- static
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # draw paddles, ball and scores  
    c.draw_line([PAD_LEFT_X, pad_left_y], [PAD_LEFT_X, pad_left_y + PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_line([PAD_RIGHT_X, pad_right_y], [PAD_RIGHT_X, pad_right_y + PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score_left ), (WIDTH/2 - 100 , 40), 38, "White")
 	c.draw_text(str(score_right), (WIDTH/2 + 100 , 40), 38, "White")
def keydown(key):
    global pad_left_y, pad_right_y, pad_vel_left, pad_vel_right
    if key == simplegui.KEY_MAP['down']:
        pad_vel_right += PAD_VEL
        #pad_right_y = pad_right_y + PAD_VEL
    elif key == simplegui.KEY_MAP['up']:
        pad_vel_right -= PAD_VEL
        #pad_right_y = pad_right_y - PAD_VEL	
    elif key == simplegui.KEY_MAP['w']:
        pad_vel_left -= PAD_VEL
        #pad_left_y = pad_left_y - PAD_VEL
    elif key == simplegui.KEY_MAP['s']:
        pad_vel_left += PAD_VEL
        #pad_left_y = pad_left_y + PAD_VEL
    pass
def keyup(key):	
    global pad_vel_left, pad_vel_right
    pad_vel_left = 0
    pad_vel_right = 0
   
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global score_left, score_right, ball_pos, ball_vel, pad_left_y, pad_right_y
    ##################### update ball ##########################################        
    # the ball touches/collides with the left and right gutters
    # increase the velocity of the ball by 10% each time it strikes a paddle
    # ball strikes the left or right gutter (but not a paddle), 
    # the opposite player receives a point
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS: # right gutter
        if  pad_right_y <= ball_pos[1] <= pad_right_y + PAD_HEIGHT:
            ball_vel = [1.1*a*b for a,b in zip(ball_vel,BALL_HOR)]   
        else:
            score_left += 1
            ball_init(False)
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS: # left gutter
        if  pad_left_y <= ball_pos[1] <= pad_left_y + PAD_HEIGHT:
            ball_vel = [1.1*a*b for a,b in zip(ball_vel,BALL_HOR)]  
        else:
            score_right += 1 
            ball_init(True)
    # the ball collides with and bounces off of the top and bottom walls   
    if ball_pos[1] > HEIGHT or ball_pos[1] <= 0:
        ball_vel = [a*b for a,b in zip(ball_vel,BALL_VER)]             
    ball_pos = [int(a/10)+b for a,b in zip(ball_vel,ball_pos)]
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
timer = simplegui.create_timer(100, timer_handler) 
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)
init()
frame.start()
