import sys
from enemy_class import *
from settings import *

pygame.init()
vec = pygame.math.Vector2


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # a display object displaying the game screen
        self.clock = pygame.time.Clock()    # clock object responsible for the game automation
        self.running = True                 # indicator that the game is running
        self.state = 'start'                # default state of the game
        self.cell_width = MAZE_WIDTH//28    # width of the game maze
        self.cell_height = MAZE_HEIGHT//30  # height of the game maze
        pygame.display.set_caption('PACMAN')
        self.walls = []                     # a list of wall positions
        self.coins = []                     # a list of coin positions
        self.enemies = []                   # a list of Enemy objects
        self.enemy_pos = []                 # a list of Enemy positions
        self.player_pos = None              # player's position

        self.load_background()

        self.player = Player(self, vec(self.player_pos))    # Player object

        self.make_enemies()

# run loop

    # function working as the main loop of the game
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'victory':
                self.victory_events()
                self.victory_update()
                self.victory_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# helper functions

    # function putting desired text out on the game screen
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.Font(font_name, size)
        text = font.render(words, True, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    # function loading the maze.png and map.txt files in order to create the game environment
    def load_background(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # opening file and creating walls list with wall coordinates
        with open("map.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx,yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.player_pos = vec(xidx, yidx)
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_pos.append(vec(xidx, yidx))

    # function filling the list of enemies with Enemy class objects
    def make_enemies(self):
        for idx, pos in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self, vec(pos), idx, self.player))

    # function drawing a grid of the maze on screen; not used in the final game but rather used during creating it
    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GRAY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GRAY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))

    # function used to reset the map and the state of the game
    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("map.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))

        with open('score.txt') as file:
            self.previous_score = file.readline()
            file.close()

        self.state = "playing"

    # function used to remove one of the player’s life and check whether they can continue the game or not.
    # In case of the player being able to continue, the function resets their position and the position of the enemies
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    # function used to draw coin sprites on the screen
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE,
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 3)

# start functions

    # function making use of PyGame events in order to make the program responsive
    # to keyboard inputs during the start state
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    # function loading the score.txt file and loading the previous player’s score into a variable
    def start_update(self):
        with open('score.txt', "r") as file:
            self.previous_score = file.readline()
            file.close()

    # function drawing text on the screen
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PREVIOUS SCORE: {}'.format(self.previous_score), self.screen, [60, 0], START_TEXT_SIZE,
                       WHITE, TEXT_FONT, centered=False)
        self.draw_text('THE PACMAN', self.screen, [WIDTH // 2, 150], TITLE_TEXT_SIZE,
                       RED, TEXT_FONT, centered=True)
        self.draw_text('PRESS SPACE TO START', self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE,
                       YELLOW, TEXT_FONT, centered=True)
        self.draw_text('1 PLAYER', self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE,
                       CYAN, TEXT_FONT, centered=True)
        self.draw_text('© 2022 Dominik Bański', self.screen, [WIDTH // 2, HEIGHT - TOP_BOTTOM_BUFFER], FOOTER_TEXT_SIZE,
                       PURPLE, TEXT_FONT, centered=True)
        pygame.display.update()

# playing functions

    # function making use of PyGame events in order to make the program responsive
    # to keyboard inputs during the playing state
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    # function responsible for updating the elements of the game such as the state of the player,
    # the state of the enemies, whether the player got hit by the enemy or have collected all the coins
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

        if self.coins == []:
            self.state = 'victory'

    # function drawing the game environment and sprites on the screen
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], START_TEXT_SIZE, WHITE, TEXT_FONT,
                       centered=False)
        self.draw_text('PREVIOUS SCORE: {}'.format(self.previous_score), self.screen, [WIDTH // 2 + 60, 0], 18, WHITE, TEXT_FONT, centered=False)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

# game over functions

    # function making use of PyGame events in order to make the program responsive
    # to keyboard inputs during the game over state
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    # function loading the score.txt file and saving the player’s score into it
    def game_over_update(self):
        with open('score.txt', "w") as file:
            file.write(str(self.player.current_score))
            file.close()

    # function drawing text on the screen
    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], 52, RED, TEXT_FONT, centered=True)
        self.draw_text(again_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, (190, 190, 190), TEXT_FONT, centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, (190, 190, 190), TEXT_FONT, centered=True)
        pygame.display.update()

# victory functions

    # function making use of PyGame events in order to make the program responsive
    # to keyboard inputs during the victory state
    def victory_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    # function loading the score.txt file and saving the player’s score into it
    def victory_update(self):
        with open('score.txt', "w") as file:
            file.write(str(self.player.current_score))
            file.close()

    # function drawing text on the screen
    def victory_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("VICTORY", self.screen, [WIDTH // 2, 100], 52, RED, TEXT_FONT, centered=True)
        self.draw_text(again_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, (190, 190, 190), TEXT_FONT, centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, (190, 190, 190), TEXT_FONT, centered=True)
        pygame.display.update()
