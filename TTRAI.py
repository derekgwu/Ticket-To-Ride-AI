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

    def search(self, state):
        return False


    #searches the tree for a state
    def dfs(self, state):
        
        if self.compareStates(self.state, state):
            return True
        
        if len(self.children) == 0:
            
            return False

  
        for child in self.children:
            if child.dfs(state) == True:
                return True
        return False

    def compareStates(self, state1, state2):
        
        for edge1 in state1['edges']:
            found = False
            for edge2 in state2['edges']:
                if edge1 == edge2:
                    found = True
            if not found:
                return False
        
        if state1['draw_pile'] != state2['draw_pile']:
            return False
        
 
         
        return True
    

class AI:

    def __init__(self, game, board):
        self.root = None
        self.game = game
        self.board = board
    
    #state will be represented as a player
    def monteCarlo(self, player, depth):
        state = self.game.getObservations(player)

        #state of hte game when AI is called
        self.root = MTNode(state, None, None)
       

        #build out the tree
        for i in range (0, 1000):
            self.simulate(state, depth, self.root)
        
        #do a 1-layer bfs to find the best score move
        if not self.root.children:
            #no legal actions
            return None

        best_child = max(self.root.children, key=lambda c: c.value)
        best_action = best_child.move

        print(f"the best action is {best_action}")
        return best_action

    def simulate(self,state, depth,root):
        #reached depth cutoff
        if depth == 0:
            return 0
        
        #unexplored node, expansion
        if len(root.children) < len(self.game.getLegalActions(state['player'])):
            #randomly pick a new move
            next_actions = self.game.getLegalActions(state['player'])
            ##add to the tree
            action = random.choice(next_actions)
#
            new_state = self.makeNextMove(state, action)
            new_node = MTNode(new_state, action, None)
            new_node.parent = root
            
            root.children.append(new_node)


            return self.rollout(new_node, depth, root.state['player'])
        
        #selection - move down the existing tree
        #compute UCT value for each next action, pick the action with the highest UCT
        #for now let's just randomly do it idgaf
        next_node = random.choice(root.children)
        #take the action, generate a new observcation after taking that step
        next_state = next_node.state

        q = self.game.getReward(next_state['player']) + self.simulate(next_state, depth - 1, next_node)

        #backpropagation
        next_node.visit_count += 1

        next_node.value += q

        return q
        
    
    def rollout(self, root, depth, playerToTrack):
        if depth == 0:
            return 0
        
        discount_factor = 1
        
        #pick a random next legal action; note it'll probably be a different person

        #next's person to move
        curr_move = self.game.posToMove
        curr_move += 1
        curr_move %= self.game.numPlayers + self.game.numAi
        next_player = self.game.players[curr_move]

        #generate a random action for them
        next_actions = self.game.getLegalActions(next_player)
        #no more legal moves
        if not next_actions:
            return self.game.getReward(playerToTrack)
        action = random.choice(next_actions)
        state = self.game.getObservations(next_player)

        next_state = self.makeNextMove(state, action)
        return self.game.getReward(playerToTrack) + (discount_factor * self.rollout(next_state, depth - 1, playerToTrack))

    
    def makeNextMove(self, state, action):
        new_state = self.makeStateCopy(state)
    
       #if the action is a place train down
        if action['move'] == 'train':
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
       

            #if the action is draw a card
        elif action['move'] == 'card':
            new_state['player'].hand[action['card']] += 1   
       
            #if the action is pick up a destination ticket
        else:
            new_state['player'].tickets[action['ticket']] = False
        
        return new_state

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
    
    def apply_action(self, player, action):
        #train move
        if action['move'] == 'train':
            edge = action['edge']
            city1, city2 = edge['edge']
            routeDist = edge['weight']

            #choose a card combination
            combo = random.choice(action['possible_cards'])
            #pick a non wild color for the track
            color_choice = 'wild'  # default
            for c in combo.keys():
                if c != 'wild':
                    color_choice = c
                    break

            #claim route on player board
            player.playerBoard.addEdge(city1, city2, routeDist, color_choice)

            #remove route from main board
            self.game.board.removeEdge(city1, city2, color_choice)

            #add points
            player.addPoints(self.game.routeValues[routeDist])

            #remove cards from hand and add to discard
            for c, count in combo.items():
                player.removeCardsFromHand(c, count)
                self.game.deck.addToDiscard([c] * count)

            #remove trains
            player.playNumTrains(routeDist)

        #draw card move
        elif action['move'] == 'card':
            card = action['card']
            if card in self.game.deck.getDrawPile():
                player.addCardToHand(self.game.deck.pickFaceUpCard(card))
            else:
                #draw from face-down pile if all else
                player.addCardToHand(self.game.deck.pickFaceDown())

        #ticket move
        elif action['move'] == 'ticket':
            ticket = action['ticket']
            player.addTicket(ticket)