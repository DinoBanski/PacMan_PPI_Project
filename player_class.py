import pygame.time
from pygame.math import Vector2 as vec
from settings import *
import time


class Player:
    def __init__(self, app, pos):
        self.app = app      # Game object
        self.starting_pos = [pos.x, pos.y]  # Player's starting position
        self.grid_pos = pos     # Player's position on the invisible grid
        self.pix_pos = self.get_pix_pos()   # Player's position on the screen
        self.direction = vec(1, 0)      # Vector of Player's direction
        self.stored_direction = None    # Player's stored vector of directon
        self.able_to_move = True    # Indicator whether the Player is able to move or not
        self.current_score = 0      # Player's current score
        self.speed = 2      # Player's speed
        self.lives = 3      # Player's number of lives

    # function responsible for updating the state elements of the player such as their speed,
    # ability to move, position on the grid etc.
    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        if self.on_coin():
            self.eat_coin()

    # function drawing the player’s sprite and the sprites representing the amount of the player’s lives on the scree
    def draw(self):
        pygame.draw.circle(self.app.screen, YELLOW,
                           (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width//2-1)

        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, YELLOW, (30 + 20*x, HEIGHT - 15), 7)

    # function moving the player’s sprite in one of the four directions
    def move(self, direction):
        self.stored_direction = direction

    # function calculating the vector which represents the player’s position on the screen
    # based on their position on the invisible grid
    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

    # function determining whether the player is able to move or not based on their position on the invisible grid
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    # function determining whether the player is able to move or not based on their position
    # relative to the position of the maze walls
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    # function determining whether the player made contact with the coin sprite on the map or not
    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    # function removing the coin object from the list consequently removing the coin sprite from the map
    # as well as adding it to the player’s score
    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

