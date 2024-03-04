from __future__ import print_function
import re, sys, time
from itertools import count
from collections import OrderedDict, namedtuple
import random
import copy


####
piece123 = { 'P': 180, 'N': 600, 'B': 650, 'R': 950, 'Q': 1850, 'K': 800}
setpieces = ['P', 'N', 'B', 'R', 'Q', 'K']
whitepostotal = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            100,  110,  115,  115, 115, 115,  110,  100,
             60,   65,   70,   75,  75,  70,   65,   60,
             5,  15,   20,  20,  30,   20,  15, 10,
             5,   0,  15,  15,  40,   15,   0,  5,
            15,    5,   5,  10,  10,   5,   5,  15,
            -5,   20,  15,  0, -10,  15, 20, -5,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -50, -25, -20,  10,  10, -20, -25, -50,
            0,  -5,  45,   10,  10,  45,  -5,   0,
            5,   0,   -5,  40,  40,  -5,   0,   5,
            10,  25,  15,  20,  10,  15,  30,  10,
            0,   5,   20,  15,  35,  20,   5,   0,
           -15,  10,  30,  15,  15,  30,  10, -15,
           -15, -10,  -5,  15,   15,  -5, -10, -15,
           -50, -10, -15, -10, -10, -15, -10, -50),
    'B': ( 10, -20, -30, -35, -35, -30, -20,  10,
           -10,  30,  35,  10,  10,  20,  30, -10,
             5,  5,   25,  25,  25,  20,  25,   5,
            10,  10,  30,  35,  35,  30,  30,  10,
            10,  20,  10,  25,  25,  30,  10,  10,
            15,  15,  30,  20,  20,  30,  20,  15,
            15,  30,  20,  15,  15,  20,  30,  15,
            20,   5,  -5, -10, -10,  -5,   5,   0),
    'R': (  45,  15,  30,  20, 20,  30,  10,  45,
            45,  40,  45,  45,  45,  45,  40,  45,
            20,  15,  20,  20,  20,  20,  15,  20,
             0,   5,  15,  15,  15,  15,   5,   0,
           -20,  15,  10,   15, 15,  10,  15,  10,
           -10,  10,  15,   15,  25,  15,   30,  10,
           -15, -20, -20, -25, -25, -20, -20, -15,
           -10,  -15,  -5,  30,  25, 30, -15, -10),
    'Q': (   15,   10,  20,  20, 20,  20,  10,  15,
            60,  40,  45,  15,  15,  45,  40,  60,
            20,  15,  20,  20,  20,  20,  15,  20,
             0,   5,  15,  15,  15,  15,   5,   0,
           -20,  15,  10,   15, 15,  10,  15, -20,
           -10,  10,  25,   5,  5,  25,  10, -10,
           -15,  20,  10,  5,  5,  10,  20, -15,
            10,  5,  10,  15,  15, 10,   5,  10),
    'K': (   0,  5,  -10, -40, -40,  -10,  5,   0,
            10,  10,   5, -15, -15,   5,  10,  10,
            10,   5, -30, -35, -35, -30,  5,   10,
           -55,  -50, -60,  -40, -40,-60, -50, -55,
           -50, -40, -50, -60, -60, -50,  -20, -50,
           -35, -30, -30, -60, -60, -30, -30, -35,
            5,   0, -5, -50, -50,   -5,  0,   5,
            20,  30,  40,    10,   0,   10,  40,  20),
}

blackpostotal = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                100,  110,  115,  115, 115, 115,  110,  100,
                 60,   65,   70,   75,  75,  70,   65,   60,
                 5,  15,   20,  20,  20,   20,  15, 10,
                 5,   0,  15,   5,  25,   10,   15,  5,
                15,    5,   5,  15,  25,   5,   0,  15,
                -5,   20,  15,  5,  -10,   5, 0, -5,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( -50, -25, -20,  10,  10, -20, -25, -50,
                0,  -5,  45,   10,  10,  45,  -5,   0,
                5,   0,   -5,  40,  40,  -5,   0,   5,
                10,  25,  15,  20,  10,  15,  30,  10,
                0,   5,   20,  15,  35,  20,   5,   0,
               -15,  10,  35,  15,  15,  20,  10, -15,
               -15, -10,  -5,  15,   15,  -5, -10, -15,
               -50, -10, -15, -10, -10, -15, -10, -50),
        'B': ( 10, -20, -30, -35, -35, -30, -20,  10,
               -10,  30,  35,  10,  10,  20,  30, -10,
                 5,  5,   25,  25,  25,  20,  25,   5,
                10,  10,  30,  35,  35,  30,  30,  10,
                10,  20,  10,  25,  25,  30,  10,  10,
                15,  15,  30,  20,  20,  30,  20,  15,
                15,  30,  20,  15,  15,  20,  30,  15,
                20,   5,  -5, -10, -10,  -5,   5,   0),
        'R': (  45,  15,  30,  20, 20,  30,  10,  45,
                45,  40,  45,  45,  45,  45,  40,  45,
                20,  15,  20,  20,  20,  20,  15,  20,
                 0,   5,  15,  15,  15,  15,   5,   0,
               -20,  15,  10,   15, 15,  10,  15,  10,
               -10,  10,  15,   15,  25,  15,   30,  10,
               -15, -20, -20, -25, -25, -20, -20, -15,
               -5,  -15, -10,  30,  25, 20, -15, -10),
        'Q': (   15,   10,  20,  20, 20,  20,  10,  15,
                60,  40,  45,  15,  15,  45,  40,  60,
                20,  15,  20,  20,  20,  20,  15,  20,
                 0,   5,  15,  15,  15,  15,   5,   0,
               -20,  15,  10,   15, 15,  10,  15, -20,
               -10,  10,  25,   5,  5,  25,  10, -10,
               -15,  20,  10,  5,  5,  10,  20, -15,
                10,  5,  10,  15,  15, 10,   5,  10),
        'K': (   0,  5,  -10, -40, -40,  -10,  5,   0,
                10,  10,   5, -15, -15,   5,  10,  10,
                10,   5, -30, -35, -35, -30,  5,   10,
               -55,  -50, -60,  -40, -40,-60, -50, -55,
               -50, -40, -50, -60, -60, -50,  -20, -50,
               -35, -30, -30, -60, -60, -30, -30, -35,
                5,   0, -5, -50, -50,   -5,  0,   5,
                20,  30,  40,    10,   0,   10,  50,  20),
    }

sumofwhites = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'B': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'R': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'Q': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'K': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
    }

sumofblacks = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'B': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'R': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'Q': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'K': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
    }

whiteboardpos = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'B': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'R': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'Q': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'K': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
    }

blackboardpos = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'B': ( 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'R': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'Q': (   0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
        'K': (  0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                 0,   0,   0,   0,   0,   0,   0,   0),
    }


def summoves():
    for n in setpieces:
        for i in range(64):
            sumofwhites[n][i]+=whiteboardpos[n][i]
            sumofblacks[n][i]+=blackboardpos[n][i]
    
def normalize():
    for n in setpieces:
        tot = 0
        for i in sumofwhites[n]:
            tot += i
        tot = tot/64
        for i in sumofwhites[n]:
            i = i/5/tot*piece123

        tot = 0
        for i in sumofblacks[n]:
            tot += i
        tot = tot/64
        for i in sumofblacks[n]:
            i = i/5/tot*piece123
        for i in range(64):
            whitepostotal[n][i] += sumofwhites[n][i]
            blackpostotal[n][i] += sumofblacks[n][i]
            
        tot = 0
        for i in whitepostotal[n]:
            tot += i
        tot = tot/64
        for i in whitepostotal[n]:
            i = i/tot*piece123[n]

        tot = 0
        for i in blackpostotal[n]:
            tot += i
        tot = tot/64
        for i in blackpostotal[n]:
            i = i/tot*piece123[n]

        

####

brd = pygame.display.set_mode((1000,1000))


wicon = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\BRD.jpg')
bicon = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\BBRD.jpg')
def refresh():
    brd.blit(wicon, (0,0))
pygame.display.update()

bpawn = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\Black Pawn.png')
bknight = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\Black Knight.png')
bbishop = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\Black Bishop.png')
brook = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\Black Rook.png')
bqueen = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\Black Queen.png')
bking = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\Black King.png')

wpawn = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\White Pawn.png')
wknight = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\White Knight.png')
wbishop = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\White Bishop.png')
wrook = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\White Rook.png')
wqueen = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\White Queen.png')
wking = pygame.image.load(r'C:\Users\soren\OneDrive\Desktop\Chess\White King.png')

while True: 

    letters = ['a','b','c','d','e','f','g','h']
    piece = { 'P': 180, 'N': 600, 'B': 650, 'R': 950, 'Q': 1850, 'K': 120000 }
    pstw = copy.deepcopy(whitepostotal)
    for k, table in pstw.items():
        padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
        pstw[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
        pstw[k] = (0,)*20 + pstw[k] + (0,)*20
        
    pstb = copy.deepcopy(blackpostotal)
    for k, table in pstb.items():
        padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
        pstb[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
        pstb[k] = (0,)*20 + pstb[k] + (0,)*20




    A1, H1, A8, H8 = 91, 98, 21, 28
    initial = (
        '         \n'
        '         \n'
        ' rnbqkbnr\n'
        ' pppppppp\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' PPPPPPPP\n'
        ' RNBQKBNR\n'
        '         \n'
        '         \n'
    )

    N, E, S, W = -10, 1, 10, -1
    directions = {
        'P': (N, N+N, N+W, N+E),
        'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
        'B': (N+E, S+E, S+W, N+W),
        'R': (N, E, S, W),
        'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
        'K': (N, E, S, W, N+E, S+E, S+W, N+W)
    }

    MATE_LOWER = piece['K'] - 10*piece['Q']
    MATE_UPPER = piece['K'] + 10*piece['Q']

    TABLE_SIZE = 1e8

    QS_LIMIT = 150
    EVAL_ROUGHNESS = 20

    OutstandingMove = (
        '         \n'
        '         \n'
        ' RNBQKBNR\n'
        ' PPPPPPPP\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        '         \n'
        '         \n'
    )
    class Position(namedtuple('Position', 'board score wc bc ep kp')):


        def gen_moves(self):

            for i, p in enumerate(self.board):
                if not p.isupper(): continue
                for d in directions[p]:
                    for j in count(i+d, d):
                        q = self.board[j]
                        if q.isspace() or q.isupper(): break
                        if p == 'P' and d in (N, N+N) and q != '.': break
                        if p == 'P' and d == N+N and (i < A1+N or self.board[i+N] != '.'): break
                        if p == 'P' and d in (N+W, N+E) and q == '.' and j not in (self.ep, self.kp): break
                        yield (i, j)
                        if p in 'PNK' or q.islower(): break
                        if i == A1 and self.board[j+E] == 'K' and self.wc[0]: yield (j+E, j+W)
                        if i == H1 and self.board[j+W] == 'K' and self.wc[1]: yield (j+W, j+E)

        def rotate(self):
            ''' Rotates the board, preserving enpassant '''
            return Position(
                self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
                119-self.ep if self.ep else 0,
                119-self.kp if self.kp else 0)

        def nullmove(self):
            ''' Like rotate, but clears ep and kp '''
            return Position(
                self.board[::-1].swapcase(), -self.score,
                self.bc, self.wc, 0, 0)

        def move(self, move):
            i, j = move
            p, q = self.board[i], self.board[j]
            put = lambda board, i, p: board[:i] + p + board[i+1:]
            board = self.board
            wc, bc, ep, kp = self.wc, self.bc, 0, 0
            score = self.score + self.value(move)
            board = put(board, j, board[i])
            board = put(board, i, '.')
            if i == A1: wc = (False, wc[1])
            if i == H1: wc = (wc[0], False)
            if j == A8: bc = (bc[0], False)
            if j == H8: bc = (False, bc[1])
            if p == 'K':
                wc = (False, False)
                if abs(j-i) == 2:
                    kp = (i+j)//2
                    board = put(board, A1 if j < i else H1, '.')
                    board = put(board, kp, 'R')
            if p == 'P':
                if A8 <= j <= H8:
                    board = put(board, j, 'Q')
                if j - i == 2*N:
                    ep = i + N
                if j - i in (N+W, N+E) and q == '.':
                    board = put(board, j+S, '.')
            return Position(board, score, wc, bc, ep, kp).rotate()


        def value(self, move):
            i, j = move
            p, q = self.board[i], self.board[j]
            score = pst[p][j] - pst[p][i]
            if move != None:
                if p.upper() == 'K':
                    if j-i in (W+W, E+E):
                        score += 50
            if q.islower():
                score += pst[q.upper()][119-j]
            if abs(j-self.kp) < 2:
                score += pst['K'][119-j]
            if p == 'K' and abs(i-j) == 2:
                score += pst['R'][(i+j)//2]
                score -= pst['R'][A1 if j < i else H1]
            if p == 'P':
                if A8 <= j <= H8:
                    score += pst['Q'][j] - pst['P'][j]
                if j == self.ep:
                    score += pst['P'][119-(j+S)]
            return score

    Entry = namedtuple('Entry', 'lower upper')

    class LRUCache:
        def __init__(self, size):
            self.od = OrderedDict()
            self.size = size

        def get(self, key, default=None):
            try: self.od.move_to_end(key)
            except KeyError: return default
            return self.od[key]

        def __setitem__(self, key, value):
            try: del self.od[key]
            except KeyError:
                if len(self.od) == self.size:
                    self.od.popitem(last=False)
            self.od[key] = value

    class Searcher:
        def __init__(self):
            self.tp_score = LRUCache(TABLE_SIZE)
            self.tp_move = LRUCache(TABLE_SIZE)
            self.nodes = 0

        def bound(self, pos, gamma, depth, root=True):

            self.nodes += 1

            depth = max(depth, 0)

            if pos.score <= -MATE_LOWER:
                return -MATE_UPPER

            entry = self.tp_score.get((pos, depth, root), Entry(-MATE_UPPER, MATE_UPPER))
            if entry.lower >= gamma and (not root or self.tp_move.get(pos) is not None):
                return entry.lower
            if entry.upper < gamma:
                return entry.upper


            def moves():
                if depth > 0 and not root and any(c in pos.board for c in 'RBNQ'):
                    yield None, -self.bound(pos.nullmove(), 1-gamma, depth-3, root=False)
                if depth == 0:
                    yield None, pos.score
                killer = self.tp_move.get(pos)
                if killer and (depth > 0 or pos.value(killer) >= QS_LIMIT):
                    yield killer, -self.bound(pos.move(killer), 1-gamma, depth-1, root=False)
                for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
                    check = 0
                    for n in (pos.move(move)).gen_moves():
                        kcount = 0
                        for i in (pos.move(move)).move(n):
                            for p in str(i):
                                if p == 'K':
                                    kcount+=1
                            if kcount == 0:
                                check = 1
                    if depth > 0 or pos.value(move) >= QS_LIMIT:
                        if check != 1:
                            yield move, -self.bound(pos.move(move), 1-gamma, depth-1, root=False) - 300
                            

            best = -MATE_UPPER
            for move, score in moves():
                best = max(best, int(score*random.randint(80,120)/100))
                if best >= gamma:
                    self.tp_move[pos] = move
                    break

            if best < gamma and best < 0 and depth > 0:
                is_dead = lambda pos: any(pos.value(m) >= MATE_LOWER for m in pos.gen_moves())
                if all(is_dead(pos.move(m)) for m in pos.gen_moves()):
                    in_check = is_dead(pos.nullmove())
                    best = -MATE_UPPER if in_check else 0


            if best >= gamma:
                self.tp_score[(pos, depth, root)] = Entry(best, entry.upper)
            if best < gamma:
                self.tp_score[(pos, depth, root)] = Entry(entry.lower, best)

            return best


        def _search(self, pos):
            self.nodes = 0

            for depth in range(1, 1000):
                self.depth = depth

                lower, upper = -MATE_UPPER, MATE_UPPER
                while lower < upper - EVAL_ROUGHNESS:
                    gamma = (lower+upper+1)//2
                    score = self.bound(pos, gamma, depth)
                    if score >= gamma:
                        lower = score
                    if score < gamma:
                        upper = score
                
                score = self.bound(pos, lower, depth)

                yield

        def search(self, pos, secs):
            start = time.time()
            for _ in self._search(pos):
                if time.time() - start > secs:
                    break
            return self.tp_move.get(pos), self.tp_score.get((pos, self.depth, True)).lower


    if sys.version_info[0] == 2:
        input = raw_input
        class NewOrderedDict(OrderedDict):
            def move_to_end(self, key):
                value = self.pop(key)
                self[key] = value
        OrderedDict = NewOrderedDict


    def parse(c):
        fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
        return A1 + fil - 10*rank


    def render(i):
        rank, fil = divmod(i - A1, 10)
        return chr(fil + ord('a')) + str(-rank + 1)


    def print_pos(pos):
        whiteboardpos = {
            'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0),
            'N': ( 0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0),
            'B': ( 0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0),
            'R': (  0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0),
            'Q': (   0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0),
            'K': (  0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                    0,   0,   0,   0,   0,   0,   0,   0,
                     0,   0,   0,   0,   0,   0,   0,   0),
        }
        brd.blit(wicon,(0,0))
        white = []
        black = []
        whitenames = []
        blacknames = []
        deadwhite = []
        deadblack = []
        originalwhite = [1,1,1,1,1,1,1,1,2,2,3,3,4,4,5,6]
        originalblack = [1,1,1,1,1,1,1,1,2,2,3,3,4,4,5,6]
        for r in range(8):
            for c in range(8):
                number = 0
                p = pos.board.split()[r][c]
                if p.upper() == 'P':
                    number = 1
                elif p.upper() == 'N':
                    number = 2
                elif p.upper() == 'B':
                    number = 3
                elif p.upper() == 'R':
                    number = 4
                elif p.upper() == 'Q':
                    number = 5
                elif p.upper() == 'K':
                    number = 6
                if p.isupper():
                    white.append(number)
                elif p.islower():
                    black.append(number)
        white.sort()
        black.sort()
        for j in white:
            if j in originalwhite:
                originalwhite.remove(j)
        for k in black:
            if k in originalblack:
                originalblack.remove(k)
        for w in white:
            if w == 1:
                whitenames.append('P')
            if w == 2:
                whitenames.append('N')
            if w == 3:
                whitenames.append('B')
            if w == 4:
                whitenames.append('R')
            if w == 5:
                whitenames.append('Q')
            if w == 6:
                whitenames.append('K')
        for n in black:
            if n == 1:
                blacknames.append('P')
            if n == 2:
                blacknames.append('N')
            if n == 3:
                blacknames.append('B')
            if n == 4:
                blacknames.append('R')
            if n == 5:
                blacknames.append('Q')
            if n == 6:
                blacknames.append('K')
        for w in originalwhite:
            if w == 1:
                deadwhite.append('P')
            if w == 2:
                deadwhite.append('N')
            if w == 3:
                deadwhite.append('B')
            if w == 4:
                deadwhite.append('R')
            if w == 5:
                deadwhite.append('Q')
            if w == 6:
                deadwhite.append('K')
        for n in originalblack:
            if n == 1:
                deadblack.append('P')
            if n == 2:
                deadblack.append('N')
            if n == 3:
                deadblack.append('B')
            if n == 4:
                deadblack.append('R')
            if n == 5:
                deadblack.append('Q')
            if n == 6:
                deadblack.append('K')
        for x in range(8):
            for y in range(8):
                p = ''
                if pos.board.split()[x][y].islower():
                    color = 'w'
                    p = pos.board.split()[x][y].upper()
                elif pos.board.split()[x][y].isupper():
                    color = 'b'
                    p = pos.board.split()[x][y]
                if pos.board.split()[x][y].isupper() or pos.board.split()[x][y].islower():
                    if color == 'w':
                        if p.lower() == 'p':
                            brd.blit(wpawn, (90*x+20, 90*y+20))
                        if p.lower() == 'n':
                            brd.blit(wknight, (90*x+20, 90*y+20))
                        if p.lower() == 'b':
                            brd.blit(wbishop, (90*x+20, 90*y+20))
                        if p.lower() == 'r':
                            brd.blit(wrook, (90*x+20, 90*y+20))
                        if p.lower() == 'q':
                            brd.blit(wqueen, (90*x+20, 90*y+20))
                        if p.lower() == 'k':
                            brd.blit(wking, (90*x+20, 90*y+20))
                        whiteboardpos[p.upper][8*x+y] = 1
                    if color == 'b':
                        if p.lower() == 'p':
                            brd.blit(bpawn, (90*x+20, 90*y+20))
                        if p.lower() == 'n':
                            brd.blit(bknight, (90*x+20, 90*y+20))
                        if p.lower() == 'b':
                            brd.blit(bbishop, (90*x+20, 90*y+20))
                        if p.lower() == 'r':
                            brd.blit(brook, (90*x+20, 90*y+20))
                        if p.lower() == 'q':
                            brd.blit(bqueen, (90*x+20, 90*y+20))
                        if p.lower() == 'k':
                            brd.blit(bking, (90*x+20, 90*y+20))
                        blackboardpos[p.upper][8*x+y] = 1
        for i in range(len(deadwhite)):
            x = deadwhite[i]
            if x.lower() == 'p':
                brd.blit(wpawn, (i*55+10,0))
            if x.lower() == 'n':
                brd.blit(wknight, (i*55+10,0))
            if x.lower() == 'b':
                brd.blit(wbishop, (i*55+10,0))
            if x.lower() == 'r':
                brd.blit(wrook, (i*55+10,0))
            if x.lower() == 'q':
                brd.blit(wqueen, (i*55+10,0))
            if x.lower() == 'k':
                brd.blit(wking, (i*55+10,0))
        
        for i in range(len(deadblack)):
            x = deadblack[i]
            if x.lower() == 'p':
                brd.blit(bpawn, (-i*55+990,1000))
            if x.lower() == 'n':
                brd.blit(bknight, (-i*55+990,1000))
            if x.lower() == 'b':
                brd.blit(bbishop, (-i*55+990,1000))
            if x.lower() == 'r':
                brd.blit(brook, (-i*55+990,1000))
            if x.lower() == 'q':
                brd.blit(bqueen, (-i*55+990,1000))
            if x.lower() == 'k':
                brd.blit(bking, (-i*55+990,1000))
        pygame.display.update()
print_pos()
