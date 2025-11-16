# State Specification

## Description of State Space
  In Ticket to Ride, a game state captures information about every player’s cards and trains, and the board itself. The board has vertices and edges, represented as city destinations and train routes, respectively. Every train route has two destinations it connects, the color and player association of the route, and the length of the route. The state also contains information about each player’s possessions. At any time in the game, a player can have trains of varying colors to place on the board and different destination tickets. 
	The state space of Ticket to Ride is the set of all possible states. In other words, it is the set of all possible information combinations about the board and player-specific information. With over 140 cards and 30 destination vertices, it is evident that this state space cannot be searched using a simple breadth-first search or A* search. We can also express the state space in mathematical notation.

As mentioned above, the state space of Ticket to Ride consists of the board state, the cards in players' hands, and the current face-up train cards.

### Players
$P = \{ P_1, P_2, \ldots, P_k \}$

### Colors
$c = \{ \text{Purple}, \text{White}, \text{Blue}, \text{Yellow}, \text{Orange}, \text{Black}, \text{Red}, \text{Green} \}$

### Cities
$C = \{ C_{ny}, C_{la}, C_{ph}, \ldots, C_{j} \}$

### Edges
Edges are unordered pairs of distinct cities:
$E = \{ (C_i, C_j) \mid C_i, C_j \in C,\ i \neq j \}$

Each edge $e \in E$ is defined by the functions:

- Weight (number of trains required):
  $$w : E \to \mathbb{N}$$

- Color of the route:
  $$c : E \to c$$

- Player assignment (or unclaimed):
  $$p : E \to P \cup \{ \varnothing \}$$

### Board
The board is the set of all edges with attributes:
$$B = \{ (e, w(e), c(e), p(e)) \mid e \in E \}$$

## Observability
This is a partially observable state space, as a player, or the agent, cannot fully observe the entire state space. As mentioned above, a player only has access to their own destination tickets and train cars. An agent cannot observe other players or agents tickets and cars, which means no agent has access to the full state space. This means the state space is partially observable.
