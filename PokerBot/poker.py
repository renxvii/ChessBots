import pickle

card_values_w_ace = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K", " A"]
card_signs = ["H", "S", "D", "C"]

def card_to_num (c):
    for i in range(13, 0, -1):
        if c[0] == card_values_w_ace[i]:
            return i

def sort_cards (l1):
    cards = []
    for i in range(13, 0, -1):
        for card in l1:
            if card_values_w_ace[i] == card[0]:
                cards.append(card)
    return cards

def is_straight (l1):
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
        if len(cards) == 5:
            return cards
    return []


def is_flush (l1):
    count = [0,0,0,0]
    cards = []
    for i in range(4):
        for card in l1:
            if card[1] == card_signs[i]:
                count[i] += 1
    for i in range(4):
        if count[i] > 4:
            for card in sort_cards(l1):
                if card[1] == card_signs[i]:
                    cards.append(card)
                if len(cards) == 5:
                    return cards
    return []    

def is_straight_flush (l1):
    count = [0,0,0,0]
    cards = []
    for i in range(4):
        for card in l1:
            if card[1] == card_signs[i]:
                count[i] += 1
    for i in range(4):
        if count[i] > 4:
            for card in sort_cards(l1):
                if card[1] == card_signs[i]:
                    cards.append(card)
            return is_straight(cards)
    return []

def is_royal_flush (l1):
    c = sort_cards(is_straight(is_flush(l1)))
    if c != []:
        if c[0][0] == " A":
            return c
    return []
    

def is_foak (l1):
    cards = []
    for i in range(13, 0, -1):
        count = 0
        cards = []
        for card in l1:
            if card[0] == card_values_w_ace[i]:
                count += 1
                cards.append(card)
            if count == 4:
                for crd in l1:
                    if crd[0] != cards[0][0] and crd[0] == " A":
                        cards.append(crd)
                        return cards
                for j in range(12, -1, -1):
                    for crd in l1:
                        if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                            cards.append(crd)
                            return cards
    return []

def is_fh (l1):
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
    if cards == []:
        return []
    for j in range(13, 0, -1):
        cnt = 0
        tempc = []
        for crd in l1:
            if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                cnt += 1
                tempc.append(crd)
            if cnt == 2:
                return cards + tempc
    return []

def is_toak (l1):
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
    for j in range(13, 0, -1):
        for crd in l1:
            if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                cards.append(crd)
            if len(cards) == 5:
                return cards
    return []

def is_pair (l1):
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
            if count == 2:
                cards += tempc
                count = 0
                break
    if cards == []:
        return []
    for j in range(13, 0, -1):
        for crd in l1:
            if crd[0] != cards[0][0] and crd[0] == card_values_w_ace[j]:
                cards.append(crd)
            if len(cards) == 5:
                return cards
    return []             

def is_twopair (l1):
    cards = []
    a = is_pair(l1)
    if a == []:
        return []
    else:
        a = a[:2]
    b = []
    for c in l1:
        if c[0] != a[0][0]:
            b.append(c)
    b = is_pair(b)
    if len(a + b) >= 5:
        return a + b[:3]
    return []
        
        

def high (l1):
    cards = []
    for card in l1:
        cards.append(card)
        if len(cards) == 5:
            return cards

def find_hand (l1):
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

def get_hand_str (h1):
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

def compare (h1, h2, tb):
    hplay = find_hand(h1 + tb)
    hprog = find_hand(h2 + tb)
    if int(hplay[0][0]) > int(hprog[0][0]):
        print(get_hand_str(hplay))
        print(hplay[1:])
        print("Player wins hand")
    elif int(hplay[0][0]) < int(hprog[0][0]):
        print(get_hand_str(hprog))
        print(hprog[1:])
        print("Program wins hand")
    else:
        w = 0
        c = 1
        while w == 0:
            if c > 5:
                w = 3
            elif card_to_num(hplay[c]) > card_to_num(hprog[c]):
                w = 1
            elif card_to_num(hplay[c]) < card_to_num(hprog[c]):
                w = 2
            else:
                c += 1
        if w == 1:
            print(get_hand_str(hplay))
            print(hplay[1:])
            if c > 1:
                print("Player wins hand with a " + hplay[c][0] + " kicker")
            else:
                print("Player wins hand")
        elif w == 2:
            print(get_hand_str(hprog))
            print(hprog[1:])
            if c > 1:
                print("Program wins hand with a " + hprog[c][0] + " kicker")
            else:
                print("Program wins hand")
        else:
            print(get_hand_str(hplay))
            print(hplay[1:])
            print("Tie")


compare ([[" 2", "S"],[" J", "C"]], [[" 4", "H"],[" Q", "C"]], [[" 8", "D"],["10", "C"],[" 2", "H"],[" 7", "D"],[" A", "H"]])
        
def price (h2, tb):
    score = 0
    count = []
    suits = [0,0,0,0]
    hand = (h2 + tb)
    rnd = len(tb)
    for i in range(14):
        count.append(0)
    for i in range(14):
        for card in hand:
            if card[0] == card_values_w_ace[i]:
                count[i] += 1
    for i in range(1, 14):
        if count[i] == 1:
            score += (i * i) / 30 / rnd
        elif count[i] == 2:
            score += i / 2 / (rnd + 2)
        elif count[i] == 3:
            score += ((i / 2 + 10) ** 0.5) * 6 / rnd
        elif count[i] == 4:
            score += (i / 2 + 5) * 4 / rnd 
    for i in range(4):
        if card[1] == card_signs[i]:
            suits[i] += 1
    for i in range(4):
        if suits[i] == 4:
            score += 3 * (5 - rnd)
        elif suits[i] == 5:
            score += 3 * (6 - rnd)
def make_grid():
    grid = []       
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    for i in range(13):
        for j in range(13):
            for k in range(13):
                for l in range(13):
                    for m in range(13):
                        for n in range(13):
                            for o in range(13):
                                f.append(1.0)
                            e.append(f)
                        d.append(e)
                    c.append(d)
                b.append(c)
            a.append(b)
        grid.append(a)
    gridsigns = []
    b = []
    c = []
    d = []
    for i in range(7):
        for j in range(7):
            for k in range(7):
                for l in range(7):
                    d.append(1.0)
                c.append(d)
            b.append(c)
        gridsigns.append(b)
    outfile = open('pokergrid','wb')
    pickle.dump(grid,outfile)
    outfile.close

    outfile = open('pokersuits','wb')
    pickle.dump(gridsigns,outfile)
    outfile.close
    
            
make_grid()            

