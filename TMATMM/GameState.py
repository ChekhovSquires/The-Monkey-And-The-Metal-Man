from games.TMATMM.Player import Player
from typing import List
from json import dumps
from copy import deepcopy
from games.utils.utils import get_action


class GameState:

    def findWinner(self):

        for agent in self.agents:
            if agent.check_alive():
                return [agent.ID]

        return self.findWinnerPrev()

    def findWinnerPrev(self):
        agent_dicts = self.logs[-4]
        winners = []
        for agent_dict in agent_dicts:
            if agent_dict["spotter alive"] or agent_dict["assasin alive"]:
                winners.append(agent_dict["agent id"])

        return winners

    def writeToHistory(self, inp):
        self.logs.append(inp)

    def __init__(self, height, width, walls, high_points,
                 history_file, spawn_points=[], spawn_directions=[], agent_classes=[], store_logs=True, show_bot_prints=True):
        if not spawn_points:
            spawn_points = [((0, 0), (0, 1)), ((0, width-1), (1, width-1)),
                            ((height-1, width-1), (height-1, width-2)), ((height-1, 0), (height-2, 0))]
        if not spawn_directions:
            spawn_directions = [((1, 0), (1, 0)), ((0, -1), (0, -1)),
                                ((-1, 0), (-1, 0)), ((0, 1), (0, 1))]
        print_logs = {"print_logs": show_bot_prints}
        initialising_vals = [[*spawn_points[x], *
                              spawn_directions[x]] for x in range(4)]

        self.size = (width, height)
        self.logs = []
        self.high_points = set(high_points)
        board = [[1 for x in range(self.size[0])]for x in range(self.size[1])]
        for wall in walls:
            board[wall[0]][wall[1]] = 0
        for high_point in high_points:
            board[high_point[0]][high_point[1]] = 2

        self.board = board
        self.store_logs = store_logs
        self.writeToHistory(deepcopy(board))

        self.agents: List[Player]
        self.agents = []
        for ind, (initialising_val, agent_class) in enumerate(zip(initialising_vals, agent_classes)):
            self.agents.append(
                Player(ind, *initialising_val, agent_class, **print_logs))

        self.writeToHistory(self.getState())
        self.circles = 0
        self.timer = 5
        self.done = False
        self.history_file = history_file

    def writeHistoryToFile(self):
        with open(self.history_file, 'w') as f:
            f.write(dumps(self.logs))

    def getStateStr(self):
        agents_state = ""
        for agent in self.agents:
            agents_state += dumps(dict(agent))+','
        return "["+agents_state[:-1]+"]"

    def getState(self):
        agents_state = []
        for agent in self.agents:
            agents_state.append(dict(agent))
        return agents_state

    def collapseMap(self):
        for x in range(len(self.board)):
            self.board[x][self.circles] = 0

        for x in range(len(self.board)):
            self.board[x][-self.circles-1] = 0

        for x in range(len(self.board[0])):
            self.board[self.circles][x] = 0

        for x in range(len(self.board[0])):
            self.board[-1-self.circles][x] = 0

        for player in self.agents:
            assasin_point = player.assasin.get_location()
            spotter_point = player.spotter.get_location()
            assasin = player.assasin
            spotter = player.spotter

            if self.board[assasin_point[0]][assasin_point[1]] == 0:
                if assasin.get_status():
                    assasin.killed()
                    print("ASSASIN ID #{} just died to storm!".format(player.ID))

            if self.board[spotter_point[0]][spotter_point[1]] == 0:
                if spotter.get_status():
                    spotter.killed()
                    print("SPOTTER ID #{} just died to storm!".format(player.ID))

    def checkBounds(self, point):
        if point[0] < self.size[0] and point[0] >= 0 and point[1] >= 0 and point[1] < self.size[1]:
            return True
        return False

    def calculateLineOfSightHighground(self, point):
        points = []
        for x in range(-5, 6):
            limit = 5-abs(x)
            for y in range(-limit, limit+1):
                cur_point = (point[0]+x, point[1]+y)
                if self.checkBounds(cur_point):
                    points.append(cur_point)

        return points

    @staticmethod
    def getPossibleViewPoints(forward_length, diagonal_length, point, direction):
        forward = []
        diagonal_counter_clock = []
        diagonal_clock = []
        angled_counter_clock = []
        angled_clock = []

        # check whether the direction being faced is one of the x directions
        if direction[0]:

            # generate the progressive points in the forward and diagonal directions
            forward = [(point[0]+x*direction[0], point[1])
                       for x in range(1, forward_length)]
            diagonal_counter_clock = [
                (point[0]+x*direction[0], point[1]+x*direction[0]) for x in range(1, diagonal_length)]
            diagonal_clock = [(point[0]+x*direction[0], point[1]-x*direction[0])
                              for x in range(1, diagonal_length)]

            # get all possibly viewable points between the forward line and diagonals

            # generate theses points as slices along the forward direction
            angled_counter_clock_1 = [
                (point[0]+x*direction[0], point[1]+direction[0]*1)for x in range(2, forward_length)]
            angled_counter_clock_2 = [
                (point[0]+x*direction[0], point[1]+direction[0]*2)for x in range(3, forward_length)]
            angled_counter_clock_3 = [
                (point[0]+x*direction[0], point[1]+direction[0]*3)for x in range(4, forward_length-1)]
            angled_counter_clock = angled_counter_clock_1 + \
                angled_counter_clock_2+angled_counter_clock_3

            angled_clock_1 = [(point[0]+x*direction[0], point[1]-direction[0]*1)
                              for x in range(2, forward_length)]
            angled_clock_2 = [(point[0]+x*direction[0], point[1]-direction[0]*2)
                              for x in range(3, forward_length)]
            angled_clock_3 = [(point[0]+x*direction[0], point[1]-direction[0]*3)
                              for x in range(4, forward_length-1)]
            angled_clock = angled_clock_1+angled_clock_2+angled_clock_3
        else:

            # generate the progressive points in the forward and diagonal directions
            forward = [(point[0], point[1]+x*direction[1])
                       for x in range(1, forward_length)]
            diagonal_counter_clock = [
                (point[0]+x*direction[1], point[1]+x*direction[1]) for x in range(1, diagonal_length)]
            diagonal_clock = [(point[0]-x*direction[1], point[1]+x*direction[1])
                              for x in range(1, diagonal_length)]

            # get all possibly viewable points between the forward line and diagonals

            # generate theses points as slices along the forward direction
            angled_counter_clock_1 = [
                (point[0]+direction[1]*1, point[1]+x*direction[1])for x in range(2, forward_length)]
            angled_counter_clock_2 = [
                (point[0]+direction[1]*2, point[1]+x*direction[1])for x in range(3, forward_length)]
            angled_counter_clock_3 = [
                (point[0]+direction[1]*3, point[1]+x*direction[1])for x in range(4, forward_length-1)]
            angled_counter_clock = angled_counter_clock_1 + \
                angled_counter_clock_2+angled_counter_clock_3

            angled_clock_1 = [(point[0]-direction[1]*1, point[1]+x*direction[1])
                              for x in range(2, forward_length)]
            angled_clock_2 = [(point[0]-direction[1]*2, point[1]+x*direction[1])
                              for x in range(3, forward_length)]
            angled_clock_3 = [(point[0]-direction[1]*3, point[1]+x*direction[1])
                              for x in range(4, forward_length-1)]
            angled_clock = angled_clock_1+angled_clock_2+angled_clock_3

        return forward, diagonal_counter_clock, diagonal_clock, angled_counter_clock, angled_clock

    def calculateViewablePoints(self, point, direction, forward, diagonal_counter_clock, diagonal_clock,
                                angled_counter_clock, angled_clock):
        boundary = []
        viewable = set()

        # mark the points that are viewable along the forward direction
        for sq in forward:
            if not self.checkBounds(sq):
                break

            if self.board[sq[0]][sq[1]] == 0:
                boundary.append(sq)
                break
            viewable.add(sq)

        # mark the points that are viewable along the clockwise diagonal
        for sq in diagonal_clock:
            if not self.checkBounds(sq):
                break

            if self.board[sq[0]][sq[1]] == 0:
                boundary.append(sq)
                break
            viewable.add(sq)

        # mark the points that are viewable along the anti clockwise diagonal
        for sq in diagonal_counter_clock:
            if not self.checkBounds(sq):
                break
            if self.board[sq[0]][sq[1]] == 0:
                boundary.append(sq)
                break
            viewable.add(sq)

        # mark the points that are viewable along the angled clockwise direction
        # mark as viewable if the point has two pre requisite points - one "behind" it and the appropriately "diagonally behind it"
        for sq in angled_clock:
            if not self.checkBounds(sq):
                continue
            if direction[0]:
                if (sq[0]-direction[0], sq[1]) in viewable and (sq[0]-direction[0], sq[1]+direction[0]) in viewable:
                    if self.board[sq[0]][sq[1]] == 0:
                        boundary.append(sq)
                    else:
                        viewable.add(sq)
            else:
                if (sq[0], sq[1]-direction[1]) in viewable and (sq[0]+direction[1], sq[1]-direction[1]) in viewable:
                    if self.board[sq[0]][sq[1]] == 0:
                        boundary.append(sq)
                    else:
                        viewable.add(sq)

        # mark the points that are viewable along the angled counter clockwise direction
        # mark as viewable if the point has two pre requisite points - one "behind" it and the appropriately "diagonally behind it"
        for sq in angled_counter_clock:
            if not self.checkBounds(sq):
                continue
            if direction[0]:
                if (sq[0]-direction[0], sq[1]) in viewable and (sq[0]-direction[0], sq[1]-direction[0]) in viewable:
                    if self.board[sq[0]][sq[1]] == 0:
                        boundary.append(sq)
                    else:
                        viewable.add(sq)
            else:
                if (sq[0], sq[1]-direction[1]) in viewable and (sq[0]-direction[1], sq[1]-direction[1]) in viewable:
                    if self.board[sq[0]][sq[1]] == 0:
                        boundary.append(sq)
                    else:
                        viewable.add(sq)

        return list(viewable)+boundary+[point]

    def calculateLineOfSightSpotter(self, point, direction):

        forward, diagonal_counter_clock, diagonal_clock, angled_counter_clock, angled_clock = self.getPossibleViewPoints(
            5 + 1, 3 + 1, point, direction)
        return self.calculateViewablePoints(point, direction, forward, diagonal_counter_clock, diagonal_clock, angled_counter_clock, angled_clock)

    def calculateLineOfSightAssasin(self, point, direction):

        forward, diagonal_counter_clock, diagonal_clock, angled_counter_clock, angled_clock = self.getPossibleViewPoints(
            2 + 1, 1 + 1, point, direction)
        return self.calculateViewablePoints(point, direction, forward, diagonal_counter_clock, diagonal_clock, angled_counter_clock, angled_clock)

    def calculatePercepts(self, agentId):

        agent = self.agents[agentId]

        # (_, spotter_point, assasin_point, spotter_direction, assasin_direction, spotter_alive, assasin_alive, agent_object) = agent_deets
        board = [[-1 for x in range(self.size[0])]
                 for x in range(self.size[1])]

        all_points = []
        spotter_points = []
        assasin_points = []
        if agent.spotter.get_status():

            spotter_point = agent.spotter.get_location()

            if spotter_point in self.high_points:
                points = self.calculateLineOfSightHighground(spotter_point)
            else:
                points = self.calculateLineOfSightSpotter(
                    spotter_point, agent.spotter.get_direction())
            spotter_points = points
            all_points += points

        if agent.assasin.get_status():
            assasin_point = agent.assasin.get_location()
            points = self.calculateLineOfSightAssasin(
                assasin_point, agent.assasin.get_direction())
            assasin_points = points
            all_points += points

        for point in all_points:
            board[point[0]][point[1]] = self.board[point[0]][point[1]]

        for other_agent in self.agents:

            if other_agent.ID == agentId:
                continue

            if other_agent.spotter.get_status():
                other_spotter_point = other_agent.spotter.get_location()

                if board[other_spotter_point[0]][other_spotter_point[1]] != -1:
                    board[other_spotter_point[0]][other_spotter_point[1]] = {
                        "playerId": other_agent.ID,
                        "direction": other_agent.spotter.get_direction(),
                        "type": "spotter",
                        "square": board[other_spotter_point[0]][other_spotter_point[1]]
                    }

            if other_agent.assasin.get_status():
                other_assasin_point = other_agent.assasin.get_location()

                if board[other_assasin_point[0]][other_assasin_point[1]] != -1:
                    board[other_assasin_point[0]][other_assasin_point[1]] = {
                        "playerId": other_agent.ID,
                        "direction": other_agent.assasin.get_direction(),
                        "type": "assasin",
                        "square": board[other_assasin_point[0]][other_assasin_point[1]]
                    }

        percepts = {
            "board": board,
            "timer": self.timer,
            "circles collapsed": self.circles,
            "spotter location": agent.spotter.get_location(),
            "assasin location": agent.assasin.get_location(),
            "spotter alive": agent.spotter.get_status(),
            "assasin alive": agent.assasin.get_status(),
            "spotter direction": agent.spotter.get_direction(),
            "assasin direction": agent.assasin.get_direction()
        }
        return percepts, {"spotter_point": spotter_points, "asssasin_point": assasin_points}

    def agentStep(self, agentId, action):

        assasin_step_results = []
        spotter_step_results = []

        agent = self.agents[agentId]
        spotter_move = action["Spotter"]
        assasin_move = action["Assasin"]
        current_spotter_direction = spotter_move["direction"]
        current_assasin_direction = assasin_move["direction"]
        current_assasin_point = agent.assasin.get_location()
        current_spotter_point = agent.spotter.get_location()

        if agent.spotter.get_status():
            moves = spotter_move["moves"]
            for x in range(2):
                if not moves:
                    break
                move = moves.pop(0)
                if (self.checkBounds((current_spotter_point[0]+move[0], current_spotter_point[1]+move[1])) and
                        self.board[current_spotter_point[0]+move[0]][current_spotter_point[1]+move[1]] != 0 and
                        (current_spotter_point[0]+move[0], current_spotter_point[1]+move[1]) != current_assasin_point):
                    current_spotter_point = (
                        current_spotter_point[0]+move[0], current_spotter_point[1]+move[1])
                    spotter_step_results.append((move, True))

                else:
                    spotter_step_results.append((move, False))

            for other_agent in self.agents:
                if other_agent.ID == agentId:
                    continue

                if other_agent.spotter.get_status():
                    if other_agent.spotter.get_location() == current_spotter_point:
                        other_agent.spotter.killed()
                        print("SPOTTER ID #{} was killed!".format(other_agent.ID))

                if other_agent.assasin.get_status():
                    if other_agent.assasin.get_location() == current_spotter_point:
                        other_agent.assasin.killed()
                        print("ASSASIN ID #{} was killed!".format(other_agent.ID))

        if agent.assasin.get_status():
            moves = assasin_move["moves"]
            for x in range(4):
                if not moves:
                    break
                move = moves.pop(0)
                if (self.checkBounds((current_assasin_point[0]+move[0], current_assasin_point[1]+move[1])) and
                        self.board[current_assasin_point[0]+move[0]][current_assasin_point[1]+move[1]] != 0 and
                        current_spotter_point != (current_assasin_point[0]+move[0], current_assasin_point[1]+move[1])):
                    current_assasin_point = (
                        current_assasin_point[0]+move[0], current_assasin_point[1]+move[1])
                    assasin_step_results.append((move, True))

                else:
                    assasin_step_results.append((move, False))

            for other_agent in self.agents:
                if other_agent.ID == agentId:
                    continue

                if other_agent.spotter.get_status():
                    if other_agent.spotter.get_location() == current_assasin_point:
                        other_agent.spotter.killed()
                        print("SPOTTER ID #{} was killed!".format(other_agent.ID))

                if other_agent.assasin.get_status():
                    if other_agent.assasin.get_location() == current_assasin_point:
                        other_agent.assasin.killed()
                        print("ASSASIN ID #{} was killed!".format(other_agent.ID))

        # set direction of assasin and spotter
        agent.assasin.set_direction(current_assasin_direction)
        agent.spotter.set_direction(current_spotter_direction)

        # set location of assasin and spotter
        agent.assasin.set_location(current_assasin_point)
        agent.spotter.set_location(current_spotter_point)

        return {"agent id": agentId, "spotter steps": spotter_step_results, "assasin steps": assasin_step_results}

    def getNumAlive(self) -> int:
        num_alive = 0
        for agent in self.agents:
            if agent.check_alive():
                num_alive += 1

        return num_alive

    def gameStep(self):

        num_alive = self.getNumAlive()

        if num_alive <= 1:
            self.done = True
            winner = self.findWinner()
            self.writeToHistory(winner)
            print(winner)
            print("GAME OVER")
            return

        for agent in self.agents:
            if agent.check_alive():
                percepts, viewable_points = self.calculatePercepts(agent.ID)
                action = get_action(agent.agent.step, percepts, default_action={
                    "Spotter": {
                        "direction": agent.spotter.get_direction(),
                        "moves": []
                    },
                    "Assasin": {
                        "direction": agent.assasin.get_direction(),
                        "moves": []
                    },
                    "Debug": "move skipped due to error/ timeout"
                })
                # action = agent.agent.step(percepts)
                moves_dict = self.agentStep(agent.ID, action)
                moves_dict["viewable points"] = viewable_points
                if self.store_logs:
                    try:
                        moves_dict["Debug"] = action["Debug"]
                    except:
                        pass
                self.writeToHistory(moves_dict)
                self.writeToHistory(self.getState())

        num_alive = self.getNumAlive()

        if num_alive <= 1:
            self.done = True
            winner = self.findWinner()
            self.writeToHistory(winner)
            print(winner)
            print("GAME OVER")
            return

        self.timer -= 1

        if self.timer == 0:
            self.timer = 5
            self.collapseMap()
            self.writeToHistory(0)
            self.writeToHistory(deepcopy(self.board))
            self.writeToHistory(self.getState())
            self.circles += 1
