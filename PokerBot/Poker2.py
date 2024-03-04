print("Booting up...")

import random
from time import sleep
import pickle
from make_grid import make_grid
##try:
##    infile = open("pokergrid","rb")
##    infile.close
##    infile = open("pokersigns","rb")
##    infile.close
##except:
##    print("N")
##    make_grid()
card_values = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K"]
card_signs = ["H", "S", "D", "C"]
calls = 0
cards = []
log = []
bs = 0.1
last_update = 9
up = []
program_bluff = []
program_cards = []
program_funds = []
program_bet = []
program_in = []
dealer = []
for i in range(8):
    up.append(" ")
    dealer.append(" ")
    program_cards.append([])
    program_funds.append(0)
    program_bet.append(0)
    program_in.append(False)
    program_bluff.append(False)
pot = 0 # Establishes the amount of money available to win
for values in range (len(card_values)):
    for signs in range (len(card_signs)):
        h = [card_values[values], card_signs[signs]]
        cards.append(h) # Creates a list with the deck of cards
print("\n\n\n\n\n\n\n\n\n\n\nHere are your move options (to be used when prompted):\nFold - Ends round and gives pot to program \nCheck - Does not increase pot and moves to next round \nMatch - Puts the amount needed into the pot to play round \nRaise -  Increases the amount needed to be put into the pot to play round")
buy_in = max(int(input("What is your buy-in price?\n")),100) # Establishes how much money the player will play with
small_blind = buy_in / 100
num_bots = max(min(int(input("How many bots?\n")),7),1)
dealer[0] = "D"
for i in range(num_bots + 1):
    program_in[i] = True
    program_funds[i] = buy_in

card_values_w_ace = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K", " A"]

def card_to_num (c): # Assigns a numeric value to each card
    for i in range(13, 0, -1):
        if c[0] == card_values_w_ace[i]:
            return i

def sort_cards (l1): # Orders the cards in terms of their numeric value
    cards = []
    for i in range(13, 0, -1):
        for card in l1:
            if card_values_w_ace[i] == card[0]:
                cards.append(card)
    return cards

def is_straight (l1): # Checks for straight
    count = 0
    cards = []
    for i in range(13, -1, -1):
        found = []
        for card in l1:
            if card_values_w_ace[i] == card[0]:
                found = card
        if found != []:
            cards.append(found)
        else:
            cards = []
        if len(cards) == 5: # Makes sure straight is 5 cards
            return cards
    return []


def is_flush (l1):
    count = [0,0,0,0]
    cards = []
    for i in range(4): # Keeps count of how many cards of a specific suit there are
        for card in l1:
            if card[1] == card_signs[i]:
                count[i] += 1
    for i in range(4): # Checks for a flush
        if count[i] > 4:
            for card in sort_cards(l1):
                if card[1] == card_signs[i]:
                    cards.append(card)
                if len(cards) == 5:
                    return cards
    return []

def is_straight_flush (l1): # Combines function of straight and flush
    count = [0,0,0,0]
    cards = []
    for i in range(4): # Keeps count of card suits
        for card in l1:
            if card[1] == card_signs[i]:
                count[i] += 1
    for i in range(4):
        if count[i] > 4:
            for card in sort_cards(l1):
                if card[1] == card_signs[i]:
                    cards.append(card)
            return is_straight(cards) # If there is a flush, it moves on to check for a straight within the cards of the same suit
    return []

def is_royal_flush (l1):
    c = sort_cards(is_straight(is_flush(l1))) # Checks for highest flush, then straight, then sorts cards
    if c != []:
        if c[0][0] == " A":
            return c
    return []


def is_foak (l1): # Checks for 4 of a kind
    cards = []
    for i in range(13, 0, -1):
        count = 0
        tempc = []
        for card in l1:
            if cards != []:
                break
            if card[0] == card_values_w_ace[i]:
                count += 1
                tempc.append(card)
            if count == 4:
                cards += tempc
                count = 0
    if cards == []:
        return []
    for j in range(13, -1, -1):
        for crd in l1:
            if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                cards.append(crd)
                return cards
    return []

def is_toak (l1): # Checks for three of a kind
    cards = []
    for i in range(13, 0, -1):
        count = 0
        tempc = []
        for card in l1:
            if cards != []:
                break
            if card[0] == card_values_w_ace[i]:
                count += 1
                tempc.append(card)
            if count == 3:
                cards += tempc
                count = 0
                break
    if cards == []:
        return []
    for j in range(13, 0, -1): # Fills in the remaining two spots with the highest value cards
        for crd in l1:
            if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                cards.append(crd)
            if len(cards) == 5:
                return cards
    return []

def is_pair (l1): # Checks to see if the player/program has a pair
    cards = []
    for i in range(13, 0, -1):
        count = 0
        tempc = []
        for card in l1: # Checks for the highest pair
            if cards != []:
                break
            if card[0] == card_values_w_ace[i]:
                count += 1
                tempc.append(card)
            if count == 2:
                cards += tempc
                count = 0
                break
    if cards == []:
        return []
    for j in range(13, 0, -1): # Fills in the remaining spots with the three highest valued cards
        for crd in l1:
            if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                cards.append(crd)
            if len(cards) == 5:
                return cards
    return []

def is_twopair (l1): # Checks to see if there are two pairs
    cards = []
    a = is_pair(l1) # Finds the highest pair
    if a == []:
        return []
    else:
        a = a[:2]
    b = []
    for c in l1: # Finds the cards that are not in the pair
        if c[0] != a[0][0]:
            b.append(c)
    b = is_pair(b) # Looks for a second pair
    if len(a + b) >= 5:
        return a + b[:3] # Takes the two pairs with the next highest valued card
    return []

def is_fh (l1): # Checks for full house
    cards = []
    a = is_toak(l1)
    if a == []:
        return []
    else:
        a = a[:3]
    b = []
    for c in l1:
        if c[0] != a[0][0]:
            b.append(c)
    b.append(a[0])
    b = is_pair(b)
    if len(a + b) >= 5:
        return (a + b)[:5]
    return []

def high (l1): # Finds the 5 highest cards (from player/program's high with table)
    cards = []
    for card in l1:
        cards.append(card)
        if len(cards) == 5:
            return cards

def find_hand (l1): # Gives a numeric value to the type of hand the player has in order to determine which hand is higher
    cards = sort_cards(l1)
    temp = is_royal_flush(cards)
    if temp != []:
        return [["10",""]] + temp
    temp = is_straight_flush(cards)
    if temp != []:
        return [["9",""]] + temp
    temp = is_foak(cards)
    if temp != []:
        return [["8",""]] + temp
    temp = is_fh(cards)
    if temp != []:
        return [["7",""]] + temp
    temp = is_flush(cards)
    if temp != []:
        return [["6",""]] + temp
    temp = is_straight(cards)
    if temp != []:
        return [["5",""]] + temp
    temp = is_toak(cards)
    if temp != []:
        return [["4",""]] + temp
    temp = is_twopair(cards)
    if temp != []:
        return [["3",""]] + temp
    temp = is_pair(cards)
    if temp != []:
        return [["2",""]] + temp
    temp = [["1",""]]
    for i in high(cards):
        temp.append(i)
    return temp

def get_hand_str (h1): # Turns the numeric value of the hand into a string
    k = int(h1[0][0])
    if k == 1:
        return("High " + h1[1][0])
    if k == 2:
        return("Pair of " + h1[1][0] + "s")
    if k == 3:
        return("Two pairs of " + h1[1][0] + "s and " + h1[3][0] + "s")
    if k == 4:
        return("Three of a kind " + h1[1][0] + "s")
    if k == 5:
        return("Straight up to a high " + h1[1][0])
    if k == 6:
        return(h1[1][1] + " flush with a high " + h1[1][0])
    if k == 7:
        return("Full house with " + h1[1][0] + "s over " + h1[4][0] + "s")
    if k == 8:
        return("Four of a kind " + h1[1][0] + "s")
    if k == 9:
        return(h1[1][1] + " straight flush up to a high " + h1[1][0])
    if k == 10:
        return(h1[1][1] + " royal flush")    

def print_hidden(): # Prints the complete table without the program's cards being shown
    global program_funds
    global program_cards
    for i in range(7, num_bots, -1):
        program_cards[i] = [["  "," "],["  "," "]]
    l = len (table_cards)
    a = ""
    b = ""
    for i in range(l):
        a += "|" + table_cards[i][0] + " | "
        b += "| " + table_cards[i][1] + " | "
    for i in range(5 - l):
        a += "|\^/| "
        b += "|/_\| "
    strfunds = []
    for p in range(num_bots + 1):
        i = int(program_funds[p])
        c = ""
        d = ""
        e = str(i)
        if i == 0:
            e = "out"
        if len(e) % 2 == 0:
            c += " "
        for i in range(int((11 - len(e))/2)):
            c += " "
            d += " "
        k = str(int(pot))
        if len(k) % 2 == 0:
            k = " " + k
        for i in range(int((11 - len(str(int(pot))))/2)):
            k = " " + k + " "
        strfunds.append(c + e + d)
    for i in range(7, num_bots, -1):
        strfunds.append("           ")
    playing = [" "," "," "," "," "," "," "," "]
    for i in range(num_bots + 1):
        if not program_in[i]:
            playing[i] = "X"
    print(" ___ " + dealer[5] + " ___ " + up[5] + "           ___ " + dealer[4] + " ___ " + up[4] + "           ___ " + dealer[3] + " ___ " + up[3])
    print("|\^/| |\^/|           |\^/| |\^/|           |\^/| |\^/|")
    print("|/_\|" + playing[5] + "|/_\|           |/_\|" + playing[4] + "|/_\|           |/_\|" + playing[3] + "|/_\|")
    print("|___| |___|           |___| |___|           |___| |___|")
    print(strfunds[5] + "           " + strfunds[4] + "           " + strfunds[3])
    print(" ___ " + dealer[6] + " ___ " + up[6] + "  ___   ___   ___   ___   ___    ___ " + dealer[2] + " ___ " + up[2])
    print("|\^/| |\^/|  " + a + " |\^/| |\^/|")
    print("|/_\|" + playing[6] + "|/_\|  " + b + " |/_\|" + playing[2] + "|/_\|")
    print("|___| |___|  |___| |___| |___| |___| |___|  |___| |___|")
    print(strfunds[6] + "           " + k + "           " + strfunds[2])
    print(" ___ " + dealer[7] + " ___ " + up[7] + "           ___ " + dealer[0] + " ___ " + up[0] + "           ___ " + dealer[1] + " ___ " + up[1])
    print("|\^/| |\^/|           |" + program_cards[0][0][0] + " | |" + program_cards[0][1][0] + " |           |\^/| |\^/|")
    print("|/_\|" + playing[7] + "|/_\|           | " + program_cards[0][0][1] + " |" + playing[0] + "| " + program_cards[0][1][1] + " |           |/_\|" + playing[1] + "|/_\|")
    print("|___| |___|           |___| |___|           |___| |___|")
    print(strfunds[7] + "           " + strfunds[0] + "           " + strfunds[1])


def print_shown(): # Prints the complete table with the program's cards being shown
    global program_funds
    global program_cards
    for i in range(7, num_bots, -1):
        program_cards[i] = [["  "," "],["  "," "]]
    l = len (table_cards)
    a = ""
    b = ""
    for i in range(l):
        a += "|" + table_cards[i][0] + " | "
        b += "| " + table_cards[i][1] + " | "
    for i in range(5 - l):
        a += "|\^/| "
        b += "|/_\| "
    strfunds = []
    for p in range(num_bots + 1):
        i = int(program_funds[p])
        c = ""
        d = ""
        e = str(i)
        if i == 0:
            e = "out"
        if len(e) % 2 == 0:
            c += " "
        for i in range(int((11 - len(e))/2)):
            c += " "
            d += " "
        j = ""
        k = str(int(pot))
        if len(k) % 2 == 0:
            k = " " + k
        for i in range(int((11 - len(str(int(pot))))/2)):
            k = " " + k + " "
        strfunds.append(c + e + d)
    for i in range(7, num_bots, -1):
        strfunds.append("           ")
    playing = [" "," "," "," "," "," "," "," "]
    for i in range(num_bots + 1):
        if not program_in[i]:
            playing[i] = "X"
    print(" ___ " + dealer[5] + " ___ " + up[5] + "           ___ " + dealer[4] + " ___ " + up[4] + "           ___ " + dealer[3] + " ___ " + up[5])
    print("|" + program_cards[5][0][0] + " | |" + program_cards[5][1][0] + " |           |" + program_cards[4][0][0] + " | |" + program_cards[4][1][0] + " |           |" + program_cards[3][0][0] + " | |" + program_cards[3][1][0] + " |")
    print("| " + program_cards[5][0][1] + " |" + playing[5] + "| " + program_cards[5][1][1] + " |           | " + program_cards[4][0][1] + " |" + playing[4] + "| " + program_cards[4][1][1] + " |           | " + program_cards[3][0][1] + " |" + playing[3] + "| " + program_cards[3][1][1] + " |")
    print("|___| |___|           |___| |___|           |___| |___|")
    print(strfunds[5] + "           " + strfunds[4] + "           " + strfunds[3])
    print(" ___ " + dealer[6] + " ___ " + up[6] + "  ___   ___   ___   ___   ___    ___ " + dealer[2] + " ___ " + up[2])
    print("|" + program_cards[6][0][0] + " | |" + program_cards[6][1][0] + " |  " + a + " |" + program_cards[2][0][0] + " | |" + program_cards[2][1][0] + " |")
    print("| " + program_cards[6][0][1] + " |" + playing[6] + "| " + program_cards[6][1][1] + " |  " + b + " | " + program_cards[2][0][1] + " |" + playing[2] + "| " + program_cards[2][1][1] + " |")
    print("|___| |___|  |___| |___| |___| |___| |___|  |___| |___|")
    print(strfunds[6] + "           " + k + "           " + strfunds[2])
    print(" ___ " + dealer[7] + " ___ " + up[7] + "           ___ " + dealer[0] + " ___ " + up[0] + "           ___ " + dealer[1] + " ___ " + up[1])
    print("|" + program_cards[7][0][0] + " | |" + program_cards[7][1][0] + " |           |" + program_cards[0][0][0] + " | |" + program_cards[0][1][0] + " |           |" + program_cards[1][0][0] + " | |" + program_cards[1][1][0] + " |")
    print("| " + program_cards[7][0][1] + " |" + playing[7] + "| " + program_cards[7][1][1] + " |           | " + program_cards[0][0][1] + " |" + playing[0] + "| " + program_cards[0][1][1] + " |           | " + program_cards[1][0][1] + " |" + playing[1] + "| " + program_cards[1][1][1] + " |")
    print("|___| |___|           |___| |___|           |___| |___|")
    print(strfunds[7] + "           " + strfunds[0] + "           " + strfunds[1] + "\n\n\n")
    
def compare (h1, h2, tb): # Compares the hands of the player and program
    hp1 = find_hand(h1 + tb)
    hp2 = find_hand(h2 + tb)
    if int(hp1[0][0]) > int(hp2[0][0]): # Checks to see if one hand's value is greater than the other
        return 1
    elif int(hp1[0][0]) < int(hp2[0][0]):
        return 2
    else: # Compares each card individually if there are no hands of distinct greater value
        w = 0
        c = 1
        while w == 0:
            if c > 5: # Every card has the same value so it is a tie
                w = 3
            elif card_to_num(hp1[c]) > card_to_num(hp2[c]):
                w = 1
            elif card_to_num(hp1[c]) < card_to_num(hp2[c]):
                w = 2
            else:
                c += 1
        if w == 1:
            return 1
        elif w == 2:
            return 2
        else: # Used in the case of a tie
            return 3
        
wins = []
def winners (lst, tb):
    global program_cards
    global wins
    if len(wins) > 1:
        for i in wins:
            c = compare(wins[0],i,tb)
            if c == 2:
                wins.remove(i)
                wins[0] = i
            elif c == 1:
                wins.remove(i)
    if len(lst) == 1:
        if lst[0] not in wins:
            wins += lst
        return wins
    comp = compare(lst[0],lst[-1],tb)
    if comp == 1:
        if wins != []:
            if compare(wins[0],lst[1],tb) == 2:
                wins = []
        wins.append(lst[0])
        return winners(lst[:-1],tb)
    elif comp == 2:
        if wins != []:
            if compare(wins[0],lst[-1],tb) == 2:
                wins = []
        wins.append(lst[-1])
        return winners(lst[1:],tb)
    else:
        if wins != []:
            if compare(wins[0],lst[-1],tb) == 2:
                wins = [] 
        wins.append(lst[-1])
        wins.append(lst[0])
        return winners(lst[1:],tb)

def find_winners ():
    global wins
    global program_cards
    global table_cards
    global num_bots
    wins = []
    players = []
    for i in range(num_bots + 1):
        if program_in[i]:
            players.append(program_cards[i])
    return winners(players, table_cards)

def adjust(lst):
    global num_bots
    global program_in
    global program_funds
    global program_bet
    global program_cards
    global table_cards
    global pot
    for n in range(1, num_bots + 1):
        vals = []
        count = [0,0,0,0]
        for i in range(4):
            for card in (program_cards[n] + table_cards):
                if card[1] == card_signs[i]:
                    vals.append(card_to_num(card) - 1)
                    count[i] += 1
        infile = open("pokergrid","rb")
        grid = pickle.load(infile)
        prod = 0.95
        if program_cards[n] in lst:
            prod = 1.05
        grid[vals[0]][vals[1]][0] *= prod
        grid[vals[0]][vals[1]][vals[2] + 1][vals[3]][vals[4]][0] *= prod ** 4
        grid[vals[0]][vals[1]][vals[2] + 1][vals[3]][vals[4]][vals[5] + 1][0] *= prod ** 7
        grid[vals[0]][vals[1]][vals[2] + 1][vals[3]][vals[4]][vals[5] + 1][vals[6] + 1] *= prod ** 10
        infile.close
        infile = open("pokersuits","rb")
        grid = pickle.load(infile)
        grid[count[0]][count[1]][count[2]][count[3]] *= prod ** 6
        count = [0,0,0,0]
        for i in range(4):
            for card in (program_cards[n]):
                if card[1] == card_signs[i]:
                    count[i] += 1
        grid[count[0]][count[1]][count[2]][count[3]] *= prod ** 3
        for i in range(4):
            for card in (table_cards[:3]):
                if card[1] == card_signs[i]:
                    count[i] += 1
        grid[count[0]][count[1]][count[2]][count[3]] *= prod ** 4
        for i in range(4):
            if table_cards[3][1] == card_signs[i]:
                count[i] += 1
        grid[count[0]][count[1]][count[2]][count[3]] *= prod ** 5
        infile.close
        
def resolve ():
    global program_cards
    global program_funds
    global pot
    print("Winners:")
    lst = find_winners()
    ns = []
    for i in lst:
        ns.append(i)
    ls = []
    for i in range(num_bots + 1):
        if program_cards[i] in ns:
            ls.append(i)
    ls = sorted(ls)
    total = 0
    if 0 in ls:
        print("Player")
        total = 1
    for i in ls:
        if i != 0:
            print("Bot " + str(i))
            total += 1
    for i in ls:
        program_funds[i] += pot / total
    print(get_hand_str(find_hand(program_cards[ls[0]] + table_cards)))
    adjust(ns)
           
        
def turn(n):
    global last_update
    global num_bots
    global program_bluff
    global bs
    global calls
    global log
    global program_in
    global program_funds
    global program_bet
    global program_cards
    global table_cards
    global pot
    print(log[len(log) - 1])
    if n == 0:
        a = False
        while not a:
            print("\n\n\n\n\n\n\n\n\n\nPlayer's turn")
            print_hidden()
            print("Your current bet is $", "", int(program_bet[0]))
            print("The highest bet is $", "", int(max(program_bet)))
            print("The pot currently has $", "", int(pot))
            decision = input("What is your next move? (Fold, Check, or Raise)\n")
            if decision.upper() == "CHECK":
                log.append("Player calls")
                calls += 1
                a = True
                maxbet = max(program_bet)
                program_funds[0] -= maxbet - program_bet[0]
                pot += maxbet - program_bet[0]
                program_bet[0] = maxbet
            elif decision.upper() == "FOLD":
                log.append("Player folds")
                a = True
                program_in[0] = False
            elif decision.upper()[:6] == "RAISE ":
                a = True
                val = int(decision[6:]) + max(program_bet) - program_bet[0]
                if int(decision[6:]) < 0:
                    a = False
                else:
                    money = []
                    calls = 0
                    for i in range(num_bots + 1):
                        if program_in[i]:
                            money.append(program_funds[i] - program_bet[0])
                    if val > min(money):
                        last_update = n
                        maxbet = max(program_bet)
                        program_funds[0] -= min(money)
                        pot += min(money)
                        program_bet[0] += min(money)
                        log.append("Player raises " + str(int(program_bet[0] - maxbet)))
                    else:
                        last_update = n
                        maxbet = max(program_bet)
                        program_funds[0] -= val
                        pot += val 
                        program_bet[0] += val
                        log.append("Player raises " + str(int(program_bet[0] - maxbet)))
            elif decision.upper() == "LOG":
                print(log)
            else:
                print("error: that was not a valid move")
                print_hidden()
            
    else:
        print("\n\n\n\n\n\n\n\n\n\nBot " + str(n) + "'s turn")
        print_hidden()
        print("The highest bet is $", "", int(max(program_bet)))
        print("The pot currently has $", "", int(pot))
        probs = 1.0
        if program_bluff[n]:
            probs = 2.0
        elif random.random() < bs:
            probs *= 2
            program_bluff[n] = True
        vals = []
        count = [0,0,0,0]
        for i in range(4):
            for card in (program_cards[n] + table_cards):
                if card[1] == card_signs[i]:
                    vals.append(card_to_num(card) - 1)
                    count[i] += 1
        infile = open("pokergrid","rb")
        grid = pickle.load(infile)
        if len(vals) == 2:
            probs *= grid[vals[0]][vals[1]][0]
        elif len(vals) == 5:
            probs *= grid[vals[0]][vals[1]][vals[2] + 1][vals[3]][vals[4]][0]
        elif len(vals) == 6:
            probs *= grid[vals[0]][vals[1]][vals[2] + 1][vals[3]][vals[4]][vals[5] + 1][0]
        elif len(vals) == 7:
            probs *= grid[vals[0]][vals[1]][vals[2] + 1][vals[3]][vals[4]][vals[5] + 1][vals[6] + 1]
        infile.close
        infile = open("pokersuits","rb")
        grid = pickle.load(infile)
        probs *= grid[count[0]][count[1]][count[2]][count[3]]
        infile.close
        if probs < 0.5:
            if program_bet[n] < max(program_bet) and random.random() > bs: 
                program_in[n] = False
                log.append("Bot " + str(n) + " folds.")
            else:
                pot += max(program_bet) - program_bet[n]
                program_funds[n] -= max(program_bet) - program_bet[n]
                program_bet[n] = max(program_bet)
                log.append("Bot " + str(n) + " calls.")
                calls += 1
        elif probs <= 1.0:
            if random.random() > probs * program_funds[n] / (1 + 10 * (max(program_bet)**2 - program_bet[n]**2)**0.5) :
                program_in[n] = False
                log.append("Bot " + str(n) + " folds.")
            else:
                pot += max(program_bet) - program_bet[n]
                program_funds[n] -= max(program_bet) - program_bet[n]
                program_bet[n] = max(program_bet)
                log.append("Bot " + str(n) + " calls.")
                calls += 1
        else:
            chance = program_bet[n] / (program_funds[n] + program_bet[n])
            if random.random() > chance / probs:
                diff = probs - 1 - random.random()
                if int(diff * 5) * small_blind > max(program_bet) - program_bet[n]:
                    money = []
                    for i in range(num_bots + 1):
                        if program_in[i]:
                            money.append(program_funds[i] - program_bet[n])
                    last_update = n
                    if min(money) > int(diff * 5) * small_blind:
                        maxbet = max(program_bet)
                        pot += (int(diff * 5) * small_blind)
                        program_funds[n] -= (int(diff * 5) * small_blind)
                        program_bet[n] += int(diff * 5) * small_blind
                        log.append("Bot " + str(n) + " raises " + str(int(program_bet[n] - maxbet)))
                    else:
                        maxbet = max(program_bet)
                        pot += min(money)
                        program_funds[n] -= min(money)
                        program_bet[n] += min(money)
                        log.append("Bot " + str(n) + " raises " + str(int(program_bet[n] - maxbet)))
                    calls = 0
                else:
                    pot += max(program_bet) - program_bet[n]
                    program_funds[n] -= max(program_bet) - program_bet[n]
                    program_bet[n] = max(program_bet)
                    log.append("Bot " + str(n) + " calls.")
                    calls += 1
            else:
                pot += max(program_bet) - program_bet[n]
                program_funds[n] -= max(program_bet) - program_bet[n]
                program_bet[n] = max(program_bet)
                log.append("Bot " + str(n) + " calls.")
                calls += 1
            
            

def choice(v): # To be used everytime the game needs user input on their decision
    global num_bots
    global last_update
    global calls
    calls = 0
    current = v
    last_update = v % (num_bots + 1)
    agreed = False
    global program_funds
    global pot
    global program_bet
    global program_in
    global up
    while not agreed:
        up = [" "," "," "," "," "," "," "," "]
        p = 0
        for i in program_in:
            if i:
                p += 1
        up[current%(num_bots + 1)] = "P"
        if program_funds[current%(num_bots + 1)] == 0:
            if program_in[current%(num_bots + 1)]:
                a = ""  
        elif current == v:
            if program_in[current%(num_bots + 1)]:
                turn(current%(num_bots + 1))
        elif current % (num_bots + 1) == last_update:
            ag = True
            for i in range(num_bots + 1):
                if program_in[i]:
                    if program_bet[i] < max(program_bet):
                        ag = False
            if ag:
                agreed = True
            else:
                if program_in[current%(num_bots + 1)]:
                    turn(current%(num_bots + 1))
        elif not agreed:
            if program_in[current%(num_bots + 1)]:
                turn(current%(num_bots + 1))
        current = current + 1
    print("Bidding complete")
        
def blind(n):
    global num_bots
    global program_funds
    global program_bets
    global small_blind
    for i in range(num_bots + 1):
        program_bet[i] = 0
    pls = num_bots + 1
    program_funds[(n + 1) % pls] -= small_blind
    program_funds[(n + 2) % pls] -= 2 * small_blind
    program_bet[(n + 1) % pls] += small_blind
    program_bet[(n + 2) % pls] += 2 * small_blind


a = 0
lost = []
while len(lost) < num_bots:
    pot = 0
    log = ["Cards have been dealt, pre-flop bidding begins"]
    dealer[(a - 1) % (num_bots + 1)] = " "
    dealer[a % (num_bots + 1)] = "D"
    dealer[(a + 1) % (num_bots + 1)] = "S"
    dealer[(a + 2) % (num_bots + 1)] = "B"
    up[3 % (num_bots + 1)] = "P"
    for i in range(num_bots + 1):
        if program_funds[i] > 0:
            program_in[i] = True
        else:
            program_in[i] = False
    program_cards = [[],[],[],[],[],[],[],[]]
    table_cards = []
    blind(a % (num_bots + 1))
    pot += 3*small_blind
    random.shuffle(cards) # Shuffles the list of cards to simulate the shuffling of a dealer
    for i in range(2):
        for j in range(num_bots + 1):
            program_cards[(j + a + 1) % (num_bots + 1)] += [cards[i*(num_bots + 1) + j]]
    choice(a + 3)
    for i in range (4,7):
        table_cards += [cards[num_bots * 2 + i]]
    log.append("Flop dealt, post-flop bidding begins")
    sleep(3)
    program_bet = [0,0,0,0,0,0,0,0]
    choice(a + 1)
    table_cards += [cards[num_bots * 2 + 8]]
    log.append("Turn dealt, bidding begins")
    sleep(3)
    program_bet = [0,0,0,0,0,0,0,0]
    choice(a + 1)
    table_cards += [cards[num_bots * 2 + 10]]
    log.append("River dealt, final bidding begins")
    sleep(3)
    program_bet = [0,0,0,0,0,0,0,0]
    choice(a + 1)
    print_shown() # Prints the table with every card showing
    resolve()
    for i in range(num_bots + 1):
        if program_funds == 0:
            if i not in lost:
                lost.append(i)
    a += 1

          

