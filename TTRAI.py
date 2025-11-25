import TTRGameSim
import TTRPlayer
import TTRPrint
import TTRBoard
class MTNode:
    def __init__(self, player, board, move, observations, parent):
        self.children = []

        self.playerState = player
        self.board = board
        self.observations = 0
        self.move = move
        self.parent = 0
        self.visit_count = 0
        pass

    def search(self, node: "MTNode"):
        return False

    def compareStates(self, state1, state2):
        pass
    

class AI:

    def __init__(self, game, board):
        self.root = None
        self.game = game
        self.board = board
    
    #state will be represented as a player
    def monteCarlo(self, state, depth):
        self.root = MTNode(state, self.board, None, self.game.getObservations(state), None)
        max_score = -99999

        #build out the tree
        for i in range (0, 1000):
            self.simulate(state, depth)
        
        #do a 1-layer bfs to find the best score move

    def simulate(self,state,depth):
        #reached depth cutoff
        if depth == 0:
            return 0
        
        if self.root.search(state) == False:
            for action in self.game.getLegalActions(state):
                #make a new copy of the state to prevent overwrriting
                node_player = state.copy()
                node_board = self.root.board

                if action['move'] == 'train':
                    node_board = self.root.board
                elif action['move'] == 'card':
                    node_player.addCardToHand(action['card'])
                else:
                    node_player.addTicket(action['ticket'])
        return state.getReward()
    
    def rollout():
        pass