import pygame
import sys
import random


FPS = 60
W = 1024
H = 1024 
TileSize = 32

WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

window = pygame.display.set_mode((W, H), pygame.SRCALPHA, 32)
clock = pygame.time.Clock()

class Maze:

    def __init__(self, maze_layout):
        layout_file = open(maze_layout)
        temp_layout = layout_file.read()
        layout_file.close()
        self.layout = []
        for i in range(20):
            self.layout.append(temp_layout[i])
        self.curr_room = 0

    def get_first_room(self):
        new_room = Room(floor_image='./resources/background/white_stone.jpg', wall_image='./resources/walls/wall.jpg',
                        lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/B_room_layout.txt')
        return new_room        
        
    def get_next_room(self, direction):
        if direction == 'right':
            self.curr_room += 1
        elif direction == 'left':
            self.curr_room -= 1
        if self.layout[self.curr_room] == 'A':
            new_room = Room(floor_image='./resources/background/black_stone.jpg', wall_image='./resources/walls/wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/A_room_layout.txt')
        elif self.layout[self.curr_room] == 'B':
            new_room = Room(floor_image='./resources/background/white_stone.jpg', wall_image='./resources/walls/wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/B_room_layout.txt')
        elif self.layout[self.curr_room] == 'C':
            new_room = Room(floor_image='./resources/background/black_stone.jpg', wall_image='./resources/walls/wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/C_room_layout.txt')
        elif self.layout[self.curr_room] == 'D':
            new_room = Room(floor_image='./resources/background/white_stone.jpg', wall_image='./resources/walls/ice_wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/D_room_layout.txt')
        elif self.layout[self.curr_room] == 'E':
            new_room = Room(floor_image='./resources/background/black_stone.jpg', wall_image='./resources/walls/wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/E_room_layout.txt')
        elif self.layout[self.curr_room] == 'F':
            new_room = Room(floor_image='./resources/background/black_stone.jpg', wall_image='./resources/walls/wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/F_room_layout.txt')
        elif self.layout[self.curr_room] == 'G':
            new_room = Room(floor_image='./resources/background/white_stone.jpg', wall_image='./resources/walls/ice_wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/G_room_layout.txt')
        elif self.layout[self.curr_room] == 'H':
            new_room = Room(floor_image='./resources/background/white_stone.jpg', wall_image='./resources/walls/ice_wall.jpg',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/H_room_layout.txt')
        elif self.layout[self.curr_room] == 'I':
            new_room = Room(floor_image='./resources/background/grass.jpg', wall_image='./resources/walls/tree.png',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/I_room_layout.txt')
        elif self.layout[self.curr_room] == 'J':
            new_room = Room(floor_image='./resources/background/grass.jpg', wall_image='./resources/walls/tree.png',
                            lava_image='./resources/traps/lava.png', room_layout='./resources/rooms_layout/J_room_layout.txt')                   
        return new_room    

    def get_direction(self, x, y):
        if x > 800:
            return 'right'
        elif x < 200:
            return 'left'

    def get_enemy(self):
        if self.curr_room == 1:
            return Ghost('./resources/characters/ghost.png', 312, 512)
        elif self.curr_room == 3:
            return SmartGhost('./resources/characters/ghost.png', 512, 512)
        elif self.curr_room == 6:
            return Ghost('./resources/characters/ghost.png', 812, 512)
        elif self.curr_room == 10:
            return SmartGhost('./resources/characters/ghost.png', 512, 512)
        elif self.curr_room == 13:
            return SmartGhost('./resources/characters/ghost.png', 512, 512)               
        else:
            return None                                  



class Room:

    def __init__(self, floor_image, wall_image, lava_image, room_layout):
        self.wall_image = pygame.image.load(wall_image)
        self.floor_image = pygame.image.load(floor_image)
        self.lava_image = pygame.image.load(lava_image)
        self.treasure = pygame.image.load('./resources/another_static/treasure.png')
        self.stake = Stakes()
        layout_file = open(room_layout)
        temp_layout = layout_file.read()
        layout_file.close()
        self.layout = []
        for i in range(TileSize):
            self.layout.append([])
            for j in range(TileSize):
                self.layout[i].append(temp_layout[i*TileSize+i+j])

    def draw(self):
        window.blit(self.floor_image, (0, 0))
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                if self.layout[i][j] == '#':
                    window.blit(self.wall_image, (TileSize*j, TileSize*i))
                elif self.layout[i][j] == 'T':
                    window.blit(self.lava_image, (TileSize*j, TileSize*i))
                elif self.layout[i][j] == ' ':
                    pygame.draw.rect(window, BLACK, (TileSize*j, TileSize*i, TileSize, TileSize))
                elif self.layout[i][j] == 'Q':
                    pygame.draw.rect(window, WHITE, (TileSize*j, TileSize*i, TileSize, TileSize))
                elif self.layout[i][j] == '!':
                    self.stake.draw(TileSize*j, TileSize*i)
                elif self.layout[i][j] == '*':
                    window.blit(self.treasure, (TileSize*j, TileSize*i))             
                        

    def is_legal_move(self, current_tiles):
        for tile in current_tiles:
            if (self.layout[tile[1]][tile[0]] == '#'):
                return False
            elif (self.layout[tile[1]][tile[0]] == '*'):
                return False           
        return True

    def is_exit(self, current_tiles):
        for tile in current_tiles:
            if (self.layout[tile[1]][tile[0]] != 'x'):
                return False
        return True

    def is_lava(self, current_tiles):
        for tile in current_tiles:
            if (self.layout[tile[1]][tile[0]] == 'T'):
                return True
        return False

    def is_space(self, current_tiles):
        for tile in current_tiles:
            if (self.layout[tile[1]][tile[0]] == ' '):
                return True
        return False

    def is_victory_position(self, current_tiles):
        for tile in current_tiles:
            if (self.layout[tile[1]][tile[0]] == 'Q'):
                return True
        return False

    def is_stake_kill_player(self, current_tiles):
        for tile in current_tiles:
            if (self.layout[tile[1]][tile[0]] == '!'):
                return self.stake.is_kill_player()
        return False    

    def get_start_position(self):
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                if self.layout[i][j] == '@':
                    return j*TileSize, i*TileSize


class Enemy:
    
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.speed = 4

    def is_collision_with_player(self, player_x, player_y):
        if (player_x <= self.x <= player_x + TileSize) and (player_y <= self.y <= player_y + TileSize):
            return True
        if (self.x <= player_x <= self.x + TileSize) and (self.y <= player_y <= self.y + TileSize):
            return True
        return False    

    def draw(self):
        window.blit(self.image, (self.x, self.y))


class Ghost(Enemy):
    
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.direction = 'up'

    def move(self, *args, **kwargs):
        if self.direction == 'up':
            self.y += self.speed
        elif self.direction == 'down':
            self.y -= self.speed
        if (self.y < 100) and (self.direction == 'down'):
            self.direction = 'up'
        elif (self.y > 924) and (self.direction == 'up'):
            self.direction = 'down'


class SmartGhost(Enemy):
    
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def move(self, player_x, player_y):
        x_dist = self.x - player_x
        y_dist = self.y - player_y
        if abs(x_dist) - abs(y_dist) > 0:
            if x_dist > 0:
                self.x -= self.speed
            else:
                self.x += self.speed 
        else:
            if y_dist > 0:
                self.y -= self.speed
            else:
                self.y += self.speed


class Stakes:

    def __init__(self, img1='./resources/traps/trap1.png', img2='./resources/traps/trap2.png', img3='./resources/traps/trap3.png'):
        self.stake_list = [] 
        self.stake_list.append(pygame.image.load(img1))
        self.stake_list.append(pygame.image.load(img2))
        self.stake_list.append(pygame.image.load(img3))
        self.state = 0
        self.time = 0
        self._timer = 500

    def draw(self, x, y):
        self.time += 1
        if self.time > self._timer:
            self.time = 0
            self.state += 1
            if self.state > 2:
                self.state = 0
        window.blit(self.stake_list[self.state], (x, y))

    def is_kill_player(self):
        if self.state == 2:
            return True
        else:
            return False


class Hearts:

    def __init__(self, img='./resources/another_static/heart.png'):
        self.number_of_lives = 3
        self.heart_img = pygame.image.load(img)

    def draw(self):
        for i in range(self.number_of_lives):
            window.blit(self.heart_img, (TileSize*i, 0))


def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf                  
                           

def current_tiles_calc(x, y):
    current_tiles = [] # массив с номерами текущих тайлов
    tile_x = []
    tile_y = []
    if x % 32 == 0:
        tile_x.append(x//32)
    else:
        tile_x.append(x//32)
        tile_x.append(x//32+1)
    if y % 32 == 0:    
        tile_y.append(y//32)
    else:
        tile_y.append(y//32)
        tile_y.append(y//32+1)
    if (len(tile_x) == 2) and (len(tile_y) == 2):
        current_tiles.append((tile_x[0],tile_y[0]))
        current_tiles.append((tile_x[1],tile_y[0]))
        current_tiles.append((tile_x[0],tile_y[1]))
        current_tiles.append((tile_x[1],tile_y[1]))
    elif (len(tile_x) == 1) and (len(tile_y) == 2):
        current_tiles.append((tile_x[0],tile_y[0]))
        current_tiles.append((tile_x[0],tile_y[1]))
    elif (len(tile_x) == 2) and (len(tile_y) == 1):
        current_tiles.append((tile_x[0],tile_y[0]))
        current_tiles.append((tile_x[1],tile_y[0]))
    elif (len(tile_x) == 1) and (len(tile_y) == 1):
        current_tiles.append((tile_x[0],tile_y[0]))
    return current_tiles


def move(x, y, curr_room, hero, enemy=None):
    if enemy is not None:
        enemy.move(x,y)
        enemy.draw()
    #pygame.draw.rect(window, BLUE, (x, y, TileSize, TileSize))
    window.blit(hero, (x, y))

    pygame.display.update()

    curr_room.draw()
 
    keys = pygame.key.get_pressed()

    x_old = x
    y_old = y

    if keys[pygame.K_a]:
        x -= speed
    elif keys[pygame.K_d]:
        x += speed
    elif keys[pygame.K_w]:
        y -= speed
    elif keys[pygame.K_s]:
        y += speed
    current_tiles = current_tiles_calc(x, y)
    if not curr_room.is_legal_move(current_tiles):
        x, y = x_old, y_old
        current_tiles = current_tiles_calc(x, y)
    if curr_room.is_lava(current_tiles):
        raise Exception("Hero is dead")
    if curr_room.is_space(current_tiles):
        raise Exception("Hero is dead")
    if curr_room.is_stake_kill_player(current_tiles):
        raise Exception("Hero is dead")         
    if curr_room.is_exit(current_tiles):
        raise Exception("Exit from room")
    if curr_room.is_victory_position(current_tiles):
        raise Exception("Exit from maze")
    if enemy is not None:
        if enemy.is_collision_with_player(x, y):
            raise Exception("Hero is dead")     
    return x, y    

   
if __name__ == '__main__':
    maze = Maze('maze_layout.txt')

    hero = pygame.image.load('./resources/characters/knight1.png')

    lives = Hearts()

    hero_is_dead = False
    is_victory = False

    curr_room = maze.get_first_room()

    x, y = curr_room.get_start_position()

    speed = 8

    enemy = None

    particles = []

    while True:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()          

        if not hero_is_dead:        
            try:
                lives.draw()
                x, y = move(x, y, curr_room, hero, enemy)
            except Exception as err:
                if err.args[0] == 'Hero is dead':
                    if lives.number_of_lives == 0: 
                        hero_is_dead = True
                    else:
                        lives.number_of_lives -= 1
                        curr_room = maze.get_first_room()
                        x, y = curr_room.get_start_position()
                        maze.curr_room = 0
                        enemy = maze.get_enemy()
                elif err.args[0] == 'Exit from room':
                    direction = maze.get_direction(x,y)
                    curr_room = maze.get_next_room(direction)
                    enemy = maze.get_enemy()

                    if direction == 'left':
                        x = int(1080 - TileSize*3) # почему-то нельзя ставить 1080 - происходит баг - исчезает персонаж
                    elif direction == 'right':
                        x = 0   
                elif err.args[0] == 'Exit from maze':
                    is_victory = True
                    hero_is_dead = True                  
        else:
            pass
            pygame.font.init()
            myfont = pygame.font.SysFont('Comic Sans MS', 200)
            if is_victory:
                window.fill(BLUE)
                textsurface = myfont.render('Victory', False, WHITE)
                window.blit(textsurface,(250,450))

                mx, my = pygame.mouse.get_pos()
                particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])

                for particle in particles:
                    particle[0][0] += particle[1][0]
                    particle[0][1] += particle[1][1]
                    particle[2] -= 0.1
                    particle[1][1] += 0.15
                    pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

                    radius = particle[2] * 2
                    window.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)

                    if particle[2] <= 0:
                        particles.remove(particle)

            else:
                textsurface = myfont.render('Game over', False, RED)
                window.blit(textsurface,(150,300))

            pygame.display.update()

 
        clock.tick(100)