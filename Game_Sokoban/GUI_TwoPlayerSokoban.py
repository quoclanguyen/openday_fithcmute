import pygame
import tkinter as tk
from tkinter import messagebox

import os
from tkinter import ttk
from PIL import Image, ImageTk
import time

from Game_Sokoban.main import start_GUI_Start
from SokobanState import *
from SolveDFS_IDS import *
from SolveBFS_UCS import *
import time
from SolveGreedy_Astar_Local import *
from tkinter import Label


_ROOT = os.path.abspath(os.path.dirname(__file__))
FILE_MAP = "map/level6.txt"


def update_file_map(new_file_map):
    global FILE_MAP
    FILE_MAP = new_file_map
def create_instruction_label(parent_frame, text):
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 10))
    instruction_label.pack(side="bottom")
    return instruction_label

class Image(object):
    wall = os.path.join(_ROOT, 'images/map_resize/wall.gif')
    box = os.path.join(_ROOT, 'images/map_resize/box.gif')
    box_target = os.path.join(_ROOT, 'images/map_resize/box_target.gif')
    box_on_target = os.path.join(_ROOT, 'images/map_resize/box_on_target.gif')
    player = os.path.join(_ROOT, 'images/map_resize/player.gif')
    player_on_target = os.path.join(_ROOT, 'images/map_resize/player_on_target.gif')


class SokobanGame(tk.Tk):
    def __init__(self):

        super().__init__()

        self.check_use_algorithm = False

        self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))

        self.CELL_SIZE = 50

        self.title("Sokoban")
        # self.geometry(
        #     f"{14 * self.CELL_SIZE + 300}x{8 * self.CELL_SIZE + 200}")
        window_width = 14 * self.CELL_SIZE + 300
        window_height = 8 * self.CELL_SIZE + 200
        self.geometry(f"{window_width}x{window_height}")

        self.label_pvp = tk.Label(self, text="Player vs Player", font=("Helvetica", 16))
        self.label_pvp.pack(side="top", pady=10)


        # Tạo frame chứa map và hướng dẫn cho Player 1
        self.frame_player1 = tk.Frame(self)
        self.frame_player1.pack(side="left", pady=10)  # Thêm pady để tạo khoảng cách giữa frame và map

        self.canvas_player1 = tk.Canvas(self.frame_player1, width=len(self.GAME_MAP_1.state[0]) * self.CELL_SIZE,
                                        height=len(self.GAME_MAP_1.state) * self.CELL_SIZE, background='white')
        self.canvas_player1.pack(side="top")

        self.instruction_label_1 = create_instruction_label(self.frame_player1, "Player 1: Use W, A, S, D to move")

        # Tạo frame chứa map và hướng dẫn cho Player 2
        self.frame_player2 = tk.Frame(self)
        self.frame_player2.pack(side="right", pady=10)  # Thêm pady để tạo khoảng cách giữa frame và map

        self.canvas_player2 = tk.Canvas(self.frame_player2, width=len(self.GAME_MAP_2.state[0]) * self.CELL_SIZE,
                                        height=len(self.GAME_MAP_2.state) * self.CELL_SIZE, background='white')
        self.canvas_player2.pack(side="top")

        self.instruction_label_2 = create_instruction_label(self.frame_player2, "Player 2: Use Arrow keys (Right, Left, Up, Down) to move")

        self.images = {}
        self.step_counter = -1

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="top", fill="x")
        label_select_level = tk.Label(self.control_frame, text="Select level")
        label_select_level.pack(side="top", pady=10)

        n = tk.StringVar()
        self.choosenLevel = ttk.Combobox(self.control_frame, width=20, textvariable=n, state="readonly")
        levels = []
        for i in range(1, 16):
            levels.append("level{}".format(i))
        self.choosenLevel['values'] = tuple(levels)
        self.choosenLevel.current(0)
        self.choosenLevel.bind("<<ComboboxSelected>>", self.on_level_select)
        self.choosenLevel.pack(side="top", pady=5)


        tk.Frame(self.control_frame, height=10).pack()
        # Nút Start
        self.backtohome_button = tk.Button(self.control_frame, text="Back Home", borderwidth=3, width=10, height=2,
                                      background="red", fg="white", command=self.back_to_home)
        self.backtohome_button.pack(side="bottom", pady=5)

        # Nút Restart
        self.restart_button = tk.Button(self.control_frame, text="Restart", borderwidth=3, width=10, height=2,
                                        background="green", fg="white", command=self.restart_game)
        self.restart_button.pack(side="bottom")

        self.draw_game_map_1()
        self.draw_game_map_2()
    def back_to_home(self):
        response = messagebox.askyesno("Xác nhận", "Bạn có muốn thoát chế độ chơi này không?")
        if response:
            self.destroy()  # Đóng cửa sổ SokobanGame
            start_GUI_Start()  # Mở cửa sổ GUI_Start

    def restart_game(self):

        # Hiển thị hộp thoại xác nhận
        response = messagebox.askyesno("Xác nhận", "Bạn có muốn restart lại trò chơi không?")
        if response:  # Nếu người dùng chọn "Có"
            # Đặt lại trạng thái trò chơi
            global FILE_MAP

            # Đặt lại bản đồ trò chơi và cập nhật canvas
            self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
            self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))
            self.draw_game_map_1()
            self.draw_game_map_2()
    def on_level_select(self, event):
        global FILE_MAP
        FILE_MAP = "map/{}.txt".format(self.choosenLevel.get())
        self.focus_set()
        self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))

        self.draw_game_map_1()
        self.draw_game_map_2()


    def open_file_level_1(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]

            self.GAME_MAP_1 = Sokoban(lines)
            for line in self.GAME_MAP_1.state:
                print(line)
        else:
            messagebox.showerror("Sorry", "Không tìm thấy file map level!!")
            self.GAME_MAP_1 = Sokoban([
                "0#####00",
                "#00000#0",
                "#00p00#0",
                "#00000#0",
                "#00b00#0",
                "#00g00#0",
                "#######0",
                "00000000"
            ])

    def open_file_level_2(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]

            self.GAME_MAP_2 = Sokoban(lines)
            for line in self.GAME_MAP_2.state:
                print(line)
        else:
            messagebox.showerror("Sorry", "Không tìm thấy file map level!!")
            self.GAME_MAP_2 = Sokoban([
                "0#####00",
                "#00000#0",
                "#00p00#0",
                "#00000#0",
                "#00b00#0",
                "#00g00#0",
                "#######0",
                "00000000"
            ])
    def draw_game_map_1(self):
        self.canvas_player1.delete("all")
        for y, row in enumerate(self.GAME_MAP_1.state):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                image = None  # Biến để lưu trữ thể hiện của ImageTk.PhotoImage

                if cell == Level.wall:
                    if Image.wall not in self.images:  # Kiểm tra xem đã tạo thể hiện cho hình ảnh này chưa
                        self.images[Image.wall] = ImageTk.PhotoImage(file=Image.wall)
                    image = self.images[Image.wall]
                elif cell == Level.box:
                    if Image.box not in self.images:
                        self.images[Image.box] = ImageTk.PhotoImage(file=Image.box)
                    image = self.images[Image.box]
                elif cell == Level.box_target:
                    if Image.box_target not in self.images:
                        self.images[Image.box_target] = ImageTk.PhotoImage(file=Image.box_target)
                    image = self.images[Image.box_target]
                elif cell == Level.box_on_target:
                    if Image.box_on_target not in self.images:
                        self.images[Image.box_on_target] = ImageTk.PhotoImage(file=Image.box_on_target)
                    image = self.images[Image.box_on_target]
                elif cell == Level.player:

                    if Image.player not in self.images:
                        self.images[Image.player] = ImageTk.PhotoImage(file=Image.player)
                    image = self.images[Image.player]
                elif cell == Level.player_on_target:
                    if Image.player_on_target not in self.images:
                        self.images[Image.player_on_target] = ImageTk.PhotoImage(file=Image.player_on_target)
                    image = self.images[Image.player_on_target]

                if image:
                    self.canvas_player1.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_player1.image = image



        if self.GAME_MAP_1.is_complete():
            messagebox.showinfo("Congratulations", "Player 1 win !!")

    def draw_game_map_2(self):

        self.canvas_player2.delete("all")
        for y, row in enumerate(self.GAME_MAP_2.state):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                image = None  # Biến để lưu trữ thể hiện của ImageTk.PhotoImage

                if cell == Level.wall:
                    if Image.wall not in self.images:  # Kiểm tra xem đã tạo thể hiện cho hình ảnh này chưa
                        self.images[Image.wall] = ImageTk.PhotoImage(file=Image.wall)
                    image = self.images[Image.wall]
                elif cell == Level.box:
                    if Image.box not in self.images:
                        self.images[Image.box] = ImageTk.PhotoImage(file=Image.box)
                    image = self.images[Image.box]
                elif cell == Level.box_target:
                    if Image.box_target not in self.images:
                        self.images[Image.box_target] = ImageTk.PhotoImage(file=Image.box_target)
                    image = self.images[Image.box_target]
                elif cell == Level.box_on_target:
                    if Image.box_on_target not in self.images:
                        self.images[Image.box_on_target] = ImageTk.PhotoImage(file=Image.box_on_target)
                    image = self.images[Image.box_on_target]
                elif cell == Level.player:

                    if Image.player not in self.images:
                        self.images[Image.player] = ImageTk.PhotoImage(file=Image.player)
                    image = self.images[Image.player]
                elif cell == Level.player_on_target:
                    if Image.player_on_target not in self.images:
                        self.images[Image.player_on_target] = ImageTk.PhotoImage(file=Image.player_on_target)
                    image = self.images[Image.player_on_target]

                if image:

                    self.canvas_player2.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_player2.image = image

        if self.GAME_MAP_2.is_complete():
            messagebox.showinfo("Congratulations", "Player 2 win !!")

def main():
    game = SokobanGame()

    def on_key(event):
        # Xử lý đầu vào cho cả hai người chơi
        if event.keysym in ["w", "s", "a", "d"]:
            if event.keysym == "w":
                game.GAME_MAP_1.move_player_1(0, -1, game)
            elif event.keysym == "s":
                game.GAME_MAP_1.move_player_1(0, 1, game)
            elif event.keysym == "a":
                game.GAME_MAP_1.move_player_1(-1, 0, game)
            elif event.keysym == "d":
                game.GAME_MAP_1.move_player_1(1, 0, game)
        elif event.keysym in ["Up", "Down", "Left", "Right"]:
            if event.keysym == "Up":
                game.GAME_MAP_2.move_player_2(0, -1, game)
            elif event.keysym == "Down":
                game.GAME_MAP_2.move_player_2(0, 1, game)
            elif event.keysym == "Left":
                game.GAME_MAP_2.move_player_2(-1, 0, game)
            elif event.keysym == "Right":
                game.GAME_MAP_2.move_player_2(1, 0, game)
    game.bind("<Key>", on_key)
    game.mainloop()
    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()