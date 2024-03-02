from gameclass import Chess
from agentclass import Minimax, Player, MCTSAgent, Random
Agents = [Minimax(1), Minimax(2), Random(), MCTSAgent(iteration_limit=300, movemax = 10), MCTSAgent(iteration_limit=200, movemax = 20), MCTSAgent(iteration_limit=100, movemax=30)]
for i in range(len(Agents)):
    Chess(Agents[i], Player())
    Chess(Player(), Agents[i])
