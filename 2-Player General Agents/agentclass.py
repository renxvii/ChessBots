from gameclass import Game
from copy import deepcopy
import math
import random
import time

class Agent:    
    def turn(self, Game:Game):
        pass
    
    def __init__(self):
        self.player = 1

class Minimax(Agent):
    def maxi(self, Game: Game, depth: int, alpha, beta):
        if Game.checkwinner(Game.state) != 0 or depth < 0:
            return [Game.state, Game.valuation(Game.state)]
        alpha = deepcopy(alpha)
        moveset = Game.valid_moves()
        if moveset == []:
            return [None, 0]
        newGame = deepcopy(Game)
        newGame.turn *= -1
        newGame.thinking = True
        best = [None,-10000]
        random.shuffle(moveset)
        for move in moveset:
            newGame.state = move[0]
            move[1] = self.mini(newGame, depth - 1, alpha, beta)[1]
            if best[1] <= move[1]:
                best = move
            alpha = max(alpha, best[1])
            if beta < alpha:
                return best  # Alpha cutoff
        return best

    def mini(self, Game: Game, depth: int, alpha, beta):
        if Game.checkwinner(Game.state) != 0 or depth < 0:
            return [Game.state, Game.valuation(Game.state)]
        beta = deepcopy(beta)
        moveset = Game.valid_moves()
        if moveset == []:
            return [None, 0]
        newGame = deepcopy(Game)
        newGame.turn *= -1
        newGame.thinking = True
        worst = [None, 10000]
        random.shuffle(moveset)
        for move in moveset:
            newGame.state = move[0]
            move[1] = self.maxi(newGame, depth - 1, alpha, beta)[1]
            if worst[1] >= move[1]:
                worst = move
            beta = min(beta, worst[1])
            if beta < alpha:
                return worst  # Alpha cutoff
        return worst


    def turn(self, Game: Game):
        move = []
        if self.player == 1:
            move = self.maxi(Game, self.depth, float('-inf'), float('inf'))
        else:
            move = self.mini(Game, self.depth, float('-inf'), float('inf'))
        Game.play(move)

    def __init__(self, depth: int):
        self.depth = depth-1
        self.player = 1
        
    
class Player(Agent):
    def turn(self, Game:Game):
        Game.end = Game.checkwinner()
        if Game.end == 0:
            Game.playermove(input())
        else:
            print("winner: " + str(int((1 - Game.end)/2 + 1)))
    
    def __init__(self):
        self.player = 1

class Random(Agent):
    def turn(self, Game:Game):
        try:
            x = random.choice(Game.valid_moves())
        except:
            x = [None, -9999*self.player]
        Game.play(x)
    
    def __init__(self):
        self.player = 1


class MCTSNode:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.game.valid_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
                (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits)) if child.visits != 0 else self.wins/self.visits if self.visits != 0 else 0
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def rollout_policy(self, possible_moves):
        return random.choice(possible_moves)

    def expand(self):
        random.shuffle(self.untried_moves)
        move = self.untried_moves.pop()
        next_game = deepcopy(self.game)
        next_game.state = move[0]
        next_game.value = move[1]
        next_game.turn *= -1
        child_node = MCTSNode(next_game, parent=self, move=move)
        self.children.append(child_node)
        return child_node


class MCTS:
    def __init__(self, player, root_game, iteration_limit=1000, movemax=20):
        self.root = MCTSNode(root_game)
        self.player = player
        self.iteration_limit = iteration_limit
        self.movemax = movemax

    def select_node(self):
        current_node = self.root
        while current_node.is_fully_expanded():
            if current_node.children:
                current_node = current_node.best_child()
            else:
                # If the node has no children, it's a leaf node
                break
        if not current_node.is_fully_expanded():
            # Expand the current node if it's not fully expanded
            return current_node.expand()
        return current_node

    def run_search(self):
        for _ in range(self.iteration_limit):
            selected_node = self.select_node()
            result = self.simulate_game(selected_node.game)
            self.backpropagate(selected_node, result)

    def simulate_game(self, game):
        sim = deepcopy(game)
        sim.players = [Random(), Random()]
        sim.thinking = True
        movecount = 0
        while sim.end == 0:
            movecount+=1
            sim.next()
            if movecount >= self.movemax:
                v = sim.valuation()
                sim.end = -1 if v < 0 else 1 if v > 0 else 2
        
        if sim.end == 2:
            return 0
        else:
            return sim.end

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            if node.game.turn != result:
                node.wins += 1
            node = node.parent

    def best_move(self):
        if len(self.root.children) == 0:
            return [None, -9999*self.player]
        return self.root.best_child(c_param=0).move



class MCTSAgent(Agent):
    def __init__(self, iteration_limit=1000, movemax = 20):
        super().__init__()
        self.iteration_limit = iteration_limit
        self.movemax = movemax

    def turn(self, game):
        mcts = MCTS(self.player, deepcopy(game), iteration_limit=self.iteration_limit, movemax=self.movemax)
        mcts.run_search()
        best_move = mcts.best_move()
        game.play(best_move)

