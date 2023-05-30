'''Ant colony simulation.'''
import random
import numpy as np
import visualisation
import math

class Board:
    '''
    Board of colony.
    '''
    def __init__(self,n,m):
        self._board = np.zeros((n,m))

    def create_obstacle(self, x, y):
        '''
        Creates obstacle on board.
        '''
        self._board[x][y] = -1

    def choose_spawn_point(self, x, y):
        '''
        Chooses spawn point of ants.
        '''
        self._board[x][y] = -2

    def choose_food_point(self, x, y):
        '''
        Choose points of food spawn.
        '''
        self._board[x][y] = -3

class Ant:
    '''
    Automata ant.
    '''
    pheromone_max = 1
    food_collected = 0
    def __init__(self, spawn_point, life_time):
        self.search_state = 1
        self.return_state = 0
        self.__x,self.__y = spawn_point
        self.life_time = life_time
        self.pheromon_strength = 1
        self.last_move = 0,0
        self.last = 0,0
        self.time = 1

    def make_move(self, move, cell_state):
        '''
        Changes position of ant on board.
        '''
        self.life_time -= 1
        if self.life_time == 0:
            return -1
        self.last = self.__x, self.__y
        self.last_move = self.__x - move[0], self.__y - move[1]
        self.__x = move[0]
        self.__y = move[1]
        self.check_surround(cell_state)
        return self.pheromon_strength

    def check_surround(self, cell_state):
        '''
        Checks surrounds of ant.
        '''
        if cell_state == -3 and self.search_state == 1:
            self.return_state = 1
            self.search_state = 0
            self.pheromon_strength = Ant.pheromone_max
            self.time = 0
            self.last = self.last[0] + self.last_move[0], self.last[1] + self.last_move[1]
            self.last_move  = -self.last_move[0],-self.last_move[1]

        elif cell_state == -2 and self.return_state == 1:
            self.return_state = 0
            self.search_state = 1
            Ant.food_collected += 1
            print(Ant.food_collected)
            print('return:', self.time)
            self.time = 0
            self.pheromon_strength = Ant.pheromone_max
        elif self.return_state:
            self.time += 1
            self.pheromon_strength *= 0.95
        else:
            self.pheromon_strength *= 0.985

    @property
    def x(self):
        '''
        Getter.
        '''
        return self.__x

    @property
    def y(self):
        '''
        Getter.
        '''
        return self.__y

    @y.setter
    def y(self, value):
        '''
        Setter.
        '''
        self.__y = value

    @x.setter
    def x(self, value):
        '''
        Setter.
        '''
        self.__x = value


class PheromoneBoard:
    '''
    Pheromone map.
    '''
    def __init__(self, _n, _m):
        self._board = np.zeros((_n, _m))
        self.count = 0

    def evaporate(self, evaporate_rate):
        '''
        Evaporates pheromones.
        '''
        if self.count > 10:
            self.count = 0
            for x in range(len(self._board)):
                for y in range(len(self._board[0])):
                    if self._board[x][y] <= 0.001:
                        self._board[x][y] = 0
        self._board = self._board *(1 - evaporate_rate)
        self.count += 1

class Game:
    '''
    Game engine.
    '''
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = Board(n, m)
        self.pheromone_base_board = PheromoneBoard(n, m)
        self.pheromone_food_board = PheromoneBoard(n, m)
        self.step = 0

    def create_environment(self, list_of_obstacles, list_of_food):
        '''
        Creates environment.
        '''
        self.environment_created = True
        self.list_of_obstacles = list_of_obstacles
        self.list_of_food = list_of_food
        for x, y in list_of_obstacles:
            self.board.create_obstacle(x, y)
        for x, y in list_of_food:
            self.board.choose_food_point(x, y)

    def create_base(self, list_of_bases):
        '''
        Create base.
        '''
        self.base_created = True
        self.list_of_bases = list_of_bases
        for x, y in list_of_bases:
            self.board.choose_spawn_point(x, y)
        self.spawn_point = list_of_bases[len(list_of_bases)//2]
        self.pheromone_base_board._board[self.spawn_point[0],self.spawn_point[1]] = 10
        self.generate_nearbase()

    def create_colony(self, n, lifespan):
        '''
        Creates first ants.
        '''
        self.colony_created = True
        self.num_of_ants = n
        self.lifespan = lifespan
        self.ants = []
        for _ in range(n):
            self.ants.append(Ant(self.spawn_point, lifespan))

    def possible_moves(self, x, y):
        '''
        Return list of all valid moves.
        '''
        moves_list = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == dy and dx == 0:
                    continue
                if x + dx < 0 or y+dy < 0:
                    continue
                if x + dx >= self.n or y+dy >= self.m:
                    continue
                if self.board._board[x+dx][y+dy] != -1:
                    moves_list.append((x+dx, y+dy))
        return moves_list

    def estimate_moves(self, possible_moves, ant_search_state, last_move, last):
        '''
        Estimate and return attractivness of moves.
        '''
        attractivness_list = [0.0005 for _ in range(len(possible_moves))]
        if ant_search_state:
            for pos, (x,y) in enumerate(possible_moves):
                attractivness_list[pos] += self.pheromone_food_board._board[x][y]**2
                attractivness_list[pos] /= (1+self.pheromone_base_board._board[x][y])
        else:
            for pos, (x,y) in enumerate(possible_moves):
                attractivness_list[pos] += self.pheromone_base_board._board[x][y]**2
                attractivness_list[pos] /= (1+self.pheromone_food_board._board[x][y])

        _a = {(0,1):[2,5,8],
            (1,1):[5,7,8],
            (1,0):[6,7,8],
            (-1,0):[0,1,2],
            (0,-1):[0,3,6],
            (-1,-1):[0,1,3],
            (-1,1):[1,2,5],
            (1,-1):[3,6,7],
            (0,0):[]}
        _b = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        new_moves = [(elem[0]-last[0],elem[1]-last[1]) for elem in possible_moves]

        for _elem in _a[last_move]:
            if _b[_elem] in new_moves:

                attractivness_list[new_moves.index(_b[_elem])] /= 1000000

        return list(np.array(attractivness_list) / max(np.array(attractivness_list)) )

    def make_move(self, possible_moves, attractivness_list):
        '''
        Return random move from attractive moves.
        '''
        chance = random.random()
        chance_list = [0]
        for _elem in attractivness_list:
            chance_list.append(chance_list[-1] + _elem)
        chance_list.pop(0)
        chance = chance * chance_list[-1]
        for pos, _elem in enumerate(chance_list):
            if chance < _elem:
                return possible_moves[pos]
        return possible_moves[-1]

    def run(self):
        '''Runs the game.'''
        assert self.base_created == True
        assert self.colony_created == True
        assert self.environment_created == True

        self.step += 1
        if self.step % 3 == 0:
            self.ants.append(Ant(self.spawn_point, self.lifespan))
        if self.step % 300 == 0:
            _c = 0
            _b = 0
            for _elem in self.ants:
                if _elem.return_state == 1:
                    _c+=1
                else:
                    _b += 1

        for _x,_y in self.list_of_bases:
            self.pheromone_base_board._board[_x][_y] = 9999
        for _x,_y in self.near_base:
            self.pheromone_base_board._board[_x][_y] = 1200
        for pos, ant in enumerate(self.ants):
            possible = self.possible_moves(ant.x, ant.y)
            attractivness = self.estimate_moves(possible,\
                                                 ant.search_state, ant.last_move, (ant.x,ant.y))
            move = self.make_move(possible, attractivness)
            pheromone = ant.make_move(move, self.board._board[move[0]][move[1]])
            if pheromone == -1:
                self.ants.pop(pos)
            else:
                if ant.search_state:
                    self.pheromone_base_board._board[move[0]][move[1]] += pheromone
                else:
                    self.pheromone_food_board._board[move[0]][move[1]] += pheromone
        self.pheromone_base_board.evaporate(0.003)
        self.pheromone_food_board.evaporate(0.003)

    def generate_nearbase(self):
        '''
        Generates space near base.
        '''
        self.near_base = []
        for x,y in self.list_of_bases:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if (x+dx,y+dy) not in self.list_of_bases:
                        self.near_base.append((x+dx,y+dy))

    def str(self):
        '''
        Returns printable and suitable for visualisation function string of base.
        '''
        new_board = Board(self.n, self.m)
        for pos in range(len(self.board._board)):
            for sop in range(len(self.board._board[0])):
                if self.pheromone_base_board._board[pos][sop] > 0:
                    new_board._board[pos][sop] = -4
                if self.pheromone_food_board._board[pos][sop] > 0:
                    new_board._board[pos][sop] = -5
                if self.pheromone_base_board._board[pos][sop] > 0 and self.pheromone_food_board._board[pos][sop] > 0:
                    new_board._board[pos][sop] = -6

        for _x, _y in self.list_of_obstacles:
            new_board._board[_x][_y] = -1

        for _x, _y in self.list_of_food:
            new_board._board[_x][_y] = -3

        for ant in self.ants:
            if ant.search_state:
                new_board._board[ant.x][ant.y] = 1
            else:
                new_board._board[ant.x][ant.y] = 2

        new_base_pher_board = self.pheromone_base_board._board.copy()
        new_pheromone_food_board = self.pheromone_food_board._board.copy()

        base_start = (self.near_base[0][0] + 1, self.near_base[0][1] + 1)
        for _i in range(0,3):
            for _j in range(0,3):
                new_board._board[base_start[0]+_i][base_start[1]+_j] = -2
                new_base_pher_board[base_start[0]+_i][base_start[1]+_j] = 0
                new_pheromone_food_board[base_start[0]+_i][base_start[1]+_j] = 0

        for _x, _y in self.near_base:
            new_board._board[_x][_y] = -7
            new_base_pher_board[_x][_y] = 0
            new_pheromone_food_board[_x][_y] = 0


        return  new_board._board, new_base_pher_board, new_pheromone_food_board, new_base_pher_board.max(), new_pheromone_food_board.max()



def generate_circle_coords(radius, center=(0, 0)):
    coords = []
    center_x, center_y = center

    for x in range(center_x - radius, center_x + radius + 1):
        for y in range(center_y - radius, center_y + radius + 1):
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            if distance <= radius:
                coords.append((x, y))
    return coords

def generate_rectangle_coords(n, m, top_left=(0, 0)):
    x1, y1 = top_left
    x2, y2 = x1 + n, y1 + m

    coords = []
    for x in range(x1, x2):
        for y in range(y1, y2):
            coords.append((x, y))

    return coords

# a = Game(20,20)
# a.create_environment([], [(16,15),(18,16),(16,17),(17,17),(18,18),(17,18)])
# a.create_base([(11,11),(11,12),(12,12),(12,11)])
# a.create_colony(8, 100)

a = Game(100,100)
a.create_environment(generate_rectangle_coords(10, 10, (60,35))+generate_circle_coords(6, (63,63)), [(i,y) for i in range(75,82) for y in range(75,82)]+[(i,y) for i in range(75,82) for y in range(25,32)])
a.create_base([(i,y) for i in range(45,48) for y in range(50,53)])
a.create_colony(20, 250)

# terrain = []

# # Generate circles
# circle_radius_1 = 12
# circle_center_1 = (60, 60)
# circle_coords_1 = generate_circle_coords(circle_radius_1, circle_center_1)
# terrain.extend(circle_coords_1)

# circle_radius_2 = 10
# circle_center_2 = (120, 40)
# circle_coords_2 = generate_circle_coords(circle_radius_2, circle_center_2)
# terrain.extend(circle_coords_2)

# circle_radius_3 = 15
# circle_center_3 = (80, 120)
# circle_coords_3 = generate_circle_coords(circle_radius_3, circle_center_3)
# terrain.extend(circle_coords_3)

# circle_radius_4 = 8
# circle_center_4 = (140, 100)
# circle_coords_4 = generate_circle_coords(circle_radius_4, circle_center_4)
# terrain.extend(circle_coords_4)

# # Generate rectangles
# rectangle_width_1 = 20
# rectangle_height_1 = 15
# rectangle_top_left_1 = (90, 70)
# rectangle_coords_1 = generate_rectangle_coords(rectangle_width_1, rectangle_height_1, rectangle_top_left_1)
# terrain.extend(rectangle_coords_1)

# rectangle_width_2 = 10
# rectangle_height_2 = 20
# rectangle_top_left_2 = (30, 100)
# rectangle_coords_2 = generate_rectangle_coords(rectangle_width_2, rectangle_height_2, rectangle_top_left_2)
# terrain.extend(rectangle_coords_2)

# rectangle_width_3 = 15
# rectangle_height_3 = 8
# rectangle_top_left_3 = (120, 140)
# rectangle_coords_3 = generate_rectangle_coords(rectangle_width_3, rectangle_height_3, rectangle_top_left_3)
# terrain.extend(rectangle_coords_3)

# rectangle_width_4 = 12
# rectangle_height_4 = 10
# rectangle_top_left_4 = (50, 140)
# rectangle_coords_4 = generate_rectangle_coords(rectangle_width_4, rectangle_height_4, rectangle_top_left_4)
# terrain.extend(rectangle_coords_4)

# a = Game(150,150)
# a.create_environment(terrain,generate_rectangle_coords(10, 10, (100, 100)))
# a.create_base([(76, 67), (77, 67), (78, 67),
#         (76, 68), (77, 68), (78, 68),
#         (76, 69), (77, 69), (78, 69)])
# a.create_colony(20, 500)

for i in range(25000):
    a.run()
    board_str = a.str()
    visualisation.draw_board(visualisation.fire_screen, board_str[0], \
                             a.n, a.m, visualisation.FIRESCREEN_WIDTH/a.n, board_str[1:])
    #time.sleep(1)
