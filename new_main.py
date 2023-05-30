import numpy as np
import random
import time
import visualisation

class Board:

    def __init__(self,n,m):
        self._board = np.zeros((n,m))

    def create_obstacle(self, x, y):
        self._board[x][y] = -1

    def choose_spawn_point(self, x, y):
        self._board[x][y] = -2

    def choose_food_point(self, x, y):
        self._board[x][y] = -3

class Ant:
    pheromone_max = 1
    food_collected = 0
    ant_z = 0
    board = Board(100,100)
    def __init__(self, spawn_point, life_time):
        self.search_state = 1
        self.return_state = 0
        self.__x,self.__y = spawn_point
        self.life_time = life_time
        self.pheromon_strength = 1
        self.last_move = 0,0
        self.last = 0,0
        Ant.ant_z += 1
        self.time = 0
        self.geni = False
        if Ant.ant_z == 500:
            self.geni = True
    def make_move(self, move, cell_state):
        if self.geni == True:
            Ant.board._board[move[0]][move[1]] += 1
        #self.time += 1
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
        if cell_state == -3:
            self.return_state = 1
            self.search_state = 0
            self.pheromon_strength = Ant.pheromone_max
            #print('search:',self.time)
            self.time = 0
            self.gini = 0
        elif cell_state == -2 and self.return_state == 1:
            self.return_state = 0
            self.search_state = 1
            Ant.food_collected += 1
            print(Ant.food_collected)
            print('return:',self.time)
            self.gini = False
            self.time = 0
            self.pheromon_strength = Ant.pheromone_max
        elif self.return_state:
            self.time += 1
            self.pheromon_strength = 6/self.time
        else:
            self.pheromon_strength *= 0.985

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    """
    @y.setter
    def y(self, value):
        self.__y = value
    """

    """
    @x.setter
    def x(self, value):
        self.__x = value
    """

class Pheromone_board:
    def __init__(self, n, m):
        self._board = np.zeros((n, m))
        self.count = 0

    def evaporate(self, evaporate_rate):
        if self.count > 10:
            self.count = 0
            for x in range(len(self._board)):
                for y in range(len(self._board[0])):
                    if self._board[x][y] <= 0.001:
                        self._board[x][y] = 0
        self._board = self._board *(1 - evaporate_rate)
        self.count += 1
        


    def create_feromon(self, x,y ,pheromon_strength):
        self.board[x][y] += pheromon_strength


class Game:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = Board(n, m)
        self.pheromone_base_board = Pheromone_board(n, m)
        self.pheromone_food_board = Pheromone_board(n, m)
        self.step = 0

    def create_environment(self, list_of_obstacles, list_of_food):
        self.environment_created = True
        for x, y in list_of_obstacles:
            self.board.create_obstacle(x, y)
        for x, y in list_of_food:
            self.board.choose_food_point(x, y)

    def create_base(self, list_of_bases):
        self.base_created = True
        self.list_of_bases = list_of_bases
        for x, y in list_of_bases:
            self.board.choose_spawn_point(x, y)
        self.spawn_point = list_of_bases[len(list_of_bases)//2]
        self.pheromone_base_board._board[self.spawn_point[0],self.spawn_point[1]] = 10
        self.generate_nearbase()

    def create_colony(self, n, lifespan):
        self.colony_created = True
        self.num_of_ants = n
        self.lifespan = lifespan
        self.ants = []
        for _ in range(n):
            self.ants.append(Ant(self.spawn_point, lifespan))

    def possible_moves(self, x, y):
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
        attractivness_list = [0.0005 for _ in range(len(possible_moves))]
        if ant_search_state:
            for pos, (x,y) in enumerate(possible_moves):
                attractivness_list[pos] += self.pheromone_food_board._board[x][y]
                attractivness_list[pos] /= (1+self.pheromone_base_board._board[x][y])
        else:
            for pos, (x,y) in enumerate(possible_moves):
                attractivness_list[pos] += self.pheromone_base_board._board[x][y]
                attractivness_list[pos] /= (1+self.pheromone_food_board._board[x][y])
        #print(attractivness_list)
        a = {(0,1):[2,5,8,1,7],
            (1,1):[5,7,8,2,6],
            (1,0):[6,7,8,3,5],
            (-1,0):[0,1,2,3,5],
            (0,-1):[0,3,6,1,7],
            (-1,-1):[0,1,3,2,6],
            (-1,1):[1,2,5,0,8],
            (1,-1):[3,6,7,0,8],
            (0,0):[]}
        b = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        new_moves = [(elem[0]-last[0],elem[1]-last[1]) for elem in possible_moves]
        #print(new_moves)
        #print(attractivness_list,"FDF")
        for elem in a[last_move]:
            if b[elem] in new_moves:
                #print('FGGGGGGGGGGGGGGGGGGGGGGGGGGG')
                attractivness_list[new_moves.index(b[elem])] /= 10
        #for i in range(len(attractivness_list)):
        #    attractivness_list[i] /= max(attractivness_list)

        return list(np.array(attractivness_list) / max(np.array(attractivness_list)) )

    def make_move(self, possible_moves, attractivness_list):
        #print(attractivness_list,'1')
        chance = random.random()
        chance_list = [0]
        #print(attractivness_list, 'huy')
        for elem in attractivness_list:
            chance_list.append(chance_list[-1] + elem)
        #print(chance_list)
        chance_list.pop(0)
        chance = chance * chance_list[-1]
        #print(attractivness_list,'1')
        #print(chance_list,'2')
        for pos,elem in enumerate(chance_list):
            if chance < elem:
                return possible_moves[pos]
        return possible_moves[-1]

    def run(self):
        assert self.base_created == True
        assert self.colony_created == True
        assert self.environment_created == True

        self.step += 1
        if self.step % 4 == 0:
            self.ants.append(Ant(self.spawn_point, self.lifespan))
        if self.step % 300 == 0:
            c = 0
            b = 0
            for elem in self.ants:
                if elem.return_state == 1:
                    c+=1
                else:
                    b += 1
            print(len(self.ants), 'gg', c,'r',b)
        for x,y in self.list_of_bases:
            self.pheromone_base_board._board[x][y] = 9999
        for x,y in self.near_base:
            self.pheromone_base_board._board[x][y] = 1200            
        for pos, ant in enumerate(self.ants):
            possible = self.possible_moves(ant.x, ant.y)
            #print(possible)
            attractivness = self.estimate_moves(possible, ant.search_state, ant.last_move, (ant.x,ant.y))
            #print(attractivness)
            move = self.make_move(possible, attractivness)
            #print(move)
            pheromone = ant.make_move(move, self.board._board[move[0]][move[1]])
            if pheromone == -1:
                self.ants.pop(pos)
            else:
                if ant.search_state:
                    self.pheromone_base_board._board[move[0]][move[1]] += pheromone
                else:
                    self.pheromone_food_board._board[move[0]][move[1]] += pheromone
        #self.pheromone_base_board.evaporate(0.01)
        #self.pheromone_food_board.evaporate(0.01)

    def generate_nearbase(self):
        self.near_base = []
        for x,y in self.list_of_bases:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if (x+dx,y+dy) not in self.list_of_bases:
                        self.near_base.append((x+dx,y+dy))

    def str(self):
        new_board = Board(self.n, self.m)
        for pos in range(len(self.board._board)):
            for sop in range(len(self.board._board[0])):
                new_board._board[pos][sop] = self.board._board[pos][sop]
        for pos in range(len(self.board._board)):
            for sop in range(len(self.board._board[0])):
                if self.pheromone_base_board._board[pos][sop] > 0:
                    new_board._board[pos][sop] = -4
                if self.pheromone_food_board._board[pos][sop] > 0:
                    new_board._board[pos][sop] = -5
                if self.pheromone_base_board._board[pos][sop] > 0 and self.pheromone_food_board._board[pos][sop] > 0:
                    new_board._board[pos][sop] = -6
                
        for ant in self.ants:
            if ant.search_state:
                new_board._board[ant.x][ant.y] = 1
            else:
                new_board._board[ant.x][ant.y] = 2
        text = ''
        return  new_board._board

"""
a = Game(20,20)
a.create_environment([], [(16,15),(18,16),(16,17),(17,17),(18,18),(17,18)])
a.create_base([(11,11),(11,12),(12,12),(12,11)])
a.create_colony(8, 100)
for _ in range(100):
    print(a)
    a.run()
    time.sleep(2)
a = Game(100,100)
a.create_environment([], [(20,25),(20,26),(20,27),(22,25),(29,28),(28,28),(25,25),(26,26),(25,27)])
a.create_base([(51,51),(51,52),(52,52),(50,50),(52,51),(53,51),(53,52)])
"""
"""
"""
a = Game(100,100)
havka = [(x,y) for x in range(10,20) for y in range(10,20)] + [(x,y) for x in range(80,90) for y in range(80,90)]
a.create_environment([], havka)
a.create_base([(x,y) for x in range(45,55) for y in range(45,55)])
a.create_colony(50, 600)
for i in range(3000):
    a.run()
    visualisation.draw_board(visualisation.fire_screen, a.str(), a.n, a.m, visualisation.FIRESCREEN_WIDTH/a.n)
    #print(a.pheromone_base_board._board)
    #print()
    #time.sleep(0.1)
with open('test.txt','w') as file:
    text = ''
    #for i in a.pheromone_food_board._board:
    for i in Ant.board._board:
        for elem in i:
            text += str(round(elem,1))
            text += ' '
        text += '\n'
    file.write(text)
print(Ant.ant_z)