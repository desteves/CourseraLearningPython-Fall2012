http://www.codeskulptor.org/#user6-XeHHk0TzbM-3.py
http://www.codeskulptor.org/#user6-sxXQoAH1rfVZkUI.py
################################
# file: Blackjack.py
# author: DWE
# date: 30NOV2012
# brief: Mini-project #6 - Blackjack
# link: http://www.codeskulptor.org/#
# version 0.01 
# messy version -- sorry!!!
################################
import simplegui
import random

FRAME_WIDTH = 600
FRAME_HEIGHT = 600
CARD_SIZE = (73, 98) # load card sprite - 949x392 - source: jfitz.com
CARD_CENTER = (36.5, 49)
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)

card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# SUIT = {1:'Spade', 2:'Heart', 3:'Diamond', 4:'Clubs'}
#position based on card_images size and CARD_SIZE
#the key for the dictionary, SUIT_POS, is the same as the key for SUIT 
#the value for the dictionary, SUIT_POS, is the top left corner (y-value)
#x-value for the first card of each suit is 0
SUIT_POS = {1:CARD_SIZE[1], 2:CARD_SIZE[1]*2, 3:CARD_SIZE[1]*3, 4:0}
# card is an element in the list ALL_CARDS
# if card % 10 == 0 then value is 10
# else if card / 10 == 1, then is an Ace so value is either 1 OR 11
# else value is card % 10
# if card < 50 card suit  = SUIT[card/10]		
# else         card suit  = SUIT[(card/10)%4+1] 			
ALL_CARDS = [11,12,13,14,15,16,17,18,19,10,#spade   11 is Ace 	
           21,22,23,24,25,26,27,28,29,20,  #heart   21 is Ace
           31,32,33,34,35,36,37,38,39,30,  #diamond 31 is Ace
           41,42,43,44,45,46,47,48,49,40,  #clubs   41 is Ace
           80,120,160,   #spade   J,Q,K
           50,90,130,    #heart   J,Q,K
           60,100,140,   #diamond J,Q,K
           70,110,150,   #clubs   J,Q,K
          ]
DEALER = 0
PLAYER = 1
#DEALT_MAX = len(ALL_CARDS)
#PLAYER_VISIBLE_CARDS_MAX = 5
SPACER = 10
PLAYER_POS = (SPACER, FRAME_HEIGHT - CARD_SIZE[1] - SPACER)
DEALER_POS = (SPACER, SPACER)

card_order = []
dealt_count = 0
dealer_hand = []
dealer_aces = 0
dealer_bust = 0
dealer_hole = 1 # 1 (True) = Face Down, 0 (False) = Face Up
player_hand = []
player_bust = 0
player_aces = 0

end_game_msg = ""
user_act_msg = "New deal?"
winnings_msg = 0

def get_x_pos(card):  #rank position
    p = CARD_SIZE[0]
    if card % 10:
        p *= card % 10#1-9
    elif card < 41:
        p *= 10 #tens
    elif card < 81:
        p *= 11 #jokers
    elif card < 121:	
        p *= 12  #queens
    else:		 #kings
        p *= 13	
    p -= CARD_SIZE[0]
    return p
def get_y_pos(card): #y
    return SUIT_POS[card/10] if card < 50 else SUIT_POS[(card/10)%4+1]

def init():
    global card_order, dealt_count, dealer_hole
    global dealer_hand, dealer_aces, dealer_bust
    global player_hand, player_bust, player_aces
    global end_game_msg,user_act_msg,winnings_msg
    card_order = ALL_CARDS[:]
    random.shuffle(card_order)    
    # Hitting the "Deal" button in the middle of the 
    # hand causes the player to lose the current hand.
    if dealt_count and not " Wins!" in end_game_msg:
        winnings_msg -= 1       
    dealer_aces = 0
    dealer_bust = 0
    dealer_hole = 1
    player_bust = 0
    player_aces = 0
    end_game_msg = ""
    user_act_msg = "Hit or stand?"
    player_hand = [card_order.pop(), card_order.pop()]
    dealer_hand = [card_order.pop(), card_order.pop()]
    dealt_count = 4
    
def hand_val(p): # (int player)
    hand = player_hand if p == PLAYER else dealer_hand
    aces = player_aces if p == PLAYER else dealer_aces
    val = 0
    for card in hand:    
        val += 10 if card % 10 == 0 else card % 10
    if aces and val + 10 <= 21: val += 10
    return val
  
def is_busted(val):
    return 1 if val > 21 else 0
def deal():
    deal_card(PLAYER)
# computes hand values and declares a winner.
def deal_card(p):
    global dealt_count, player_hand, dealer_hand, dealer_bust, player_bust
    global end_game_msg, user_act_msg, winnings_msg, dealer_hole
    if not dealt_count:
        end_game_msg = "GAME NOT STARTED"
        return
    if p == PLAYER:	
        if "Wins!" in end_game_msg:
            user_act_msg = "GAME OVER, New deal?"
            return
        if not is_busted(hand_val(PLAYER)):
            player_hand.append(card_order.pop())
        else:    # recognizes the player busting
            end_game_msg = "Player Bust!, Dealer Wins!"
            dealer_hole = 0	#show hole card
            winnings_msg -= 1
        player_bust = is_busted(hand_val(PLAYER))        
    else: 
        dealer_hand.append(card_order.pop())		
        dealer_bust = is_busted(hand_val(DEALER))
    dealt_count += 1
    
# If the dealer busts, the player wins.  
# Otherwise, the player and dealer then compare the values of their hands and  
# the hand with the higher value wins
# computes hand values and declares a winner.
def stand():
    global player_bust, dealer_hole, dealer_bust, dealer_hand
    global end_game_msg,user_act_msg, winnings_msg
    if " Wins!" in end_game_msg:
        user_act_msg = "GAME OVER, New deal?"
        return
    if not dealt_count:
        end_game_msg = "GAME NOT STARTED"
        return
    if not player_bust:
        dealer_hole = 0	#show hole card
        while hand_val(dealer_hand) < 16 and not dealer_bust:
            deal_card(DEALER)
        if dealer_bust: #recognizes the dealer busting
            end_game_msg = "Dealer Bust, Player Wins!"
            winnings_msg += 1
            return
        if hand_val(DEALER) >= hand_val(PLAYER):          
            end_game_msg = "Dealer Wins!"
            winnings_msg -= 1
        else: 
            end_game_msg = "Player Wins!"
            winnings_msg += 1
    else: # recognizes the player busting
        end_game_msg = "Player Bust!, Dealer Wins!"
        dealer_hole = 0	#show hole card
        winnings_msg -= 1
    user_act_msg = "New deal?"
# draw handler    
def draw(canvas):  
    offset = 1
    canvas.draw_text(str(end_game_msg), (SPACER , FRAME_HEIGHT/2 + 50), 18, "Black")
    canvas.draw_text(str(user_act_msg), (SPACER , FRAME_HEIGHT/2), 18, "White")
    canvas.draw_text("Score " + str(winnings_msg), 
                    (FRAME_WIDTH - 200, FRAME_HEIGHT/2), 18, "White")      
    canvas.draw_text("Player " + str(hand_val(PLAYER)), 
                    (FRAME_WIDTH - 200, FRAME_HEIGHT/2 + 50), 18, "White")    
    for card in player_hand:
        card_center = (CARD_CENTER[0] + int(get_x_pos(card)),
                       CARD_CENTER[1] + int(get_y_pos(card)))
        draw_center = (PLAYER_POS[0]  + CARD_CENTER[0] * offset,
                       PLAYER_POS[1]  + CARD_CENTER[1])
        offset += 1
        canvas.draw_image(card_images,card_center,CARD_SIZE,draw_center,CARD_SIZE)
    offset = 1
    for card in dealer_hand:
        card_center = (CARD_CENTER[0] + int(get_x_pos(card)),
                       CARD_CENTER[1] + int(get_y_pos(card)))
        draw_center = (DEALER_POS[0]  + CARD_CENTER[0] * offset,
                       DEALER_POS[1]  + CARD_CENTER[1])
        offset += 1
        #isolate the dealer's hole card
        if card == dealer_hand[0]: offset += 2
        canvas.draw_image(card_images,card_center,CARD_SIZE,draw_center,CARD_SIZE)
    #cover up the hole card
    if dealer_hole and dealt_count:
        draw_center = (DEALER_POS[0]  + CARD_CENTER[0],
                       DEALER_POS[1]  + CARD_CENTER[1])
        canvas.draw_image(card_back,CARD_BACK_CENTER,
                          CARD_BACK_SIZE,draw_center,
                          CARD_BACK_SIZE)
    else:  canvas.draw_text("Dealer " + str(hand_val(DEALER)), 
                    (FRAME_WIDTH - 200, FRAME_HEIGHT/2 - 50), 18, "White")   
        
frame = simplegui.create_frame("Blackjack", FRAME_WIDTH, FRAME_HEIGHT)
frame.set_canvas_background("Green")
frame.add_button("Deal", init, 200)
frame.add_button("Hit",  deal, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
frame.start()
