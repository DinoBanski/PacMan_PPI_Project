import random

from player_class import *
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number, player):
        self.app = app                      # Game object
        self.grid_pos = pos                 # Enemy's position on the grid
        self.player = player                # Player object
        self.starting_pos = [pos.x, pos.y]  # Enemy's starting position
        self.pix_pos = self.get_pix_pos()   # Enemy's position on the screen
        self.radius = int(self.app.cell_width // 2.3)  # Enemy's sprite radius
        self.number = number    # Enemy's identification number
        self.direction = vec(0, 0)      # Enemy's vector of direction
        self.personality = self.set_personality()   # Enemy's personality type
        self.target = None      # Enemy's target coordinates
        self.speed = self.set_speed()       # Enemy's speed

    # function responsible for updating the state elements of the enemy such as its speed,
    # ability to move, position on the grid etc.
    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    # function drawing the enemy sprite on the screen with each colour being dependant of its set number
    def draw(self):
        if self.number == 0:
            pygame.draw.circle(self.app.screen, RED, (int(self.pix_pos.x), int(self.pix_pos.y)), 10)
        elif self.number == 1:
            pygame.draw.circle(self.app.screen, CYAN, (int(self.pix_pos.x), int(self.pix_pos.y)), 10)
        elif self.number == 2:
            pygame.draw.circle(self.app.screen, PURPLE, (int(self.pix_pos.x), int(self.pix_pos.y)), 10)
        elif self.number == 3:
            pygame.draw.circle(self.app.screen, GREEN, (int(self.pix_pos.x), int(self.pix_pos.y)), 10)

    # function setting the enemy’s personality based on its number
    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

    # function setting the enemy’s speed based on it’s personality
    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    # function responsible for setting the enemy’s target based on its personality.
    # If the personality is set to scared the enemy is programmed to target the position furthest from them playe
    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:  # scared
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)
            if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    # function determining whether the enemy is able to move or not based on their position on the invisible grid
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    #  function setting the enemy’s moving algorithm based on its set personality
    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_dir()
        elif self.personality == "slow":
            self.direction = self.get_path_dir(self.target)
        elif self.personality == "speedy":
            self.direction = self.get_path_dir(self.target)
        elif self.personality == "scared":
            self.direction = self.get_path_dir(self.target)

    # function calculating the direction vector of the enemy based on the next available cell in its path
    def get_path_dir(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vec(x_dir, y_dir)

    # function looking for the next available cell on the map using the Breadth-First Search algorithm
    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)],
                        [int(target[0]), int(target[1])])
        return path[1]

    # Bread-First Search algorithm used for traversing the list of all grid cells coordinates
    # and searching the shortest possible path to the set target
    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    # a function randomising the direction in which the enemy will move
    def get_random_dir(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    # function calculating the vector which represents the enemy’s position on the screen based on
    # their position on the invisible grid
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

