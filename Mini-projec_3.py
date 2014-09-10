################################################
# Mini-proj_3.py
# author: DWE
# date: 08NOV2012
# author's OS: Linux Ubuntu 12.04
# author's browser: Chrome
# note: Program simulates a stopwatch
# brief: 
# url: http://www.codeskulptor.org/#user4-YNMogrJ9ahxnnoU.py
################################################
import simplegui
import time
# template for "Stopwatch: The Game"
# define global variables
t_inc = 1 ## tenths of a second
t_now = 0 
run = 0
X = 0 ## cound watch stops in a full second
Y = 0 ## count watch stops total
# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format_reflex():
    return str(X) + "/" + str(Y)
def format(t):
    int_time  = int((t/10) / 60)
    str_time  = str(int_time) ## if int_time > 9 else "0" + str(int_time)
    str_time += ":"
    int_time  = int((t/10) % 60)
    str_time += str(int_time) if int_time > 9 else "0" + str(int_time)
    str_time += "."
    str_time += str(t%10)
    return str_time
# print format(0)    
# print format(11)
# print format(321)
# print format(613)
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_click():
    global run
    run = 1
    timer.start()
def stop_click():
    global run
    global t_now
    global X
    global Y
    if run:  
        Y += t_inc
        if not (t_now % 10):
            X += t_inc
    run = 0
    timer.stop()
def reset_click():
    global t_now
    global run
    global X
    global Y
    t_now = 0
    run = 0
    X = 0
    Y =0
    timer.stop()
# Handler to draw on canvas
def draw(canvas):
    global t_now
    canvas.draw_text(format(t_now), (125, 125), 24, "Fuchsia") 
    canvas.draw_text(format_reflex(), (10, 15), 12, "Fuchsia")
# define event handler for timer with 0.1 sec interval
def timer_handler():
    # using global variable
    global t_inc
    global t_now
    global run
    t_now += t_inc
    print format(t_now)
# create frame
# register event handlers
# start timer and frame
# create frame
frame = simplegui.create_frame("STOPWATCH", 350, 200)
## timer for every 100 milliseconds (0.1 seconds)
timer = simplegui.create_timer(100, timer_handler) 
# register event handlers for control elements
frame.add_button( "START", start_click,  150)
frame.add_button( "STOP", stop_click, 150)
frame.add_button( "RESET", reset_click, 150)
frame.set_draw_handler(draw)
frame.start()

