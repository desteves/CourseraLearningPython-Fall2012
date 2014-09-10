################
# RPSLS.py
# author: Diana W Esteves
# date: 17OCT2012
# author's OS: Linux Ubuntu 12.04
# author's browser: Chrome
# http://www.codeskulptor.org/#user2-wNWXoPf73JK0MpQ.py
################
# Rock-paper-scissors-lizard-Spock template
# name one of "rock", "paper", "scissors", "lizard", or "Spock"
# each options wins agains the preceding two choices 
# each options loses against the following two choices
options = { 0 : "rock",
            1 : "Spock",
            2 : "paper",
            3 : "lizard",
            4 : "scissors", }
options_n = dict(zip(options.values(), options.keys()))
def number_to_name(number):
     return options[number]
def name_to_number(name):
    return options_n[name]
import random
def rpsls(name): 
    player_number = name_to_number(name)
    comp_number = random.randrange(0, 5)
    winner = (comp_number - player_number) % 5
    print "\nPlayer chooses " + name + "\nComputer chooses " + number_to_name(comp_number)
    if not winner:  
        print "Player and computer tie!"        
    elif winner < 3:
       print "Computer wins!"
    else:
        print "Player wins!"
    return

for o in options.values():
   rpsls(o)
   

