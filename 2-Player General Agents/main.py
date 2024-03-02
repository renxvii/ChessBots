from gameclass import Connect4, TicTacToe, Checkers, Chess
from agentclass import Minimax, Player, MCTSAgent, Random
Agents = [Minimax(1), Minimax(2), Random(), MCTSAgent(iteration_limit=300, movemax = 10), MCTSAgent(iteration_limit=200, movemax = 20), MCTSAgent(iteration_limit=100, movemax=30)]
Games = [TicTacToe, Connect4, Checkers, Chess]
for game in Games:
    print(game)
    for i in range(len(Agents)):
        for j in range(i):   
            scores = [0,0,0,0]
            for c in range(50):
                print(Agents[i], Agents[j])
                print(scores)
                gameiter = game(Agents[i], Agents[j], render=False)
                scores[gameiter.end] += 1
                gameiter = game(Agents[j], Agents[i], render=False)
                scores[-gameiter.end] += 1
            print(Agents[i], Agents[j])
            print(scores)