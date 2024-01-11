from MazeAIGUI import MazeAIGUI
from MazePlayerGUI import MazePlayerGUI
import pygame
class MazeApp:
    def __init__(self, size, width, height, mode, bg_music):
        self.margin = 1
        self.width = width
        self.height = height
        self.mode = mode
        bg_music.stop()
        self.game_music = pygame.mixer.Sound("./sound/game.mp3")
        self.game_music.play(-1)
        self.size = size
        self.gridHeight = round((self.height - self.margin) / self.size) - self.margin
        if self.mode == "ai":
            self.app = MazeAIGUI(self.width, self.height, self.margin, self.size, 'Maze Project', self.game_music)
            self.app.setGridSize(self.gridHeight, self.gridHeight)
            self.app.mainLoop()
        else:
            self.app = MazePlayerGUI(self.width, self.height, self.margin, self.size, 'Maze Project', self.game_music)
            self.app.setGridSize(self.gridHeight, self.gridHeight)
            self.app.mainLoop()
