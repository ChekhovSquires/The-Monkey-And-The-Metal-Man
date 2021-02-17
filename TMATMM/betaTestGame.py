#!/usr/bin/env python
# Import Modules
import os
import pygame as pg
from pygame.compat import geterror


size = (19,19)
tile_size = 25

rotate = pg.transform.rotate
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def calculateLineOfSightHighground(point):
    points = []
    for x in range(-5,6):
        limit = 5-abs(x)
        for y in range(-limit,limit+1):
            cur_point = (point[0]+x,point[1]+y)
            if checkBounds(cur_point):
                points.append(cur_point)

    return points

def calculateLineOfSightAssasin(board,point,direction):

    # initialising the different directions in consideration
    forward = []
    diagonal_counter_clock =[]
    diagonal_clock = []
    angled_counter_clock =[]
    angled_clock = []

    # check whether the direction being faced is one of the x directions
    if direction[0]:

        # generate the progressive points in the forward and diagonal directions
        forward = [(point[0]+x*direction[0],point[1])for x in range(1,3)]
        diagonal_counter_clock = [(point[0]+x*direction[0],point[1]+x*direction[0]) for x in range(1,2)]
        diagonal_clock = [(point[0]+x*direction[0],point[1]-x*direction[0]) for x in range(1,2)]

        # get all possibly viewable points between the forward line and diagonals

        # generate theses points as slices along the forward direction
        angled_counter_clock = [(point[0]+x*direction[0],point[1]+direction[0]*1)for x in range(2,3)]
        angled_clock = [(point[0]+x*direction[0],point[1]-direction[0]*1)for x in range(2,3)]
    else:
        
        # generate the progressive points in the forward and diagonal directions
        forward = [(point[0],point[1]+x*direction[1])for x in range(1,3)]
        diagonal_counter_clock = [(point[0]+x*direction[1],point[1]+x*direction[1]) for x in range(1,2)]
        diagonal_clock = [(point[0]-x*direction[1],point[1]+x*direction[1]) for x in range(1,2)]
        
        # get all possibly viewable points between the forward line and diagonals

        # generate theses points as slices along the forward direction
        angled_counter_clock = [(point[0]+direction[1]*1,point[1]+x*direction[1])for x in range(2,3)]
        angled_clock = [(point[0]-direction[1]*1,point[1]+x*direction[1])for x in range(2,3)]

    boundary = []
    viewable = set()

    # mark the points that are viewable along the forward direction
    for sq in forward:
        if not checkBounds(sq):
            break
        
        if board[sq[0]][sq[1]] == 0:
            boundary.append(sq)
            break
        viewable.add(sq)

    # mark the points that are viewable along the clockwise diagonal
    for sq in diagonal_clock:
        if not checkBounds(sq):
            break
        
        if board[sq[0]][sq[1]] == 0:
            boundary.append(sq)
            break
        viewable.add(sq)

    # mark the points that are viewable along the anti clockwise diagonal
    for sq in diagonal_counter_clock:
        if not checkBounds(sq):
            break
        
        if board[sq[0]][sq[1]] == 0:
            boundary.append(sq)
            break
        viewable.add(sq)

    # mark the points that are viewable along the angled clockwise direction
    # mark as viewable if the point has two pre requisite points - one "behind" it and the appropriately "diagonally behind it"
    for sq in angled_clock:
        if not checkBounds(sq):
            continue
        if direction[0]:
            if (sq[0]-direction[0],sq[1]) in viewable and (sq[0]-direction[0],sq[1]+direction[0]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)
        else:
            if (sq[0],sq[1]-direction[1]) in viewable and (sq[0]+direction[1],sq[1]-direction[1]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)

    # mark the points that are viewable along the angled counter clockwise direction
    # mark as viewable if the point has two pre requisite points - one "behind" it and the appropriately "diagonally behind it"
    for sq in angled_counter_clock:
        if not checkBounds(sq):
            continue
        if direction[0]:
            if (sq[0]-direction[0],sq[1]) in viewable and (sq[0]-direction[0],sq[1]-direction[0]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)
        else:
            if (sq[0],sq[1]-direction[1]) in viewable and (sq[0]-direction[1],sq[1]-direction[1]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)

    return list(viewable)+boundary+[point]

def calculateLineOfSightSpotter(board,point,direction):

    # initialising the different directions in consideration
    forward = []
    diagonal_counter_clock =[]
    diagonal_clock = []
    angled_counter_clock =[]
    angled_clock = []

    # check whether the direction being faced is one of the x directions
    if direction[0]:

        # generate the progressive points in the forward and diagonal directions
        forward = [(point[0]+x*direction[0],point[1])for x in range(1,6)]
        diagonal_counter_clock = [(point[0]+x*direction[0],point[1]+x*direction[0]) for x in range(1,4)]
        diagonal_clock = [(point[0]+x*direction[0],point[1]-x*direction[0]) for x in range(1,4)]

        # get all possibly viewable points between the forward line and diagonals

        # generate theses points as slices along the forward direction
        angled_counter_clock_1 = [(point[0]+x*direction[0],point[1]+direction[0]*1)for x in range(2,6)]
        angled_counter_clock_2 = [(point[0]+x*direction[0],point[1]+direction[0]*2)for x in range(3,6)]
        angled_counter_clock_3 = [(point[0]+x*direction[0],point[1]+direction[0]*3)for x in range(4,5)]
        angled_counter_clock = angled_counter_clock_1+angled_counter_clock_2+angled_counter_clock_3

        angled_clock_1 = [(point[0]+x*direction[0],point[1]-direction[0]*1)for x in range(2,6)]
        angled_clock_2 = [(point[0]+x*direction[0],point[1]-direction[0]*2)for x in range(3,6)]
        angled_clock_3 = [(point[0]+x*direction[0],point[1]-direction[0]*3)for x in range(4,5)]
        angled_clock = angled_clock_1+angled_clock_2+angled_clock_3
    else:
        
        # generate the progressive points in the forward and diagonal directions
        forward = [(point[0],point[1]+x*direction[1])for x in range(1,6)]
        diagonal_counter_clock = [(point[0]+x*direction[1],point[1]+x*direction[1]) for x in range(1,4)]
        diagonal_clock = [(point[0]-x*direction[1],point[1]+x*direction[1]) for x in range(1,4)]
        
        # get all possibly viewable points between the forward line and diagonals

        # generate theses points as slices along the forward direction
        angled_counter_clock_1 = [(point[0]+direction[1]*1,point[1]+x*direction[1])for x in range(2,6)]
        angled_counter_clock_2 = [(point[0]+direction[1]*2,point[1]+x*direction[1])for x in range(3,6)]
        angled_counter_clock_3 = [(point[0]+direction[1]*3,point[1]+x*direction[1])for x in range(4,5)]
        angled_counter_clock = angled_counter_clock_1+angled_counter_clock_2+angled_counter_clock_3

        angled_clock_1 = [(point[0]-direction[1]*1,point[1]+x*direction[1])for x in range(2,6)]
        angled_clock_2 = [(point[0]-direction[1]*2,point[1]+x*direction[1])for x in range(3,6)]
        angled_clock_3 = [(point[0]-direction[1]*3,point[1]+x*direction[1])for x in range(4,5)]
        angled_clock = angled_clock_1+angled_clock_2+angled_clock_3

    boundary = []
    viewable = set()

    # mark the points that are viewable along the forward direction
    for sq in forward:
        if not checkBounds(sq):
            break
        
        if board[sq[0]][sq[1]] == 0:
            boundary.append(sq)
            break
        viewable.add(sq)

    # mark the points that are viewable along the clockwise diagonal
    for sq in diagonal_clock:
        if not checkBounds(sq):
            break
        
        if board[sq[0]][sq[1]] == 0:
            boundary.append(sq)
            break
        viewable.add(sq)

    # mark the points that are viewable along the anti clockwise diagonal
    for sq in diagonal_counter_clock:
        if not checkBounds(sq):
            break
        
        if board[sq[0]][sq[1]] == 0:
            boundary.append(sq)
            break
        viewable.add(sq)

    # mark the points that are viewable along the angled clockwise direction
    # mark as viewable if the point has two pre requisite points - one "behind" it and the appropriately "diagonally behind it"
    for sq in angled_clock:
        if not checkBounds(sq):
            continue
        if direction[0]:
            if (sq[0]-direction[0],sq[1]) in viewable and (sq[0]-direction[0],sq[1]+direction[0]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)
        else:
            if (sq[0],sq[1]-direction[1]) in viewable and (sq[0]+direction[1],sq[1]-direction[1]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)

    # mark the points that are viewable along the angled counter clockwise direction
    # mark as viewable if the point has two pre requisite points - one "behind" it and the appropriately "diagonally behind it"
    for sq in angled_counter_clock:
        if not checkBounds(sq):
            continue
        if direction[0]:
            if (sq[0]-direction[0],sq[1]) in viewable and (sq[0]-direction[0],sq[1]-direction[0]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)
        else:
            if (sq[0],sq[1]-direction[1]) in viewable and (sq[0]-direction[1],sq[1]-direction[1]) in viewable:
                if board[sq[0]][sq[1]] == 0:
                    boundary.append(sq)
                else:
                    viewable.add(sq)

    return list(viewable)+boundary+[point]

    
def checkBounds(point):
    if point[0]<size[0] and point[0]>=0 and point[1]>=0 and point[1]<size[1]:
        return True
    return False

class Assasin(pg.sprite.Sprite):

    def __init__(self, i, initial_position, initial_direction):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("Assasin{}.png".format(i), 1)
        self.original_image = self.image
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (initial_position[1]*tile_size,initial_position[0]*tile_size)
        initial_direction = list(initial_direction)
        if initial_direction == [1,0]:
            self.image = rotate(self.original_image,180)
        elif initial_direction == [-1,0]:
            self.image = rotate(self.original_image,0)
        elif initial_direction == [0,1]:
            self.image = rotate(self.original_image,270)
        else:
            self.image = rotate(self.original_image,90)

    def step(self,new_position, new_direction):
        self.rect.topleft = (new_position[1]*tile_size,new_position[0]*tile_size)
        new_direction = list(new_direction)
        if new_direction == [1,0]:
            self.image = rotate(self.original_image,180)
        elif new_direction == [-1,0]:
            self.image = rotate(self.original_image,0)
        elif new_direction == [0,1]:
            self.image = rotate(self.original_image,270)
        else:
            self.image = rotate(self.original_image,90)

class Spotter(pg.sprite.Sprite):

    def __init__(self, i, initial_position, initial_direction):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("Spotter{}.png".format(i), 1)
        self.original_image = self.image
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (initial_position[1]*tile_size,initial_position[0]*tile_size)
        initial_direction = list(initial_direction)

        if initial_direction == [1,0]:
            self.image = rotate(self.original_image,180)
        elif initial_direction == [-1,0]:
            self.image = rotate(self.original_image,0)
        elif initial_direction == [0,1]:
            self.image = rotate(self.original_image,270)
        else:
            self.image = rotate(self.original_image,90)

    def step(self,new_position, new_direction):
        self.rect.topleft = (new_position[1]*tile_size,new_position[0]*tile_size)
        new_direction = list(new_direction)
        if new_direction == [1,0]:
            self.image = rotate(self.original_image,180)
        elif new_direction == [-1,0]:
            self.image = rotate(self.original_image,0)
        elif new_direction == [0,1]:
            self.image = rotate(self.original_image,270)
        else:
            self.image = rotate(self.original_image,90)

# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def main(file_name):

    turn = 0

    turn_switch = {
        0:1,
        1:2,
        2:3,
        3:0
    }

    f = open(file_name)
    history = f.readlines()
    f.close()
    board = history[0]
    board = eval(board)
    initial_state = history[1]
    initial_state = eval(initial_state)
    history = history[2:]
    history = list(map(eval,history))

    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()

    agents = []
    allSprites = []

    screen = pg.display.set_mode(tuple([x*tile_size for x in size]))
    wall,wall_rect = load_image('wall.png')
    empty,empty_rect = load_image('empty.png')
    highground,highground_rect = load_image('highground.png')
    vision,vision_rect = load_image('vision.png',-1)

    for ind_y, row in enumerate(board):
        for ind_x, element in enumerate(row):
            if element == 0:
                screen.blit(wall,(ind_x*tile_size,ind_y*tile_size))
            elif element == 1:
                screen.blit(empty,(ind_x*tile_size,ind_y*tile_size))
            else:
                screen.blit(highground,(ind_x*tile_size,ind_y*tile_size))

    for agent_state in initial_state:
        (agentId, current_spotter_point, current_assasin_point,
            current_spotter_direction, current_assasin_direction,
            spotter_alive, assasin_alive) = agent_state
        assasin = Assasin(agentId, current_assasin_point, current_assasin_direction)
        spotter = Spotter(agentId, current_spotter_point, current_spotter_direction)
        agents.append((
                assasin,
                spotter
            ))
        allSprites.append(assasin)
        allSprites.append(spotter)

    new_state = initial_state

    allSprites = pg.sprite.RenderPlain(tuple(allSprites))

    pg.display.flip()

    going = True
    clock = pg.time.Clock()
    while history and going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                new_state = history.pop(0)
                if not new_state:
                    board = history.pop(0)
                    new_state = history.pop(0)
                    break
                turn = turn_switch[turn]

                for agent_state in new_state:
                    (agentId, current_spotter_point, current_assasin_point,
                        current_spotter_direction, current_assasin_direction,
                        spotter_alive, assasin_alive) = agent_state
                    if assasin_alive:
                        agents[agentId][0].step(current_assasin_point,current_assasin_direction)
                    else:
                        if agents[agentId][0]:
                            obj = agents[agentId][0]
                            agents[agentId] = (None,agents[agentId][1])
                            del obj

                    if spotter_alive:
                        agents[agentId][1].step(current_spotter_point,current_spotter_direction)
                    else:
                        if agents[agentId][1]:
                            obj = agents[agentId][1]
                            agents[agentId] = (agents[agentId][0],None)
                            del obj
        for ind_y, row in enumerate(board):
            for ind_x, element in enumerate(row):
                if element == 0:
                    screen.blit(wall,(ind_x*tile_size,ind_y*tile_size))
                elif element == 1:
                    screen.blit(empty,(ind_x*tile_size,ind_y*tile_size))
                else:
                    screen.blit(highground,(ind_x*tile_size,ind_y*tile_size))

        
        allSprites.empty()
        allSprites = []
        for agent in agents:
            if agent[0]:
                allSprites.append(agent[0])
            if agent[1]:
                allSprites.append(agent[1])
        # pass turn if dead
        while True:
            (agentId, current_spotter_point, current_assasin_point,
                        current_spotter_direction, current_assasin_direction,
                        spotter_alive, assasin_alive) = new_state[turn]
            if spotter_alive or assasin_alive:
                break

            turn = turn_switch[turn]

        # render visible for next turn
        (agentId, current_spotter_point, current_assasin_point,
                        current_spotter_direction, current_assasin_direction,
                        spotter_alive, assasin_alive) = new_state[turn]
        visible_points = []
        if spotter_alive:
            if board[current_spotter_point[0]][current_spotter_point[1]] == 2:
                visible_points += calculateLineOfSightHighground(current_spotter_point)
            else:
                visible_points += calculateLineOfSightSpotter(board,
                    current_spotter_point,current_spotter_direction)
        
        if assasin_alive:
            visible_points += calculateLineOfSightAssasin(board,
                    current_assasin_point,current_assasin_direction)

        for point in visible_points:
            screen.blit(vision,(point[1]*tile_size,point[0]*tile_size))
        # update to next turn

        allSprites = pg.sprite.RenderPlain(tuple(allSprites))
        allSprites.draw(screen)
        pg.display.flip()
    pg.quit()

# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main("history.hbd")
