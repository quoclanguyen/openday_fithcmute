# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:18:34 2023

@author: DELL
"""
from tkinter import messagebox
import copy

class Level(object):
    wall = '#'
    box = 'b'
    box_target = 'g'
    box_on_target = 'x'
    player = 'p'
    player_on_target = 'u'
    
class Sokoban:
    def __init__(self, sokoban, depth=0, path = [], cost = 0, heuristic = 0, player_pos = None, stack = None):
        self.state = sokoban
        if player_pos is None:
            for y, row in enumerate(self.state):
                for x, cell in enumerate(row):
                    if cell == Level.player or cell == Level.player_on_target:
                        self.player_pos = (x, y)
        else:
            self.player_pos = player_pos
        self.depth = depth 
        self.path = path
        self.cost = cost
        self.cost_astar = 0
        self.heuristic_value = self.heuristic_calculate()
        if stack is None:
            self.stack = [(self.state)]
        else:
            self.stack = stack
    
    def move_player(self, dx, dy, SokobanGame = None):
        x, y = self.player_pos
        new_map = [list(row) for row in self.state]
        # for row in self.state:
        #     print(row)
        # print()
        cell = new_map[y][x]
        new_x, new_y = x + dx, y + dy
        new_cell = new_map[new_y][new_x]
        if new_cell == Level.wall:
            return  
        
        elif new_cell == Level.box_target:
            if cell == Level.player_on_target:
                new_map[y][x] = Level.box_target
            elif cell == Level.player:
                new_map[y][x] = '0'
            new_map[new_y][new_x] = Level.player_on_target
            self.player_pos = (new_x, new_y)
            
        elif new_cell == '0':
            if cell == Level.player:
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = Level.box_target
            new_map[new_y][new_x] = Level.player
            self.player_pos = (new_x, new_y)
            
        elif new_cell == Level.box or new_cell == Level.box_on_target:
            new_x2, new_y2 = new_x + dx, new_y + dy
            new_cell_next = new_map[new_y2][new_x2]
            if new_cell_next == Level.box_on_target or new_cell_next == Level.box or new_cell_next == Level.wall:
                return
            if cell == Level.player:
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = Level.box_target
            if new_cell == Level.box_on_target:
                new_map[new_y][new_x] = Level.player_on_target
                self.player_pos = (new_x, new_y)
            else:
                new_map[new_y][new_x] = Level.player
                self.player_pos = (new_x, new_y)
            if new_cell_next == '0':
                new_map[new_y2][new_x2] = Level.box
            elif new_cell_next == Level.box_target:
                new_map[new_y2][new_x2] = Level.box_on_target
            
        self.state = ["".join(r) for r in new_map]
        self.stack.append(copy.copy(self.state))

        if SokobanGame is not None:
            SokobanGame.draw_game_map()

    def move_player_1(self, dx, dy, SokobanGame=None):
        x, y = self.player_pos
        new_map = [list(row) for row in self.state]
        # for row in self.state:
        #     print(row)
        # print()
        cell = new_map[y][x]
        new_x, new_y = x + dx, y + dy
        new_cell = new_map[new_y][new_x]
        if new_cell == Level.wall:
            return

        elif new_cell == Level.box_target:
            if cell == Level.player_on_target:
                new_map[y][x] = Level.box_target
            elif cell == Level.player:
                new_map[y][x] = '0'
            new_map[new_y][new_x] = Level.player_on_target
            self.player_pos = (new_x, new_y)

        elif new_cell == '0':
            if cell == Level.player:
                new_map[y][x] = '0'
            else:
                new_map[y][x] = Level.box_target
            new_map[new_y][new_x] = Level.player
            self.player_pos = (new_x, new_y)

        elif new_cell == Level.box or new_cell == Level.box_on_target:
            new_x2, new_y2 = new_x + dx, new_y + dy
            new_cell_next = new_map[new_y2][new_x2]
            if new_cell_next == Level.box_on_target or new_cell_next == Level.box or new_cell_next == Level.wall:
                return
            if cell == Level.player:
                new_map[y][x] = '0'
            else:
                new_map[y][x] = Level.box_target
            if new_cell == Level.box_on_target:
                new_map[new_y][new_x] = Level.player_on_target
                self.player_pos = (new_x, new_y)
            else:
                new_map[new_y][new_x] = Level.player
                self.player_pos = (new_x, new_y)
            if new_cell_next == '0':
                new_map[new_y2][new_x2] = Level.box
            elif new_cell_next == Level.box_target:
                new_map[new_y2][new_x2] = Level.box_on_target

        self.state = ["".join(r) for r in new_map]
        self.stack.append(copy.copy(self.state))

        if SokobanGame is not None:
            SokobanGame.draw_game_map_1()

    def move_player_2(self, dx, dy, SokobanGame=None):
        x, y = self.player_pos
        new_map = [list(row) for row in self.state]
        # for row in self.state:
        #     print(row)
        # print()
        cell = new_map[y][x]
        new_x, new_y = x + dx, y + dy
        new_cell = new_map[new_y][new_x]
        if new_cell == Level.wall:
            return

        elif new_cell == Level.box_target:
            if cell == Level.player_on_target:
                new_map[y][x] = Level.box_target
            elif cell == Level.player:
                new_map[y][x] = '0'
            new_map[new_y][new_x] = Level.player_on_target
            self.player_pos = (new_x, new_y)

        elif new_cell == '0':
            if cell == Level.player:
                new_map[y][x] = '0'
            else:
                new_map[y][x] = Level.box_target
            new_map[new_y][new_x] = Level.player
            self.player_pos = (new_x, new_y)

        elif new_cell == Level.box or new_cell == Level.box_on_target:
            new_x2, new_y2 = new_x + dx, new_y + dy
            new_cell_next = new_map[new_y2][new_x2]
            if new_cell_next == Level.box_on_target or new_cell_next == Level.box or new_cell_next == Level.wall:
                return
            if cell == Level.player:
                new_map[y][x] = '0'
            else:
                new_map[y][x] = Level.box_target
            if new_cell == Level.box_on_target:
                new_map[new_y][new_x] = Level.player_on_target
                self.player_pos = (new_x, new_y)
            else:
                new_map[new_y][new_x] = Level.player
                self.player_pos = (new_x, new_y)
            if new_cell_next == '0':
                new_map[new_y2][new_x2] = Level.box
            elif new_cell_next == Level.box_target:
                new_map[new_y2][new_x2] = Level.box_on_target

        self.state = ["".join(r) for r in new_map]
        self.stack.append(copy.copy(self.state))

        if SokobanGame is not None:
            SokobanGame.draw_game_map_2()
    def is_complete(self):
        for row in self.state:
            if 'b' in row:
                return False
        return True
    
    def generate_moves(self):
        x, y = self.player_pos
        moves =[]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for direction in directions:
            x_new, y_new = x + direction[0], y + direction[1]
            # Kiểm tra xem người chơi có thể di chuyển đến vị trí mới hay không
            if self.is_valid_move(x_new,y_new):
                new_sokoban = copy.copy(self)
                new_sokoban.move_player(direction[0], direction[1])
                new_sokoban.depth = self.depth + 1
                new_sokoban.heuristic_value = new_sokoban.heuristic_calculate()
                moves.append(new_sokoban)

        return moves
    
    def is_valid_move(self, col, row):
        if (
            0 <= row < len(self.state) and
            0 <= col < len(self.state[row]) and
            self.state[row][col] != Level.wall
        ):
            return True
        return False

    def heuristic_calculate(self):
        box_positions = self.get_box_positions()
        target_positions = self.get_target_positions()

        heuristic_value = 0
        for box_pos in box_positions:
            min_distance = float('inf')
            for target_pos in target_positions:
                distance = abs(box_pos[0] - target_pos[0]) + abs(box_pos[1] - target_pos[1])
                min_distance = min(min_distance, distance)
            heuristic_value += min_distance
        return heuristic_value

    def get_box_positions(self):
        box_positions = []
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                if cell == Level.box or cell == Level.box_on_target:
                    box_positions.append((x, y))
        return box_positions

    def get_target_positions(self):
        target_positions = []
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                if cell == Level.box_target or cell == Level.box_on_target or cell == Level.player_on_target:
                    target_positions.append((x, y))
        return target_positions
    
        