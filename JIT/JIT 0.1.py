from __future__ import print_function
import random
import re, sys, time
from itertools import count
from collections import OrderedDict, namedtuple
from copy import deepcopy



letters = ['a','b','c','d','e','f','g','h']
piece = { 'P': 200, 'N': 550, 'B': 650, 'R': 950, 'Q': 1850, 'K': 120000 }
pstw = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            100,  110,  115,  115, 115, 115,  110,  100,
             60,   65,   70,   75,  75,  70,   65,   60,
             5,  15,   20,  20,  30,   20,  15, 10,
             5,   0,  15,  30,  40,   15,   0,  5,
            15,    5,   5,  0,  10,   5,   5,  15,
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
            20,  30,  40,    10,   0,   -10,  40,  20),
}
for k, table in pstw.items():
    padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
    pstw[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
    pstw[k] = (0,)*20 + pstw[k] + (0,)*20
    
pstb = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            100,  110,  115,  115, 115, 115,  110,  100,
             60,   65,   70,   75,  75,  70,   65,   60,
             5,  15,   20,  20,  20,   20,  15, 10,
             5,   0,  15,   25,  15,   10,   15,  5,
            15,    5,   5,  10,  25,   5,   0,  15,
            -5,   20,  15,  -10,  5,   5, 0, -5,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -50, -25, -20,  10,  10, -20, -25, -50,
            0,  -5,  45,   10,  10,  45,  -5,   0,
            5,   0,   -5,  40,  40,  -5,   0,   5,
            10,  25,  15,  20,  10,  15,  30,  10,
            0,   5,   20,  15,  35,  20,   5,   0,
           -15,  10,  20,  15,  15,  15,  10, -15,
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
           -10,  -15,  40,  25,  30, -5, -15, -10),
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
            20,  50, -15,    0,   10,   40,  30,  20),
}
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
        return Position(
            self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
            119-self.ep if self.ep else 0,
            119-self.kp if self.kp else 0)

    def switch(self):
        return Position(
            self.board[::-1],-self.score, self.bc, self.wc,
            119-self.ep if self.ep else 0,
            119-self.kp if self.kp else 0)

    def flip(self):
        return Position(
            self.board[::-1].swapcase(), self.score, self.bc, self.wc,
            self.kp if self.ep else 0,
            self.ep if self.kp else 0)
    

    def nullmove(self):
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
        return score*random.randint(85,115)/100

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
                if incheck(pos.move(killer))==1:
                    yield killer, -self.bound(pos.move(killer), 1-gamma, depth-1, root=False)
                else:
                    yield killer, 0
            for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
                k = []
                for i in range(len(history)-1):
                    if history[i] == pos.move(move):    
                        k.append(i)
                if len(k) == 2:
                    yield move, 0
                elif depth > 0 or pos.value(move) >= QS_LIMIT:
                    yield move, -self.bound(pos.move(move), 1-gamma, depth-1, root=False)

                
        best = -MATE_UPPER
        for move, score in moves():
            best = max(best, score)
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
            if time.time() - start > secs*1.5:
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
    white = []
    black = []
    whiteynames = []
    niBBanames = []
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
            whiteynames.append('P')
        if w == 2:
            whiteynames.append('N')
        if w == 3:
            whiteynames.append('B')
        if w == 4:
            whiteynames.append('R')
        if w == 5:
            whiteynames.append('Q')
        if w == 6:
            whiteynames.append('K')
    for n in black:
        if n == 1:
            niBBanames.append('P')
        if n == 2:
            niBBanames.append('N')
        if n == 3:
            niBBanames.append('B')
        if n == 4:
            niBBanames.append('R')
        if n == 5:
            niBBanames.append('Q')
        if n == 6:
            niBBanames.append('K')
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
        a=sys.stdout.shell.write(str(8-x), 'DEFINITION')
        a=sys.stdout.shell.write('   ', 'DEFINITION')
        for y in range(8):
            p = ''
            if pos.board.split()[x][y].islower():
                color = 'console'
                p = pos.board.split()[x][y].upper()
            elif pos.board.split()[x][y].isupper():
                color = 'KEYWORD'
                p = pos.board.split()[x][y]
            if (x+y)%2==1:
                square = 'console'
            else:
                square = 'KEYWORD'
            a=sys.stdout.shell.write('[',square)
            if pos.board.split()[x][y].isupper() or pos.board.split()[x][y].islower():
                a=sys.stdout.shell.write(p, color)
            else:
                a=sys.stdout.shell.write(' ')
            a=sys.stdout.shell.write(']',square)
        if x == 0:
            a = sys.stdout.shell.write('    Taken Material', 'console')
        if x == 1:
            a = sys.stdout.shell.write('    ')
            for dw in deadwhite:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(dw, 'KEYWORD')
        if x == 2:
            a = sys.stdout.shell.write('    Remaining Material', 'console')
        if x == 3:
            a = sys.stdout.shell.write('    ')
            for nn in niBBanames:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(nn, 'console')
        if x == 4:
            a = sys.stdout.shell.write('    ')
            for ww in whiteynames:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(ww, 'KEYWORD')
        if x == 5:
            a = sys.stdout.shell.write('    Remaining Material', 'KEYWORD')
        if x == 6:
            a = sys.stdout.shell.write('    ')
            for dn in deadblack:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(dn, 'console')
        if x == 7:
            a = sys.stdout.shell.write('    Taken Material', 'KEYWORD')
        sys.stdout.shell.write('\n') 
    sys.stdout.shell.write('\n') 
    a=sys.stdout.shell.write('     A  B  C  D  E  F  G  H', 'DEFINITION')

def print_pos2(pos):
    white = []
    black = []
    whiteynames = []
    niBBanames = []
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
                black.append(number)
            elif p.islower():
                white.append(number)
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
            whiteynames.append('P')
        if w == 2:
            whiteynames.append('N')
        if w == 3:
            whiteynames.append('B')
        if w == 4:
            whiteynames.append('R')
        if w == 5:
            whiteynames.append('Q')
        if w == 6:
            whiteynames.append('K')
    for n in black:
        if n == 1:
            niBBanames.append('P')
        if n == 2:
            niBBanames.append('N')
        if n == 3:
            niBBanames.append('B')
        if n == 4:
            niBBanames.append('R')
        if n == 5:
            niBBanames.append('Q')
        if n == 6:
            niBBanames.append('K')
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
        a=sys.stdout.shell.write(str(x+1), 'DEFINITION')
        a=sys.stdout.shell.write('   ', 'DEFINITION')
        for y in range(8):
            p = ''
            if pos.board.split()[x][y].islower():
                color = 'KEYWORD'
                p = pos.board.split()[x][y].upper()
            elif pos.board.split()[x][y].isupper():
                color = 'console'
                p = pos.board.split()[x][y]
            if (x+y)%2==0:
                square = 'KEYWORD'
            else:
                square = 'console'
            a=sys.stdout.shell.write('[',square)
            if pos.board.split()[x][y].isupper() or pos.board.split()[x][y].islower():
                a=sys.stdout.shell.write(p, color)
            else:
                a=sys.stdout.shell.write(' ')
            a=sys.stdout.shell.write(']',square)
        if x == 7:
            a = sys.stdout.shell.write('    Taken Material', 'console')
        if x == 6:
            a = sys.stdout.shell.write('    ')
            for dw in deadwhite:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(dw, 'KEYWORD')
        if x == 5:
            a = sys.stdout.shell.write('    Remaining Material', 'console')
        if x == 4:
            a = sys.stdout.shell.write('    ')
            for nn in niBBanames:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(nn, 'console')
        if x == 3:
            a = sys.stdout.shell.write('    ')
            for ww in whiteynames:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(ww, 'KEYWORD')
        if x == 2:
            a = sys.stdout.shell.write('    Remaining Material', 'KEYWORD')
        if x == 1:
            a = sys.stdout.shell.write('    ')
            for dn in deadblack:
                a = sys.stdout.shell.write(' ')
                a=sys.stdout.shell.write(dn, 'console')
        if x == 0:
            a = sys.stdout.shell.write('    Taken Material', 'KEYWORD')
        sys.stdout.shell.write('\n') 
    sys.stdout.shell.write('\n') 
    a=sys.stdout.shell.write('     H  G  F  E  D  C  B  A', 'DEFINITION')
    
def print_pos3(pos):
    for x in range(8):
        a=sys.stdout.shell.write(str(8-x), 'DEFINITION')
        a=sys.stdout.shell.write('   ', 'DEFINITION')
        for y in range(8):
            p = ''
            if pos.board.split()[x][y].islower():
                color = 'KEYWORD'
                p = pos.board.split()[x][y].upper()
            elif pos.board.split()[x][y].isupper():
                color = 'console'
                p = pos.board.split()[x][y]
            if (x+y)%2==0:
                square = 'KEYWORD'
            else:
                square = 'console'
            a=sys.stdout.shell.write('[',square)
            if pos.board.split()[x][y].isupper() or pos.board.split()[x][y].islower():
                a=sys.stdout.shell.write(p, color)
            else:
                a=sys.stdout.shell.write(' ')
            a=sys.stdout.shell.write(']',square)
        sys.stdout.shell.write('\n') 
    sys.stdout.shell.write('\n') 
    a=sys.stdout.shell.write('     A  B  C  D  E  F  G  H', 'DEFINITION')
def incheck(pos):
    for h in range(len(pos.board)-1):
        if pos.board[h].upper() == 'K':
            for i in pos.rotate().gen_moves():
                if pos.rotate().move(i).board[h].lower() in letters2:
                    return 1
gg = 0
def run(x, y, pos, turn, color, h):
    searcher = Searcher()
    sys.stdout.shell.write('\n') 
    sys.stdout.shell.write('\n' + '\n    Level ' + str(x+1) + ' Computer vs Level ' + str(y+1) + ' Computer\n')
    sys.stdout.shell.write('\n') 
    history = h
    history.append(pos)
    check = 0
    gg = 0
    TO = False
    if color == 1:
        print_pos(pos)
    else:
        print_pos2(pos)
    while True:
        if color == 1:
            if TO == True:
                break
            pst = deepcopy(pstw)
            move, score = searcher.search(pos, secs=3*check+x)
            if score == -MATE_UPPER:
                sys.stdout.shell.write('\n' + "\n\n    White resigns")
                break
            if letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)) == 'e1c1' and pos.wc[1] == True:
                a = sys.stdout.shell.write("\n\n\n    White Jit's move: 0-0-0",'DEFINITION')
            elif letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)) == 'e1g1' and pos.wc[0] == True:
                a = sys.stdout.shell.write("\n\n\n    White Jit's move: 0-0",'DEFINITION')
            else:
                a = sys.stdout.shell.write("\n\n\n    White Jit's move: " + letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)),'DEFINITION')
            saved = 0
            check = 0
            for h in range(len(pos.board)-1):
                if pos.board[h].upper() == 'K':
                    saved = h
                for i in pos.rotate().gen_moves():
                    if pos.rotate().move(i).board[saved].lower() in letters2:
                        check = 1
            if check == 1:
                a = sys.stdout.shell.write('+', 'DEFINITION')
            if score == MATE_UPPER:
                a = sys.stdout.shell.write('+', 'DEFINITION')
                gg = 1
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + "\n    White Move "+ str(int((turn+1)/2)) + '\n', 'KEYWORD')
            turn += 1
            pos = pos.move(move)
            history.append(pos)
            print_pos(pos.rotate())
            k = []
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n\n    White resigns')
                    TO = True
                    break
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
            
                

            pst = deepcopy(pstb)
            move, score = searcher.search(pos, secs=3*check+y)
            if score == -MATE_UPPER:
                sys.stdout.shell.write('\n' + "\n\n    Black resigns")
                break
            if move:
                if pos.board[119-parse('e4')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n' and letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'd7d5' and turn < 10:
                    if random.randint(1,50) < 40 and pos.board[119-parse('e7')].lower()=='p'and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('e7'), 119-parse('e5')
                    elif random.randint(1,50) < 40 and pos.board[119-parse('c7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('c7'), 119-parse('c5')
                    elif pos.board[119-parse('d7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('d7'), 119-parse('d6')
                    
            
            if letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8c8' and pos.bc[1] == True:
                a = sys.stdout.shell.write("\n\n\n    Black Jit's move: 0-0-0",'DEFINITION')
    
            elif letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8g8' and pos.bc[0] == True:
                a = sys.stdout.shell.write("\n\n\n    Black Jit's move: 0-0",'DEFINITION')
            else:
                a = sys.stdout.shell.write("\n\n\n    Black Jit's move: " + letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)),'DEFINITION')
            
            pos = pos.move(move)
            saved = 0
            check = 0
            for h in range(len(pos.board)-1):
                if pos.board[h].upper() == 'K':
                    saved = h
                for i in pos.rotate().gen_moves():
                    if pos.rotate().move(i).board[saved].lower() in letters2:
                        check = 1
            if check == 1:
                a = sys.stdout.shell.write('+', 'DEFINITION')
            if score == MATE_UPPER:
                a = sys.stdout.shell.write('+', 'DEFINITION')
                gg = 1
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + "\n    Black Move " + str(int((turn+1)/2)) + '\n')
            turn += 1
            history.append(pos)
            print_pos(pos)
            
            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n\n    Black resigns')
                    TO = True
                    break

            
        if color == 2:
            if TO == True:
                break
            pst = deepcopy(pstb)
            move, score = searcher.search(pos, secs=3*check+y)
            if score == -MATE_UPPER:
                sys.stdout.shell.write('\n' + "\n\n    Black resigns")
                break
            if move:
                if pos.board[119-parse('e4')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n' and letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'd7d5' and turn < 10:
                    if random.randint(1,50) < 40 and pos.board[119-parse('e7')].lower()=='p'and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('e7'), 119-parse('e5')
                    elif random.randint(1,50) < 40 and pos.board[119-parse('c7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('c7'), 119-parse('c5')
                    elif pos.board[119-parse('d7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('d7'), 119-parse('d6')
                    
            if letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8c8' and pos.bc[1] == True:
                a = sys.stdout.shell.write("\n\n\n    Black Jit's move: 0-0-0",'DEFINITION')
    
            elif letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8g8' and pos.bc[0] == True:
                a = sys.stdout.shell.write("\n\n\n    Black Jit's move: 0-0",'DEFINITION')
            else:
                a = sys.stdout.shell.write("\n\n\n    Black Jit's move: " + letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)),'DEFINITION')
            
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + "\n    Black Move " + str(int((turn+1)/2)) + '\n')
            turn += 1
            history.append(pos)
            pos = pos.move(move)
            print_pos2(pos.rotate())
            
            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n\n    Black resigns')
                    TO = True
                    break

            pst = deepcopy(pstw)
            move, score = searcher.search(pos, secs=3*check+x)
            if score == -MATE_UPPER:
                sys.stdout.shell.write('\n' + "\n\n    White resigns")
                break
            if letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)) == 'e1c1' and pos.wc[1] == True:
                a = sys.stdout.shell.write("\n\n\n    White Jit's move: 0-0-0",'DEFINITION')
            elif letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)) == 'e1g1' and pos.wc[0] == True:
                a = sys.stdout.shell.write("\n\n\n    White Jit's move: 0-0",'DEFINITION')
            else:
                a = sys.stdout.shell.write("\n\n\n    White Jit's move: " + letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)),'DEFINITION')
            
            
            pos = pos.move(move)
            
            saved = 0
            check = 0
            for h in range(len(pos.board)-1):
                if pos.board[h].upper() == 'K':
                    saved = h
                for i in pos.rotate().gen_moves():
                    if pos.rotate().move(i).board[saved].lower() in letters2:
                        check = 1
            if check == 1:
                a = sys.stdout.shell.write('+', 'DEFINITION')
            if score == MATE_UPPER:
                a = sys.stdout.shell.write('+', 'DEFINITION')
                gg = 1
            history.append(pos)
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + "\n    White Move "+ str(int((turn+1)/2)) + '\n', 'KEYWORD')
            turn += 1
            print_pos2(pos)
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n\n    White resigns')
                    TO = True
                    break
            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
                        
def playWhite(x, pos, turn, trueturn, color, h):
    TO = False
    OM = False
    searcher = Searcher()
    history = h
    history.append(pos)
    sys.stdout.shell.write('\n') 
    sys.stdout.shell.write('\n' + '\n    Human vs Level ' + str(x+1) + ' Computer\n')
    sys.stdout.shell.write('\n') 
    pst = deepcopy(pstb)
    check = 0
    gg = 0
    if color == 1:
        print_pos(pos)
    else:
        print_pos(pos.rotate())
    while True:
        if TO == True:
            break
        if color == 1:
            if TO == True:
                break
            move = None
            while move not in pos.gen_moves():
                if TO == True:
                    break
                user = input('\n\n    Your move: ')
                if str(user) == 'no u':
                    sys.stdout.shell.write('\n' + '\n\n    Outstanding move!')
                    OM = True
                    TO = True
                    break
                elif str(user).upper() == 'UNDO' and trueturn>=2:
                    pos = history[len(history)-3]
                    if history[len(history)-2] == 'EDIT':
                        sys.stdout.shell.write('\n' + '\n    Edit reversed')
                    else:
                        turn-=2
                    history.remove(history[len(history)-1])
                    history.remove(history[len(history)-1])
                    trueturn-=2
                    sys.stdout.shell.write('\n') 
                    if turn>1:
                        sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn)/2)) + '\n')
                    else:
                        sys.stdout.shell.write('\n' + '\n    Human vs Level ' + str(x+1) + ' Computer\n    Again...\n')
                    print_pos(pos)                    

                elif str(user).upper() == 'EDIT':
                    match = re.match('([a-h][1-8])', input('    Square\n    '))
                    if match:
                        editsquare = parse(match.group(1))
                        if editsquare == 'e1':
                            pos.wc = (False, False)
                        elif editsquare == 'e8':
                            pos.bc = (False, False)
                        elif editsquare == 'a1':
                            pos.wc[1] = False
                        elif editsquare == 'h1':
                            pos.wc[0] = False
                        elif editsquare == 'a8':
                            pos.bc[1] = False
                        elif editsquare == 'h8':
                            pos.bc[0] = False
                        user2 = input('    Piece: p, n, b, r, q, k, P, N, B, R, Q, K \n    (or period for an empty square)\n    ')
                        if editsquare>=22 and editsquare<=99 and str(user2).upper() in ['P','N','B','R','Q','K'] or str(user2) == '.':
                            board = list(pos.board)
                            board[editsquare] = user2
                            pos = Position("".join(board), pos.score, pos.wc, pos.bc, pos.ep, pos.kp)
                            if turn>1:
                                sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn)/2)) + '(edited)\n')
                            else:
                                sys.stdout.shell.write('\n' + '\n    Human vs Level ' + str(x+1) + ' Computer (edited)\n')
                            print_pos(pos)
                            trueturn+=2
                            history.append('EDIT')
                            history.append(pos)
                elif str(user).upper() == 'TAKE OVER' or str(user).upper() == 'TAKEOVER':
                    play4 = True
                    while play4 == True:
                        y = input('\n\n    AI strength\n    ')
                        if y in ['1','2','3','4','5','6','7','8','9','10']:
                            play4 = False
                            
                            run(int(y)-1,x,pos,turn,2,history)
                            TO = True
                            break
                        elif y.upper() == 'CANCEL':
                            play4 = False
                        else:
                            sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')
                elif str(user).upper() == 'SWITCH':
                    playBlack(x,pos,turn,trueturn,history)
                    break
                elif str(user) == '0-0':
                    move = parse('e1'), parse('g1')
                elif str(user) == '0-0-0':
                    move = parse('e1'), parse('c1')
                elif str(user).upper() == 'RESIGN':
                    sys.stdout.shell.write('\n' + '\n    I accept your resignation, thank you')
                elif str(user).upper() == 'OFFER DRAW' or str(user).upper() =='DRAW':
                    move, score = searcher.search(pos.rotate(), secs = x)
                    if score < -100:
                        sys.stdout.shell.write('\n' + '\n    I accept your draw, thank you')
                        break
                    else:
                        sys.stdout.shell.write('\n' + '\n    I would like to play a little bit longer!')
                        move = None
                else:
                    match = re.match('([a-h][1-8])'*2, user)
                        
                    if match:
                        move = parse(match.group(1)), parse(match.group(2))
                        if incheck(pos.move(move).rotate()) == 1:
                            move = None
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                        elif move not in pos.gen_moves():
                            move = None
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                        elif pos.board[move[0]].islower():
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                            move = None
                        elif pos.board[move[0]] == '.':
                            move = None
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                    else:
                        sys.stdout.shell.write("    Please enter a move like g8f6", "ERROR")
            if OM == True:
                sys.stdout.shell.write('\n' + '\n')
                print_pos(Outstanding)
                sys.stdout.shell.write('\n' + '\n')
                break
            pos = pos.move(move)
            if pos.score == -MATE_UPPER or gg == 1:
                TO = True
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n\n    I resign')
                    break
            history.append(pos)
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + '\n    White Move ' + str(int((turn+1)/2)) + '\n', 'KEYWORD')
            print_pos(pos.rotate())

            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
                
            turn+=1
            trueturn+=1
                
            move, score = searcher.search(pos, secs=3*check+x)
            if score == -MATE_UPPER:
                sys.stdout.shell.write('\n' + "\n\n    I resign")
                break
            if move:
                if pos.board[119-parse('e4')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n' and letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'd7d5' and turn < 10:
                    if random.randint(1,50) < 40 and pos.board[119-parse('e7')].lower()=='p'and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('e7'), 119-parse('e5')
                    elif random.randint(1,50) < 40 and pos.board[119-parse('c7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('c7'), 119-parse('c5')
                    elif pos.board[119-parse('d7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('d7'), 119-parse('d6')
                
            pos = pos.move(move)
            saved = 0
            check = 0
            sys.stdout.shell.write('\n') 
            if letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e1c1' and pos.bc[1] == True:
                a = sys.stdout.shell.write("\n\n\n    Jit's move: 0-0-0",'DEFINITION')
            elif letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8g8' and pos.bc[0] == True:
                a = sys.stdout.shell.write("\n\n\n    Jit's move: 0-0",'DEFINITION')
            else:
                a = sys.stdout.shell.write("\n\n\n    Jit's move: " + letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)),'DEFINITION')
            
            for h in range(len(pos.board)-1):
                if pos.board[h].upper() == 'K':
                    saved = h
                for i in pos.rotate().gen_moves():
                    if pos.rotate().move(i).board[saved].lower() in letters2:
                        check = 1
            if check == 1:
                a = sys.stdout.shell.write('+', 'DEFINITION')
            if score == MATE_UPPER:
                a = sys.stdout.shell.write('+', 'DEFINITION')
                gg = 1
            history.append(pos) 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn+1)/2)) + '\n')
            print_pos(pos)
            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break

            
            turn+=1
            trueturn+=1
        
        if color == 2:
            if TO == True:
                break
            move, score = searcher.search(pos, secs=3*check+x)
            if score == -MATE_UPPER:
                sys.stdout.shell.write('\n' + "\n\n    I resign")
                break
            if move:
                if pos.board[119-parse('e4')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n' and letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'd7d5' and turn < 10:
                    if pos.board[119-parse('e5')].lower()=='.' and pos.board[119-parse('e6')].lower()=='.' and random.randint(1,50) < 40 and pos.board[119-parse('e7')].lower()=='p'and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('e7'), 119-parse('e5')
                    elif pos.board[119-parse('c6')].lower()=='.' and pos.board[119-parse('c5')].lower()=='.' and random.randint(1,50) < 40 and pos.board[119-parse('c7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('c7'), 119-parse('c5')
                    elif pos.board[119-parse('d7')].lower()=='p' and pos.board[119-parse('f6')].lower()!='n':
                        move = 119-parse('d7'), 119-parse('d6')
            pos = pos.move(move)
            history.append(pos) 
            sys.stdout.shell.write('\n') 
            if letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8c8' and pos.bc[1] == True:
                a = sys.stdout.shell.write("\n\n\n    Jit's move: 0-0-0",'DEFINITION')
    
            elif letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e8g8' and pos.bc[0] == True:
                a = sys.stdout.shell.write("\n\n\n    Jit's move: 0-0",'DEFINITION')
            else:
                a = sys.stdout.shell.write("\n\n\n    Jit's move: " + letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)),'DEFINITION')
            for h in range(len(pos.board)-1):
                if pos.board[h].upper() == 'K':
                    saved = h
                for i in pos.rotate().gen_moves():
                    if pos.rotate().move(i).board[saved].lower() in letters2:
                        check = 1
            if check == 1:
                a = sys.stdout.shell.write('+', 'DEFINITION')
            if score == MATE_UPPER:
                a = sys.stdout.shell.write('+', 'DEFINITION')
                gg = 1
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn+1)/2)) + '\n')
            print_pos(pos)
            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break
                
        
            turn+=1
            trueturn+=1
            
            move = None
            while move not in pos.gen_moves():
                if TO == True:
                    break
                user = input('\n\n    Your move: ')
                if str(user) == 'no u':
                    sys.stdout.shell.write('\n' + '\n\n    Outstanding move!')
                    OM = True
                    TO = True
                    break
                elif str(user).upper() == 'UNDO' and trueturn>=2:
                    pos = history[len(history)-3]
                    if history[len(history)-2] == 'EDIT':
                        sys.stdout.shell.write('\n' + '\n    Edit reversed')
                    else:
                        turn-=2
                    history.remove(history[len(history)-1])
                    history.remove(history[len(history)-1])
                    trueturn-=2

                    sys.stdout.shell.write('\n') 
                    if turn>1:
                        sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn)/2)) + '\n')
                    else:
                        sys.stdout.shell.write('\n' + '\n    Human vs Level ' + str(x+1) + ' Computer\n    Again...\n')
                    print_pos(pos)
                
                elif str(user).upper() == 'EDIT':
                    match = re.match('([a-h][1-8])', input('    Square\n    '))
                    if match:
                        editsquare = parse(match.group(1))
                        if editsquare == 'e1':
                            pos.wc = (False, False)
                        elif editsquare == 'e8':
                            pos.bc = (False, False)
                        elif editsquare == 'a1':
                            pos.wc[1] = False
                        elif editsquare == 'h1':
                            pos.wc[0] = False
                        elif editsquare == 'a8':
                            pos.bc[1] = False
                        elif editsquare == 'h8':
                            pos.bc[0] = False
                        user2 = input('    Piece: p, n, b, r, q, k, P, N, B, R, Q, K \n    (or period for an empty square)\n    ')
                        if editsquare>=22 and editsquare<=99 and str(user2).upper() in ['P','N','B','R','Q','K'] or str(user2) == '.':
                            board = list(pos.board)
                            board[editsquare] = user2
                            pos = Position("".join(board), pos.score, pos.wc, pos.bc, pos.ep, pos.kp)
                            if turn>1:
                                sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn)/2)) + '(edited)\n')
                            else:
                                sys.stdout.shell.write('\n' + '\n    Human vs Level ' + str(x+1) + ' Computer (edited)\n')
                            print_pos(pos)
                            trueturn+=2
                            history.append('EDIT')
                            history.append(pos)
                elif str(user).upper() == 'TAKE OVER' or str(user).upper() == 'TAKEOVER':
                    play4 = True
                    while play4 == True:
                        y = input('\n\n    AI strength\n    ')
                        if y in ['1','2','3','4','5','6','7','8','9','10']:
                            play4 = False
                            run(int(y)-1,x,pos,turn,1,history)
                            TO = True
                            break
                        elif y.upper() == 'CANCEL':
                            play4 = False
                            break
                        else:
                            sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')
                      
                elif str(user).upper() == 'SWITCH':
                    playBlack(x,pos,turn,trueturn,history)
                    break
                elif str(user).upper() == 'RESIGN':
                    sys.stdout.shell.write('\n' + '\n    I accept your resignation, thank you')
                elif str(user).upper() == 'OFFER DRAW' or str(user).upper() =='DRAW':
                    move, score = searcher.search(pos.rotate(), secs = x)
                    if score < -100:
                        sys.stdout.shell.write('\n' + '\n    I accept your draw, thank you')
                        break
                    else:
                        sys.stdout.shell.write('\n' + '\n    I would like to play a little bit longer!')
                        move = None
                
                else:
                    match = re.match('([a-h][1-8])'*2, user)
                    
                    if match:
                        move = parse(match.group(1)), parse(match.group(2))
                        if incheck(pos.move(move).rotate()) == 1:
                            move = None
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                        elif move not in pos.gen_moves():
                            move = None
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                        elif pos.board[move[0]].islower():
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                            move = None
                        elif pos.board[move[0]] == '.':
                            move = None
                            sys.stdout.shell.write("    Illegal move", "ERROR")
                    else:
                        sys.stdout.shell.write("    Please enter a move like g8f6", "ERROR")
            if OM == True:
                sys.stdout.shell.write('\n' + '\n')
                print_pos(Outstanding)
                sys.stdout.shell.write('\n' + '\n')
                break
            pos = pos.move(move)
            
            history.append(pos)
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n') 
            sys.stdout.shell.write('\n' + '\n    White Move ' + str(int((turn+1)/2)) + '\n', 'KEYWORD')
            print_pos(pos.rotate())
            if pos.score == -MATE_UPPER or gg == 1:
                r = 0
                for i in pos.gen_moves():
                    if incheck(pos.move(i).rotate()) != 1:
                        r = 1
                if r == 0 and incheck(pos) == 1:
                    sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                    TO = True
                    break
                elif r == 0:
                    sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                    TO = True
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n\n    I resign')
                    TO = True
                    break
            k = []
            for i in range(len(history)-1):
                if history[i] == pos:    
                    k.append(i)
            if len(k) == 3:
                sys.stdout.shell.write('\n' + '\n\n    Draw')
                break
                
            turn+=1
            trueturn+=1

    
       


def playBlack(x, pos, turn, trueturn,h):
    TO = False
    OM = False
    searcher = Searcher()
    history = h
    history.append(pos)
    sys.stdout.shell.write('\n') 
    sys.stdout.shell.write('\n' + '\n    Level ' + str(x+1) + ' Computer vs Human\n')
    sys.stdout.shell.write('\n') 
    check = 0
    print_pos2(pos.rotate())
    pst = deepcopy(pstw)
    while True:
        gg = 0
        if TO == True:
            break
        move, score = searcher.search(pos, secs=3*check+x)
        movehistory = move
        if score == -MATE_UPPER:
            sys.stdout.shell.write('\n' + "\n\n    I resign")
            break
        pos = pos.move(move)
        saved = 0
        check = 0
        sys.stdout.shell.write('\n') 
        if letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e1c1' and pos.wc[1] == True:
            a = sys.stdout.shell.write("\n\n\n    Jit's move: 0-0-0",'DEFINITION')
        elif letters[8-move[0]%10] + str(int(move[0]/10-1)) + letters[8-move[1]%10] + str(int(move[1]/10-1)) == 'e1g1' and pos.wc[0] == True:
            a = sys.stdout.shell.write("\n\n\n    Jit's move: 0-0",'DEFINITION')
        else:
            a = sys.stdout.shell.write("\n\n\n    Jit's move: " + letters[move[0]%10-1] + str(int(11-move[0]/10)) + letters[move[1]%10-1] + str(int(11-move[1]/10)),'DEFINITION')
        for h in range(len(pos.board)-1):
            if pos.board[h].upper() == 'K':
                saved = h
            for i in pos.rotate().gen_moves():
                if pos.rotate().move(i).board[saved].lower() in letters2:
                    check = 1
        if check == 1:
            a = sys.stdout.shell.write('+', 'DEFINITION')
        if score == MATE_UPPER:
            a = sys.stdout.shell.write('+', 'DEFINITION')
            gg = 1
        history.append(pos)
        sys.stdout.shell.write('\n') 
        sys.stdout.shell.write('\n' + '\n    White Move ' + str(int((turn+1)/2)) + '\n', 'KEYWORD')
        print_pos2(pos)
        k = []
        for i in range(len(history)-1):
            if history[i] == pos:    
                k.append(i)
        if len(k) == 3:
            sys.stdout.shell.write('\n' + '\n\n    Draw')
            break
        if pos.score == -MATE_UPPER or gg == 1:
            r = 0
            for i in pos.gen_moves():
                if incheck(pos.move(i).rotate()) != 1:
                    r = 1
            if r == 0 and incheck(pos) == 1:
                sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                break
            elif r == 0:
                sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                break

        turn+=1
        trueturn+=1


        move = None
        
        while move not in pos.gen_moves():
            if TO == True:
                break
            user = input('\n\n    Your move: ')
            if str(user) == 'no u':
                sys.stdout.shell.write('\n' + '\n\n    Outstanding move!')
                OM = True
                TO = True
                break
            elif str(user).upper() == 'UNDO' and trueturn>=2:
                pos = history[len(history)-3]
                if history[len(history)-2] == 'EDIT':
                    sys.stdout.shell.write('\n' + '\n    Edit reversed')
                else:
                    turn-=2
                history.remove(history[len(history)-1])
                history.remove(history[len(history)-1])
                trueturn-=2
                sys.stdout.shell.write('\n') 
                sys.stdout.shell.write('\n' + '\n    White Move ' + str(int((turn)/2)) + '\n', 'KEYWORD')
                print_pos2(pos)
            elif str(user).upper() == 'EDIT':
                match = re.match('([a-h][1-8])', input('    Square\n    '))
                if match:
                    editsquare = 119-parse(match.group(1))
                    if editsquare == 'e1':
                        pos.wc = (False, False)
                    elif editsquare == 'e8':
                        pos.bc = (False, False)
                    elif editsquare == 'a1':
                        pos.wc[1] = False
                    elif editsquare == 'h1':
                        pos.wc[0] = False
                    elif editsquare == 'a8':
                        pos.bc[1] = False
                    elif editsquare == 'h8':
                        pos.bc[0] = False
                    user2 = input('    Piece: p, n, b, r, q, k, P, N, B, R, Q, K \n    (or period for an empty square)\n    ')
                    if editsquare>=22 and editsquare<=99 and str(user2).upper() in ['P','N','B','R','Q','K'] or str(user2) == '.':
                        board = list(pos.board)
                        board[editsquare] = user2
                        pos = Position("".join(board), pos.score, pos.wc, pos.bc, pos.ep, pos.kp)
                        sys.stdout.shell.write('\n' + '\n    White Move ' + str(int((turn+1)/2)) + '(edited)\n', 'KEYWORD')
                        print_pos2(pos)
                        trueturn+=2
                        history.append('EDIT')
                        history.append(pos)
            elif str(user).upper() == 'TAKE OVER' or str(user).upper() == 'TAKEOVER':
                play4 = True
                while play4 == True:
                    y = input('\n\n    AI strength\n    ')
                    if y in ['1','2','3','4','5','6','7','8','9','10']:
                        play4 = False
                        run(x,int(y)-1,pos,turn,2,history)
                        TO = True
                        break
                    elif y.upper() == 'CANCEL':
                        play4 = False
                    else:
                        sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')
            elif str(user).upper() == 'SWITCH':
                playWhite(x,pos,turn,trueturn,2,history)
                break
            elif str(user).upper() == 'RESIGN':
                sys.stdout.shell.write('\n' + '\n    I accept your resignation, thank you')
            elif str(user).upper() == 'OFFER DRAW' or str(user).upper() =='DRAW':
                move, score = searcher.search(pos.rotate(), secs = x)
                if score < -100:
                    sys.stdout.shell.write('\n' + '\n    I accept your draw, thank you')
                    break
                else:
                    sys.stdout.shell.write('\n' + '\n    I would like to play a little bit longer!')
                    move = None
            elif str(user) == '0-0':
                move = 119-parse('e8'), 119-parse('g8')
            elif str(user) == '0-0-0':
                move = 119-parse('e8'), 119-parse('c8')
            else:
                match = re.match('([a-h][1-8])'*2, user)
                
                if match:
                    move = 119-parse(match.group(1)), 119-parse(match.group(2))
                    if incheck(pos.move(move).rotate()) == 1:
                        move = None
                        sys.stdout.shell.write("    Illegal move", "ERROR")
                    elif move not in pos.gen_moves():
                        move = None
                        sys.stdout.shell.write("    Illegal move", "ERROR")
                    elif pos.board[move[0]].islower():
                        sys.stdout.shell.write("    Illegal move", "ERROR")
                        move = None
                    elif pos.board[move[0]] == '.':
                        move = None
                        sys.stdout.shell.write("    Illegal move", "ERROR")
                else:
                    sys.stdout.shell.write("    Please enter a move like g8f6", "ERROR")
        if OM == True:
            sys.stdout.shell.write('\n' + '\n')
            print_pos2(Outstanding)
            sys.stdout.shell.write('\n' + '\n')
            break
        pos = pos.move(move)
        history.append(pos)
        sys.stdout.shell.write('\n') 
        sys.stdout.shell.write('\n') 
        sys.stdout.shell.write('\n' + '\n    Black Move ' + str(int((turn+1)/2)) + '\n')
        print_pos2(pos.rotate())
        k = []
        for i in range(len(history)-1):
            if history[i] == pos:    
                k.append(i)
        if len(k) == 3:
            sys.stdout.shell.write('\n' + '\n\n    Draw')
            break
        if pos.score == -MATE_UPPER or gg == 1:
            r = 0
            for i in pos.gen_moves():
                if incheck(pos.move(i).rotate()) != 1:
                    r = 1
            if r == 0 and incheck(pos) == 1:
                sys.stdout.shell.write('\n' + "\n\n    Checkmate!")
                TO = True
                break
            elif r == 0:
                sys.stdout.shell.write('\n' + '\n\n    Stalemate')
                TO = True
                break
            else:
                sys.stdout.shell.write('\n' + '\n\n    I resign')
                TO = True
                break
                
        turn+=1
        trueturn+=1

play = True
starter = Position(initial, 0, (True,True), (True,True), 0, 0)
Outstanding = Position(OutstandingMove, 0, (True,True), (False,False), 0, 0)
letters2 = ['p', 'n', 'b', 'r', 'q']
pst = deepcopy(pstw)
history = []
for i in range(50):
    sys.stdout.shell.write('\n') 
new = input('                   Press ENTER\n    ')
for i in range(50):
    sys.stdout.shell.write('\n') 
if new != 'skip':
    sys.stdout.shell.write('\n' + "                  =====   =====   =====")
    time.sleep(0.5)
    for i in range(2):
        sys.stdout.shell.write('\n' + "                    =       =       =  ")
        time.sleep(0.5)
    sys.stdout.shell.write('\n' + "                  = =       =       =  ")
    time.sleep(0.5)
    sys.stdout.shell.write('\n' + "                  ===  @  =====  @  =  ")
    time.sleep(0.5)
    for i in range(2):
        sys.stdout.shell.write('\n') 
    time.sleep(1)
    sys.stdout.shell.write('\n' + "    =====   =   =   =====   =====   =====               ")
    time.sleep(0.5)
    sys.stdout.shell.write('\n' + "    =       =   =   =       =       =                   ")
    time.sleep(0.5)
    sys.stdout.shell.write('\n' + "    =       =====   =====   =====   =====         __  /|")
    time.sleep(0.5)
    sys.stdout.shell.write('\n' + "    =       =   =   =           =       =   \  / |  |  |")
    time.sleep(0.5)
    sys.stdout.shell.write('\n' + "    =====   =   =   =====   =====   =====    \/  |__|@ |")
    time.sleep(0.5)
    sys.stdout.shell.write('\n' + '\n')
    sys.stdout.shell.write('\n' + "    Welcome to the Jit chess engine (it stands for J I T)")
    sys.stdout.shell.write('\n' + "                     By Soren Choi\n")
    sys.stdout.shell.write('\n' + "          With special thanks to Jit Shetty\n\n")
    time.sleep(2)
    input("                  Press ENTER to start               \n")
    time.sleep(2)
gg = 0
while play == True:
    play2 = True
    if new!='skip':
        for i in range(50):
            sys.stdout.shell.write('\n') 
        print_pos3(starter)
        for i in range(5):
            sys.stdout.shell.write('\n') 
            time.sleep(0.25)
    i1 = input('\n    1 to watch JIT play itself, 2 to play as White,\n    3 to play as Black or type HELP for instructions\n    ')
    if str(i1).upper() == 'HELP':
        helper = True
        for i in range(25):
            print()
        while helper == True:
            Q = str(input('\n    Type PLAY for instructions on how to play against JIT.\n    Type ABOUT for more information about JIT.\n    Type BACK to leave the help menu.\n    '))
            if Q.upper() == 'PLAY':
                for i in range(25):
                    print()
                playhelp = True
                while playhelp == True:
                    R = str(input("\n    Entering moves:\n    To enter a move, type the square the piece is currently on,\n    followed by the square the piece is moving to.\n\n    Castling:\n    Type 0-0 to castle kingside, and 0-0-0 to castle queenside.\n    Word of warning: if you castle through or out of check,\n    JIT will punish you your transgressions and take your king.\n\n    Undoing moves:\n    If you have made an unintentional move, type UNDO to go back\n    to your previous move.\n    This will also undo JIT's move.\n\n    Resigning:\n    Type RESIGN to give up.\n\n    Skipping the start animation:\n    In future, you can type SKIP when the screen reads 'Press ENTER'\n    to skip the beginning animation.\n\n    Type ADVANCED to see advanced features, or BACK to go back\n    to the help screen.\n    "))
                    if R.upper() == 'ADVANCED':
                        for i in range(25):
                            print()
                        S = str(input("\n    Editing the board:\n    To enter the editing tool, type EDIT. JIT will then prompt you to pick a square \n    to edit. You can then place a piece here by typing the corresponding\n    letter(p, n, b, r, q, k - capital for your color and lowercase for JIT's).\n    You can also remove a piece or leave a square blank by typing a period.\n    JIT will not look. \n\n    Offering draws:\n    Type OFFER DRAW or DRAW to offer a draw. If you are resorting to this, it is\n    highly doubtful that JIT will agree, because he is not a dumbass and can\n    see through your stupid ploys.\n\n    Switching colors:\n    To switch colors, type SWITCH. Filthy traitor.\n\n    Handing over:\n    To have JIT take over for you, type TAKEOVER. JIT will\n    ask you what strength to play at. Pick a number between 1 and 10. If\n    you want, you can type CANCEL to cancel this.\n\n    Press ENTER to leave this screen.\n    "))
                        if S.lower() == 'cheat':
                            for i in range(25):
                                print()
                            input("\n    Type 'a1d5' to automatically win.\n\n    Press ENTER to leave this screen.\n    ")
                            for i in range(25):
                                print()
                        playhelp = False    
                    elif R.upper() == 'BACK':
                        for i in range(25):
                            print()
                        playhelp = False
                    else:
                        for i in range(25):
                            print()
                        sys.stdout.shell.write("\n    Congratulations. You win")
                        time.sleep(1)
                        sys.stdout.shell.write(" a free copy of KNACK!")
                        time.sleep(1)
                        sys.stdout.shell.write("\n\n    To claim your prize, enter your credit card number, the 3 digits on the back\n    and the expiration date!(Error)\n    ")
                        time.sleep(4)
                        for i in range(25):
                            print()
            elif Q.upper() == 'ABOUT':
                abouthelp = True
                for i in range(25):
                    print()
                while abouthelp == True:
                    T = str(input("\n    This program was made by Soren Choi with literary assistance from Rishi Sharma\n    because Soren got a B in English, technical assistance from Will Ching \n    and Straight Will.  This was inspired by JIT.\n\n    Owen did literally nothing to help.\n\n    Type BACK to return to the help menu.\n    "))
                    if T.upper() != 'BACK':
                        for i in range(25):
                            print()
                        sys.stdout.shell.write("\n    How damn hard can it be to type BACK??\n    You're a whole new level of dumbfuck(Error)\n    ")
                        time.sleep(5)
                        for i in range(25):
                            print()
                    else:
                        abouthelp = False
            elif Q.upper() == 'BACK':
                helper = False
                break
            else:
                for i in range(25):
                    print()
                sys.stdout.shell.write("\n    Mission Failed, we'll get 'em next time!(Error)\n    ")
                time.sleep(5)
                for i in range(25):
                    print()
    elif i1 in ['1','2','3']:
        i1 = int(i1)
        if i1 == 1:
            play3 = True
            while play2 == True:
                m = input('\n    White AI strength\n    ')
                if m in ['1','2','3','4','5','6','7','8','9','10']:
                    m = int(m)-1
                    while play3 == True:
                        n = input('\n    Black AI strength\n    ')
                        if n in ['1','2','3','4','5','6','7','8','9','10']:
                            n = int(n)-1
                            gg = 0
                            run(m,n,starter,1,1,history)
                            play2 = False
                            play3 = False
                            if str(input('\n    New game?\n    ')).lower() == 'no':
                                play = False
                        else:
                            sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')
                else:
                    sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')

        elif i1 == 2:
            while play2 == True:
                n = input('\n    AI strength\n    ')
                if n in ['1','2','3','4','5','6','7','8','9','10']:
                    n = int(n)-1
                    gg = 0
                    playWhite(n,starter,1,1,1,history)
                    play2 = False
                    if str(input('\n    New game?\n    ')).lower() == 'no':
                        play = False
                else:
                    sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')

        elif i1 == 3:
            while play2 == True:
                n = input('\n    AI strength\n    ')
                if n in ['1','2','3','4','5','6','7','8','9','10']:
                    n = int(n)-1
                    gg = 0
                    playBlack(n,starter,1,1,history)
                    play2 = False
                    if str(input('\n    New game?\n    ')).lower() == 'no':
                        play = False
                else:
                    sys.stdout.shell.write('\n' + '    Please enter an integer (1-10)')
    else:
        for i in range(25):
            print()
        sys.stdout.shell.write('\n' + '    Please enter 1, 2, 3 or HELP')
        time.sleep(3)
        for i in range(5):
            print()
