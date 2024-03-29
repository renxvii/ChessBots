import sys
#
from JIT_3x0_ import *

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

        
