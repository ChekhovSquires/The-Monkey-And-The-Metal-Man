import random 
class HBDagent:
    def __init__(self,*args):
        print(args)
    def step(self,state):
        vals = [[0,1],[0,-1],[1,0],[-1,0]]
        spotter_moves = [random.choice(vals),random.choice(vals)]
        spotter_direction = random.choice(vals)
        assasin_moves = [random.choice(vals),random.choice(vals),random.choice(vals),random.choice(vals)]
        assasin_direction = random.choice(vals)
        print({
            "Spotter":{
                "direction":spotter_direction, # or [-1,0],[0,1],[0,-1]
                "moves":spotter_moves # max length 2, 
                # if you input more than 2, truncated to first 2
                # if you dont input any, no move made
                # input [1,0] makes the bot move from (x,y) to (x+1,y)
                # other inputs include [-1,0],[0,1],[0,-1]
                # if you hit a wall/ edge of the map, that move is ignored and one of your 2 moves is used up
                # landing on an opponent kills them
            },
            "Assasin":{
                "direction":assasin_direction, # or [-1,0],[0,1],[0,-1]
                "moves":assasin_moves # max length 4, 
                # if you input more than 4, truncated to first 4
                # if you dont input any, no move made
                # input [1,0] makes the bot move from (x,y) to (x+1,y)
                # other inputs include [-1,0],[0,1],[0,-1]
                # if you hit a wall/ edge of the map, that move is ignored and one of your 4 moves is used up
                # landing on an opponent kills them
            }
        })
        return {
            "Spotter":{
                "direction":spotter_direction, # or [-1,0],[0,1],[0,-1]
                "moves":spotter_moves # max length 2, 
                # if you input more than 2, truncated to first 2
                # if you dont input any, no move made
                # input [1,0] makes the bot move from (x,y) to (x+1,y)
                # other inputs include [-1,0],[0,1],[0,-1]
                # if you hit a wall/ edge of the map, that move is ignored and one of your 2 moves is used up
                # landing on an opponent kills them
            },
            "Assasin":{
                "direction":assasin_direction, # or [-1,0],[0,1],[0,-1]
                "moves":assasin_moves # max length 4, 
                # if you input more than 4, truncated to first 4
                # if you dont input any, no move made
                # input [1,0] makes the bot move from (x,y) to (x+1,y)
                # other inputs include [-1,0],[0,1],[0,-1]
                # if you hit a wall/ edge of the map, that move is ignored and one of your 4 moves is used up
                # landing on an opponent kills them
            },
            "Debug":"ASdasdasdas"
        }