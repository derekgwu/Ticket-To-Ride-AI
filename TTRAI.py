import TTRGameSim
import TTRPlayer
import TTRPrint
import TTRBoard
import copy
import random 
class MTNode:
    def __init__(self, observation, move, parent):
        self.children = []
        self.state = observation
        self.move = move
        self.parent = parent
        self.visit_count = 0
        self.value = 0
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
    def monteCarlo(self, player, depth):
        state = self.game.getObservations(player)
        self.root = MTNode(state, None, None)

        #build out the tree
        for i in range (0, 10):
            self.simulate(state, depth, self.root)
        
        #do a 1-layer bfs to find the best score move

    def simulate(self,depth,root):
        #reached depth cutoff
        if depth == 0:
            return 0
        
        #unexplored node, expand it
        if len(root.children) == False:
            for action in self.game.getLegalActions(root.state['player']):
                #make a new copy of the state to prevent overwrriting
                
                new_state = self.makeStateCopy(root.state)
                

                #if the action is a place train down
                if action['move'] == 'train':
                    print("action")
                    city1 =action['edge']['edge'][0]
                    city2 =action['edge']['edge'][1]
                    routeDist =action['edge']['weight']

                    #right now get random valid coloring
                    color = random.choice(action['possible_cards'])
                    
                    keys = color.keys()
                    choice = None
                    for key in keys:
                        if key != 'wild':
                            choice = key
                        
                    # add the edge to the board
                    new_state['player'].playerBoard.addEdge(city1, city2, routeDist, choice)

                    #remove the cards
                    for card, count in color.items():
                        new_state['player'].removeCardsFromHand(card, count)


                    #add points
                    new_state['player'].addPoints(self.game.routeValues[routeDist])
                    
                    #the player's theorectical points for entering this state
                    print(self.game.getReward(new_state['player']))
        
           

                #if the action is draw a card
                elif action['move'] == 'card':
                    new_state['player'].hand[action['card']] += 1
        
                
                #if the action is pick up a destination ticket
                else:
                    new_state['player'].addTicket(action['ticket'])
                
                root.children.append(MTNode(self.game.getObservation(new_state['player']), action, root))
            return self.rollout(root, depth)
        
        #compute UCT value for each next action, pick the action with the highest UCT

        #take the action, generate a new observcation after taking that step

        #q = simulate(new state, depth - 1)

        #root.vist += 1

        #root.value += q

        #return q
        
        return self.game.getReward(root.state['player'])
    
    def rollout(self, root, depth):
        if depth == 0:
            return 
        
        #pick a random next legal action; note it'll probably be a different person
        node = random.choice(root.children)


        #create a node and add to the tree

        #recurse


    
        
        pass

    def makeStateCopy(self, state):
        player = TTRPlayer.Player(
                    copy.deepcopy(state['player'].getHand()),
                    copy.deepcopy(state['player'].getTickets()),
                    copy.deepcopy(state['player'].playerBoard),
                    state['player'].playerPosition,
                    state['player'].getNumTrains(),
                    state['player'].isAi()
                )
        edges = copy.deepcopy(state['edges'])
        draw_pile = copy.deepcopy(state['draw_pile'].copy())
        player_info = copy.deepcopy(state['public_player_info'])
        return {
            'edges' : edges,
            'player' : player,
            'draw_pile' : draw_pile,
            'public_player_info' : player_info,
        }