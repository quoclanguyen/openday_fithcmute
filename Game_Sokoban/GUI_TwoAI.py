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
import pygame

_ROOT = os.path.abspath(os.path.dirname(__file__))
FILE_MAP = "map/level6.txt"


def update_file_map(new_file_map):
    global FILE_MAP
    FILE_MAP = new_file_map


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
        self.is_running = True

        #self.open_file_level(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))

        # Kích thước ô trong trò chơi (đơn vị pixel)
        self.CELL_SIZE = 50

        self.title("Sokoban")
        self.geometry(
            f"{19 * self.CELL_SIZE + 300}x{11 * self.CELL_SIZE}")
        
        self.label_pvp = tk.Label(self, text="AI vs AI", font=("Helvetica", 16))
        self.label_pvp.pack(side="top", pady=10)

        self.frame_AI1 = tk.Frame(self)  # Tạo main frame
        self.frame_AI1.pack(side="left")

        self.canvas_AI1 = tk.Canvas(self.frame_AI1, width=len(self.GAME_MAP_1.state[0]) * self.CELL_SIZE,
                                height=len(self.GAME_MAP_1.state) * self.CELL_SIZE, background='white')
        self.canvas_AI1.pack(side="right")

        # Dropdown cho AI 1
        self.label_AI1 = tk.Label(self.frame_AI1, text="AI 1", font=("Times", 12, "bold"), background="white", anchor="center")
        self.label_AI1.pack()
        self.label_step_AI1 = tk.Label(self.frame_AI1, text="Steps: 0", font=("Times", 12, "bold"), background="white", anchor="center")
        self.label_step_AI1.pack()
        self.algorithm_choice_AI1 = ttk.Combobox(self.frame_AI1, values=["BFS", "DFS", "UCS", "IDS", "Greedy Search", "A Star","Hill Climbing","Beam Search"])
        self.algorithm_choice_AI1.pack(side="left")
        self.algorithm_choice_AI1.set("Choose algorithm AI1")


        self.frame_AI2 = tk.Frame(self)  # Tạo main frame
        self.frame_AI2.pack(side="right")
        self.canvas_AI2 = tk.Canvas(self.frame_AI2, width=len(self.GAME_MAP_2.state[0]) * self.CELL_SIZE,
                                        height=len(self.GAME_MAP_2.state) * self.CELL_SIZE, background='white')
        self.canvas_AI2.pack(side="left")

        # Dropdown cho AI 2
        self.label_AI2 = tk.Label(self.frame_AI2, text="AI 2", font=("Times", 12, "bold"), background="white", anchor="center")
        self.label_AI2.pack(side="top")
        self.label_step_AI2 = tk.Label(self.frame_AI2, text="Steps: 0", font=("Times", 12, "bold"), background="white", anchor="center")
        self.label_step_AI2.pack(side="top")
        self.algorithm_choice_AI2 = ttk.Combobox(self.frame_AI2, values=["BFS", "DFS", "UCS", "IDS", "Greedy Search", "A Star","Hill Climbing","Beam Search"])
        self.algorithm_choice_AI2.pack(side="right")
        self.algorithm_choice_AI2.set("Choose algorithm AI2")


        self.images = {}
        self.step_counter = -1

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="top", fill="x")
        
        self.stop_button = tk.Button(self.control_frame, text="Stop", borderwidth=3,
                                     width=10, height=2, background="yellow", fg="black", command=self.stop)

        self.stop_button.pack(side="bottom")
        
        # Nút Back
        self.back_button = tk.Button(self.control_frame, text="Back Home", borderwidth=3, width=10, height=2,
                                      background="red", fg="white", command=self.back_to_home)
        self.back_button.pack(side="bottom")

        # Nút Restart
        self.restart_button = tk.Button(self.control_frame, text="Restart", borderwidth=3, width=10, height=2,
                                        background="green", fg="white", command=self.restart_game)
        self.restart_button.pack(side="bottom")
        # Nút Start
        self.start_button = tk.Button(self.control_frame, text="Start", borderwidth=3, width=10, height=2,
                                      background="orange", fg="white", command=self.start_game)
        self.start_button.pack(side="bottom")
        tk.Label(self.control_frame, text="  ").pack(side="bottom")


        n = tk.StringVar()
        self.choosenLevel = ttk.Combobox(self.control_frame, width = 15, textvariable = n, state="readonly")
        levels =[]
        for i in range(1,16):
            levels.append("level{}".format(i))
        self.choosenLevel['values'] = tuple(levels)
        self.choosenLevel.pack(side="top")
        self.choosenLevel.current(0)
        self.choosenLevel.bind("<<ComboboxSelected>>", self.on_level_select)

        self.draw_game_map_1()
        self.draw_game_map_2()
        
    def stop(self):
        self.is_running = False
        
    def restart_game(self):

        # Hiển thị hộp thoại xác nhận
        response = messagebox.askyesno("Xác nhận", "Bạn có muốn restart lại trò chơi không?")
        if response:  # Nếu người dùng chọn "Có"
            # Đặt lại trạng thái trò chơi
            global FILE_MAP
            self.algorithm_running = False
            self.game_started = False
            # Đặt lại bản đồ trò chơi và cập nhật canvas
            self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
            self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))
            self.draw_game_map_1()
            self.draw_game_map_2()
            self.label_step_AI1.config(text=f"Steps: 0")
            self.label_step_AI2.config(text=f"Steps: 0")
        
    def back_to_home(self):
        self.destroy()  # Đóng cửa sổ SokobanGame
        start_GUI_Start()  # Mở cửa sổ GUI_Start

    def on_level_select(self,event):
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
        self.canvas_AI1.delete("all")
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
                    self.canvas_AI1.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_AI1.image = image
        self.update()

    def draw_game_map_2(self):

        self.canvas_AI2.delete("all")
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
                    self.canvas_AI2.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_AI2.image = image
        self.update()

    def start_game(self):
        # Hàm xử lý khi nhấn nút Start
        algorithm1 = self.algorithm_choice_AI1.get()
        algorithm2 = self.algorithm_choice_AI2.get()
        # Thực hiện các hành động dựa trên lựa chọn thuật toán ở đây
        self.solve(algorithm1, algorithm2, 0.2)
            
    def solve(self, AI1, AI2 ,timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        if AI1 == "BFS":
            result1, cell_count1 = bfs_search(self.GAME_MAP_1)
        elif AI1 == "DFS":
            result1, cell_count1 = dfs_search(self.GAME_MAP_1)
        elif AI1 == "IDS":
            result1, cell_count1 = ids_search(self.GAME_MAP_1, 5)
        elif AI1 == "UCS":
            result1, cell_count1 = ucs_search(self.GAME_MAP_1)
        elif AI1 == "Greedy Search":
            result1, cell_count1 = greedy_search(self.GAME_MAP_1)
        elif AI1 == "A Star":
            result1, cell_count1 = astar_search(self.GAME_MAP_1)
        elif AI1 == "Hill Climbing":
            result1, cell_count1 = hill_climbing(self.GAME_MAP_1)
        elif AI1 == "Beam Search":
            result1, cell_count1 = BeamSearch(self.GAME_MAP_1, 2)
        else:
            result1, cell_count1 = None, None 
            
        if AI2 == "BFS":
            result2, cell_count2 = bfs_search(self.GAME_MAP_2)
        elif AI2 == "DFS":
            result2, cell_count2 = dfs_search(self.GAME_MAP_2)
        elif AI2 == "IDS":
            result2, cell_count2 = ids_search(self.GAME_MAP_2, 5)
        elif AI2 == "UCS":
            result2, cell_count2 = ucs_search(self.GAME_MAP_2)
        elif AI2 == "Greedy Search":
            result2, cell_count2 = greedy_search(self.GAME_MAP_2)
        elif AI2 == "A Star":
            result2, cell_count2 = astar_search(self.GAME_MAP_2)
        elif AI2 == "Hill Climbing":
            result2, cell_count2 = hill_climbing(self.GAME_MAP_2)
        elif AI2 == "Beam Search":
            result2, cell_count2 = BeamSearch(self.GAME_MAP_2, 2)
        else:
            result2, cell_count2 = None, None 
            
        if result1 == None or result2 == None:
            messagebox.showinfo("Problem", "No path found for either or both AI !")
            return
        step1 = len(result1.path)
        step2 = len(result2.path)
        result1.path = self.copy_until_size_match(result1.path,result2.path)
        result2.path = self.copy_until_size_match(result2.path,result1.path)
        self.is_running = True
        for sokoban1, sokoban2 in zip(result1.path, result2.path):
            if not self.algorithm_running:
                break
            self.GAME_MAP_1= sokoban1
            self.GAME_MAP_2= sokoban2
            self.draw_game_map_1()
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP_1= Sokoban(self.GAME_MAP_1.state)
                self.GAME_MAP_2= Sokoban(self.GAME_MAP_2.state)
                break
        self.label_step_AI1.config(text=f"Steps: {step1}")
        self.label_step_AI2.config(text=f"Steps: {step2}")
        if step1 > step2:
            messagebox.showinfo("Congratulations", "AI 2 win !!")
        elif step1 < step2:
            messagebox.showinfo("Congratulations", "AI 1 win !!")
        else:
            messagebox.showinfo("Congratulations", "AI 1 and AI 2 draw !!")
        
    def copy_until_size_match(self, A, B):
        while len(A) < len(B):
            A.append(A[-1])
        return A



def main():
    game = SokobanGame()
    game.mainloop()
    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()