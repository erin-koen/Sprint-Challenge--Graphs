from world import World
from room import Room
from player import Player
from queue import Queue
import random

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.

# roomGraph={0: [(3, 5), {'n': 1}], 1: [(3, 6), {'s': 0, 'n': 2}], 2: [(3, 7), {'s': 1}]}
roomGraph={0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}], 1: [(3, 6), {'s': 0, 'n': 2}], 2: [(3, 7), {'s': 1}], 3: [(4, 5), {'w': 0, 'e': 4}], 4: [(5, 5), {'w': 3}], 5: [(3, 4), {'n': 0, 's': 6}], 6: [(3, 3), {'n': 5}], 7: [(2, 5), {'w': 8, 'e': 0}], 8: [(1, 5), {'e': 7}]}

world.loadGraph(roomGraph)
world.printRooms()
player = Player("Name", world.startingRoom)

# create a class with which to track progress of player's DFT. When player hits a dead end, perform BFT on instance of Graph_Rooms to find shortest path back to unexplored territory.

class Graph_Rooms:
    def __init__(self):
        self.rooms:{}
    def add_room(self, room):
        self.rooms[room] = set()
    def add_connection(self, room, direction):
        direction_dict = {direction: room}
        self.rooms[room].add_connection(direction_dict)
        
    def bft(self, room):
        q = Queue()
        q.put([room])
        while q.empty() is False:
            path = q.get()
            v = path[-1]
            # will need to do a little bit of debugging here wrt what's being passed
            for neighbor in self.rooms[v]:
                if neighbor is not "?":
                    path_copy = list(path)
                    path_copy.append(neighbor)
                    q.put(path_copy)
                else: 
                    return path

# instantiate a Graph of rooms visited
tracker = Graph_Rooms()

# FILL THIS IN
traversalPath = []

# use player to travel through rooms and build graph. Start the player at room 0. 
player.currentRoom = 0

# when there as many room dictionaries in the tracker as there are in the room graph, it means we've touched every room
while len(tracker.rooms) < len(roomGraph):

    # add current room to tracker
    tracker.add_room(player.currentRoom)
    
    
    # get available exits, add connections to tracker as '?'
    exits = player.currentRoom.getExits()
    
    # if no available exits, run BFT, follow path to get back to an undiscovered
    if len(exits) == 0:
        path_back = tracker.bft(player.currentRoom)
        for direction in path_back:
            traversalPath.append(direction)
            player.travel(direction)
    # otherwise
    else:

        # add all connections as question marks
        for e in exits:
            tracker.add_connection('?', e)
        
        # choose one at random (by generating a random integer between 0  and the last index in exits)
        direction = exits[random.randint(0,len(exits)-1)]
        # add it to the traversal path
        traversalPath.append(direction)
        # save current room as a variable to update connection after move
        prev_room = player.currentRoom
        
        # save the opposite direction to update the new room after the move
        opp_dir = opposite_direction(direction)
        
        # send player in that direction, player.room updates accordingly.
        player.travel(direction)
        
        # update connections
        tracker.rooms[prev_room].direction = player.currentRoom
        tracker.rooms[player.currentRoom].opp_dir = prev_room
    
        
def opposite_direction(dir):
    if dir == 'e':
        return 'w'
    if dir == 'w':
        return 'e'
    if dir == 's':
        return 'n'
    if dir == 'n':
        return 's'


# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######

# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")