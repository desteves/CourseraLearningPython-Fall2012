################################
# Memory.py
# author: DWE
# date: 26OCT2012
# author's OS: Linux Ubuntu 12.04
# author's browser: Chrome
# implementation of card game - Memory
# url: http://www.codeskulptor.org/#user6-OeDYx2ieN8-0.py
################################
import simplegui
import random

IMG_1 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/1/1c/MJw1.png")
IMG_2 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/c/c3/MJw2.png")
IMG_3 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/9/9e/MJw3.png")
IMG_4 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/e/e8/MJw4.png")
IMG_5 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/e/ed/MJw5.png")
IMG_6 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/5/58/MJw6.png")
IMG_7 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/8/8b/MJw7.png")
IMG_8 = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/e/e1/MJw8.png")
WHS = (44,53) #width-height-source
WHD = (50,100) #width-heght-destination
CS = (22,26)
cards =   { 1 : IMG_1,2 : IMG_2,3 : IMG_3,4 : IMG_4,
            5 : IMG_5,6 : IMG_6,7 : IMG_7,0 : IMG_8 }
cards_ex = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0,
            10: 0,11: 0,12: 0,13: 0,14: 0,15: 0,0: 0 }
img_order = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
state = 0
last_up_a = -1
last_up_b = -1
turn_count = 0

def init():
    global state, img_order, cards_ex, last_up_a, last_up_b, turn_count
    state = 0
    last_up_a = -1
    last_up_b = -1
    turn_count = 0
    random.shuffle(img_order)
    for k in cards_ex.keys():
        cards_ex[k] = 0
    pass  

# define event handlers
# state 0, if you click on a card, that card is exposed,
# and you switch to state 1.  
# state 1, if you click on an unexposed card, that card is exposed 
# and you switch to state 2.  
# state 2, if you click on an unexposed card, 
# that card is exposed and you switch to state 1.  
def mouseclick(pos):
    global state, cards_ex, last_up_a, last_up_b, turn_count
    t = int(pos[0]/50)
    if not state:
        cards_ex[t] = 1
        last_up_a = t
        state = 1 #single exposed unpaired card
    elif state == 1:
        if not cards_ex[t]:
             cards_ex[t] = 1
             last_up_b = t
             state = 2 #end of a turn. 	
             turn_count += 1
        else:
            print "Card already exposed!"		
    else: #state == 2	 
         #check if last 2 up are a pair
         a = img_order[last_up_a]
         b = img_order[last_up_b]
         if a%8 != b%8 : #is not pair
            cards_ex[last_up_a] = 0
            cards_ex[last_up_b] = 0			 	
         if not cards_ex[t]:
             cards_ex[t] = 1
             last_up_a = t
             last_up_b = -1
             state = 1
         else:
            print "Card already exposed!"
  
# cards are logically 50x100 pixels in size    
def draw(canvas):
    center = (25,50) #half the size
    ex = 0		
    for t in img_order:
        if cards_ex[ex]:
            canvas.draw_image(cards[t%8],CS,WHS,center,WHD)
        else:
            canvas.draw_polygon(((center[0]-25,0),(center[0]+25,0),(center[0]+25,100),(center[0]-25,100)),1,"Black", "Red")        	
        center = [a+b for a,b in zip(center,(50,0))]
        ex += 1
    l.set_text("Moves = " + str(turn_count))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")
init()
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.start()

