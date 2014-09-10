################
# Mini-proj_2.py
# author: DWE
# date: 22OCT2012
# author's OS: Linux Ubuntu 12.04
# author's browser: Chrome
# note: Program prints output to the canvas and terminal
# brief: User will have X attempts to guess a generated number with range [0, Y)
#		 Where X is 7 or 10 based on Y (100 or 1000 respectively)
# url: http://www.codeskulptor.org/#user3-bYtivjzUZxJcMU6.py
################
import simplegui
import random
import math

# initialize global variables used in your code
secret_number = 0
range_is_100 = 1
guess_count = 0

##  smallest integer n such that 2 ** n >= high - low + 1 where the secret number lies in [low, high).
##  To compute n, you should investigate using the functions math.log and math.ceil in the math module.  
guess_max_100  = math.ceil(math.log(101 , 2))  ## 7
guess_max_1000 = math.ceil(math.log(1001, 2))  ## 10
guess_max = guess_max_100
message = ''
# define event handlers for control panel
# button that changes range to range [0,100) and restarts
def print_msg():
    print message

# Handler to draw on canvas
def draw(canvas):
    y = 20;   
    for line in message.split('\n') :
      canvas.draw_text(line, (10, y), 12, "Fuchsia")                                 
      y += 20
     
def range100():
    # using global variable
    global range_is_100 
    range_is_100 = 1
    reset()
    
# button that changes range to range [0,1000) and restarts
def range1000():
    # using global variable
    global range_is_100 
    range_is_100 = 0
    reset()

def reset():
    # using global variables
    global secret_number
    global guess_count
    global guess_max
    global message
    # reset the counter
    guess_count = 0 
    # determine max number of tries
    guess_max = guess_max_100 if range_is_100 else guess_max_1000 
    # generate secret number
    secret_number = random.randrange(0, 100 if range_is_100 else 1000) 
    if 'New game started' in message:
        message = ''
    message += '\nNew game started with [0, '+  ('100' if range_is_100 else '1000') + ') range.'
    print_msg()
   
#default range is [0, 100)
range100() 

# main game logic goes here	   
# pre-cond: guess is [0-9]+
def input_guess(guess):
    int_guess = int(guess)
    global secret_number
    global guess_count
    global guess_max
    global message    
    guess_count += 1
    message = 'Attempt ' + str(guess_count) + ' out of ' + str(guess_max) + '.\n'   
    if secret_number == int_guess:
        message += 'Correct!\nThe secret number was ' + str(secret_number)
        reset() # keep same range as previous game
    elif guess_count == guess_max:
        message = 'Max tries reached.\nThe secret number was ' + str(secret_number) + '.\n'   
        reset() # keep same range as previous game
    elif secret_number > int_guess:        
        message += 'Higher than ' + guess
        print_msg()
    else: 
        message += 'Lower than ' + guess
        print_msg()
    
# create frame
frame = simplegui.create_frame("Guess the number", 350, 200)
# register event handlers for control elements
# Hitting either of these buttons should restart 
# the game and print out an appropriate message. 
# They should work at any time during the game
inp = frame.add_input("Enter Guess", input_guess, 100)
frame.add_button( "Range: 0 - 100 ", range100,  150)
frame.add_button( "Range: 0 - 1000", range1000, 150)
frame.set_draw_handler(draw)
# start frame
frame.start()
