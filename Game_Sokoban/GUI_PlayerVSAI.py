import pygame
import tkinter as tk
from tkinter import messagebox
import threading
import os
from tkinter import ttk
from PIL import Image, ImageTk
import time

from GUI_Start import start_GUI_Start
from SokobanState import *
from SolveDFS_IDS import *
from SolveBFS_UCS import *
import time
from SolveGreedy_Astar_Local import *

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

def create_instruction_label(parent_frame, text):
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 10))
    instruction_label.pack(side="bottom")
    # Thêm khoảng cách s
    tk.Frame(parent_frame, height=10).pack()
    return instruction_label
class SokobanGame(tk.Tk):
    def __init__(self):

        super().__init__()

        self.is_running = True
        self.check_use_algorithm = False
        self.player_steps = 0
        self.AI_steps = 0
        self.game_started = False
        self.AI_completed = False
        self.Player_completed = False
        self.check_result_algorithm = True
        self.algorithm_running = False
        self.player_win = False
        self.AI_win = False
        self.algorithm_selected =""


        self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))
        self.time_delay_step = 0.1

        self.CELL_SIZE = 50

        self.title("Sokoban")
        self.geometry(
            f"{13 * self.CELL_SIZE + 300}x{10 * self.CELL_SIZE}")

        self.label_pvp = tk.Label(self, text="Player vs AI", font=("Helvetica", 16))
        self.label_pvp.pack(side="top", pady=10)

        self.frame_player = tk.Frame(self)  # Tạo main frame
        self.frame_player.pack(side="left")

        self.canvas_player = tk.Canvas(self.frame_player, width=len(self.GAME_MAP_1.state[0]) * self.CELL_SIZE,
                                height=len(self.GAME_MAP_1.state) * self.CELL_SIZE, background='white')
        self.canvas_player.pack(side="top")

        # Dropdown cho Player 1
        self.label_player = create_instruction_label(self.frame_player, "Player 1: Use W, A, S, D or Arrow keys (Right, Left, Up, Down) to move")



        self.frame_AI = tk.Frame(self)
        self.frame_AI.pack(side="right")
        self.canvas_AI = tk.Canvas(self.frame_AI, width=len(self.GAME_MAP_2.state[0]) * self.CELL_SIZE,
                                        height=len(self.GAME_MAP_2.state) * self.CELL_SIZE, background='white')
        self.canvas_AI.pack(side="top")

        self.label_AI = create_instruction_label(self.frame_AI, "AI")




        self.images = {}
        self.step_counter = -1

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="top", fill="x")

        tk.Frame(self.control_frame, height=20).pack()
        self.comparison_choice = ttk.Combobox(self.control_frame, values=["Step", "Speed"], state="readonly")
        self.comparison_choice.pack(fill="x", expand=True)
        self.comparison_choice.set("Chọn kiểu so sánh")
        self.comparison_choice.bind("<<ComboboxSelected>>", self.on_comparison_choice)

        tk.Frame(self.control_frame, height=10).pack()
        self.algorithm_choice_AI = ttk.Combobox(self.control_frame,
                                                values=["BFS", "DFS", "IDS", "UCS", "Greedy", "A Star", "Hill Climbing",
                                                        "Beam Search"], state="readonly")
        self.algorithm_choice_AI.pack()
        self.algorithm_choice_AI.set("Chọn thuật toán")
        self.algorithm_choice_AI.bind("<<ComboboxSelected>>", self.xu_ly_boi_den)


        self.label_step_player = tk.Label(self.control_frame, text="Steps Player: 0", font=("Times", 12, "bold"), background="white", anchor="center")
        self.label_step_AI = tk.Label(self.control_frame, text="Steps AI: 0", font=("Times", 12, "bold"), background="white", anchor="center")

        self.time_delay = ttk.Combobox(self.control_frame,
                                       values=["0.5", "1", "1.5", "2", "2.5", "3"], state="readonly")
        self.time_delay.pack()

        self.time_delay.set("Thời gian chạy từng bước")
        self.time_delay.bind("<<ComboboxSelected>>", self.xu_ly_boi_den)

        self.time_delay.pack_forget()



        tk.Frame(self.control_frame, height=10).pack()
        n = tk.StringVar()
        self.choosenLevel = ttk.Combobox(self.control_frame, width = 15, textvariable = n, state="readonly")
        levels =[]
        for i in range(1,16):
            levels.append("level{}".format(i))
        self.choosenLevel['values'] = tuple(levels)
        self.choosenLevel.pack(side="top")
        self.choosenLevel.current(0)
        self.choosenLevel.bind("<<ComboboxSelected>>", self.on_level_select)
        # Thêm khoảng cách s
        tk.Frame(self.control_frame, height=10).pack()

        self.restart_button = tk.Button(self.control_frame, text="Restart", borderwidth=3, width=10, height=2,
                                        background="green", fg="white", command=self.restart_game)
        self.restart_button.pack()
        # Thêm khoảng cách s
        tk.Frame(self.control_frame, height=10).pack()
        # Nút Start
        self.start_button = tk.Button(self.control_frame, text="Start", borderwidth=3, width=10, height=2,
                                      background="orange", fg="white", command=self.start_game)

        self.start_button.pack()
        tk.Frame(self.control_frame, height=10).pack()
        # Nút Back
        self.back_button = tk.Button(self.control_frame, text="Back Home", borderwidth=3, width=10, height=2,
                                      background="red", fg="white", command=self.back_to_home)

        self.back_button.pack()
        tk.Frame(self.control_frame, height=10).pack()
        self.stop_button = tk.Button(self.control_frame, text="Stop", borderwidth=3,
                                     width=10, height=2, background="yellow", fg="black", command=self.stop)

        self.stop_button.pack()

        self.draw_game_map_1()
        self.draw_game_map_2()
        
    def stop(self):
        self.is_running = False

    def back_to_home(self):
        response = messagebox.askyesno("Xác nhận", "Bạn có muốn thoát chế độ chơi này không?")
        if response:
            self.destroy()
            start_GUI_Start()
    def on_comparison_choice(self, event):
        choice = self.comparison_choice.get()
        self.focus_set()
        if choice == "Speed":
            # Hiển thị time_delay và ẩn các label step
            self.time_delay.pack(fill="x", expand=True)
            self.label_step_player.pack_forget()
            self.label_step_AI.pack_forget()
        else:
            # Ẩn time_delay và hiển thị các label step
            self.time_delay.pack_forget()
            self.label_step_player.pack(fill="x", expand=True)
            self.label_step_AI.pack(fill="x", expand=True)
    def xu_ly_boi_den(self, event):
        self.focus_set()
    def on_level_select(self,event):
        global FILE_MAP
        FILE_MAP = "map/{}.txt".format(self.choosenLevel.get())
        self.focus_set()
        self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))

        self.draw_game_map_1()
        self.draw_game_map_2()

    def restart_game(self):

        response = messagebox.askyesno("Xác nhận", "Bạn có muốn restart lại trò chơi không?")
        if response:

            global FILE_MAP
            self.algorithm_running = False
            self.game_started = False
            self.player_steps = 0
            self.AI_steps = 0
            self.update_gui_info_player(0)
            self.update_gui_info_AI(0)
            self.AI_completed = False
            self.Player_completed = False
            self.check_result_algorithm = True

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
        self.canvas_player.delete("all")
        for y, row in enumerate(self.GAME_MAP_1.state):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                image = None

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
                    self.canvas_player.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_player.image = image



        if self.GAME_MAP_1.is_complete():
            comparison_type = self.comparison_choice.get()
            if (comparison_type == "Step"):
                self.Player_completed = True
                return
            else:
                self.stop_game()
                messagebox.showinfo("Congratulations", "Player 1 win !!")

    def draw_game_map_2(self):

        self.canvas_AI.delete("all")
        for y, row in enumerate(self.GAME_MAP_2.state):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                image = None

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

                    self.canvas_AI.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_AI.image = image


        if self.GAME_MAP_2.is_complete():
            comparison_type = self.comparison_choice.get()
            if (comparison_type == "Step"):
                self.AI_completed = True
                return
            else:
                self.stop_game()
                messagebox.showinfo("Congratulations", "AI win !!")


    def update_gui_info_player(self, step_counter):
        self.label_step_player.config(text=f"Steps Player: {step_counter}")
        self.update()
    def update_gui_info_AI(self, step_counter):
        self.label_step_AI.config(text=f"Steps AI: {step_counter}")
        self.update()

    def update_ai_map(self):
        if not self.algorithm_running:
            return

        self.draw_game_map_2()
        self.after(100, self.update_ai_map)
    def solve_with_bfs(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = bfs_search(self.GAME_MAP_2)
        if result == None:
            messagebox.showinfo("Problem", "Don't find the path!")
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2= sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                break
        self.after_algorithm()

    def solve_with_dfs(self, timeDelay):
        self.step_counter = 0
        self.algorithm_running = True
        result, cell_count = dfs_search(self.GAME_MAP_2)
        if result == None:
            messagebox.showinfo("Problem", "Don't find the path!")
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                break

        self.after_algorithm()

    def solve_with_ucs(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = ucs_search(self.GAME_MAP_2)
        if result is None:
            messagebox.showinfo("Problem", "Don't find the path!")
            return
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                break

        self.after_algorithm()

    def solve_with_ids(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = ids_search(self.GAME_MAP_2, 5)
        if result == None:
            self.check_result_algorithm = False
            messagebox.showinfo("Problem", "Don't find the path!")
            return
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                break

        self.after_algorithm()

    def solve_with_greedy(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = greedy_search(self.GAME_MAP_2)
        if result == None:
            messagebox.showinfo("Problem", "Don't find the path!")


        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                break

        self.after_algorithm()

    def solve_with_a_star(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = astar_search(self.GAME_MAP_2)
        if result == None:
            messagebox.showinfo("Problem", "Don't find the path!")
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
            if self.is_running == False:
                self.is_running = True
                self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                break

        self.after_algorithm()

    def solve_with_hill_climbing(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = hill_climbing(self.GAME_MAP_2)
        if result == None:
            self.check_result_algorithm = False
            messagebox.showinfo("Problem", "AI Don't find the path!")
            return
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)
        self.after_algorithm()

    def solve_with_beam_search(self, timeDelay):
        self.algorithm_running = True
        self.step_counter = 0
        result, cell_count = BeamSearch(self.GAME_MAP_2, 2)
        if result == None:
            messagebox.showinfo("Problem", "Don't find the path!")
        for sokoban in result.path:
            if not self.algorithm_running:
                break
            self.GAME_MAP_2 = sokoban
            self.AI_steps += 1
            self.step_counter += 1
            self.update_gui_info_AI(self.step_counter)
            self.draw_game_map_2()
            time.sleep(timeDelay)


        self.after_algorithm()

    def run_algorithm(self):
        self.algorithm_running = True

        # Chọn thuật toán dựa trên lựa chọn của người dùng
        algorithm_type = self.algorithm_selected
        if algorithm_type == "BFS":
            result, cell_count = bfs_search(self.GAME_MAP_2)
        elif algorithm_type == "DFS":
            result, cell_count = dfs_search(self.GAME_MAP_2)
        elif algorithm_type == "IDS":
            result, cell_count = astar_search(self.GAME_MAP_2)
        elif algorithm_type == "UCS":
            result, cell_count = ucs_search(self.GAME_MAP_2)
        elif algorithm_type == "Greedy":
            result, cell_count = greedy_search(self.GAME_MAP_2)
        elif algorithm_type == "A Star":
            result, cell_count = dfs_search(self.GAME_MAP_2)
        elif algorithm_type == "Hill Climbing":
            result, cell_count = hill_climbing(self.GAME_MAP_2)
        elif algorithm_type == "Beam Search":
            result, cell_count = BeamSearch(self.GAME_MAP_2)



        # Kiểm tra kết quả và cập nhật bản đồ AI
        if result is not None:
            for sokoban in result.path:
                if not self.algorithm_running:
                    break
                self.GAME_MAP_2 = sokoban
                self.AI_steps += 1
                time.sleep(self.time_delay_step)  # Đợi giữa các bước di chuyển
                self.update_gui_info_AI(self.AI_steps)  # Cập nhật giao diện với số bước AI
                if self.is_running == False:
                    self.is_running = True
                    self.GAME_MAP = Sokoban(self.GAME_MAP_2.state)
                    break
        else:
            messagebox.showinfo("Problem", "AI can't find a path!")

        self.algorithm_running = False
        self.after_algorithm()



    def start_game(self):
        self.game_started = True

        check = False
        comparison_type = self.comparison_choice.get()
        algorithm_type = self.algorithm_choice_AI.get()
        self.algorithm_selected = self.algorithm_choice_AI.get()
        time_delay = self.time_delay.get()

        if comparison_type not in ["Step", "Speed"]:
            # Nếu chưa chọn, hiển thị thông báo
            messagebox.showwarning("Thông báo", "Mời bạn chọn kiểu so sánh trước khi bắt đầu.")
            return
        if algorithm_type not in ["BFS", "DFS", "IDS", "UCS", "Greedy", "A Star", "Hill Climbing",
                                                        "Beam Search"]:
            # Nếu chưa chọn, hiển thị thông báo
            messagebox.showwarning("Thông báo", "Mời bạn chọn thuật toán trước khi bắt đầu.")
            return
        if comparison_type == "Speed" and time_delay not in ["0.5", "1", "1.5", "2", "2.5", "3"]:
            messagebox.showwarning("Thông báo", "Mời bạn chọn thời gian chạy từng bước của thuật toán trước khi bắt đầu.")
            return
        if comparison_type == "Step":
            if algorithm_type == "BFS":
                self.solve_with_bfs(0.1)
            elif algorithm_type == "DFS":
                self.solve_with_dfs(0.1)
            elif algorithm_type == "IDS":
                self.solve_with_ids(0.1)
            elif algorithm_type == "UCS":
                self.solve_with_ucs(0.1)
            elif algorithm_type == "Greedy":
                self.solve_with_greedy(0.1)
            elif algorithm_type == "A Star":
                self.solve_with_a_star(0.1)
            elif algorithm_type == "Hill Climbing":
                self.solve_with_hill_climbing(0.1)
            elif algorithm_type == "Beam Search":
                self.solve_with_beam_search(0.1)
        else:
            self.time_delay_step = float(time_delay)
            self.after(100, self.update_ai_map)
            algorithm_thread = threading.Thread(target=self.run_algorithm)
            algorithm_thread.start()



    def stop_game(self):
        self.game_started = False
        self.algorithm_running = False

    def after_algorithm(self):
        if self.check_result_algorithm:
            self.AI_completed = True
            self.check_results()
        else:
            self.AI_completed = False
            self.check_results()
    def check_results(self):
        if self.AI_completed and not self.Player_completed and self.AI_steps < self.player_steps:
            messagebox.showinfo("Result", "AI Win")
        elif self.AI_completed and self.Player_completed:
            if self.AI_steps < self.player_steps:
                messagebox.showinfo("Result", "AI Win")
            elif self.AI_steps == self.player_steps:
                messagebox.showinfo("Result", "Draw")
            else:
                messagebox.showinfo("Result", "Player Win")
        elif self.AI_completed == False and self.Player_completed:
            messagebox.showinfo("Result", "Player Win")
    def on_key(self, event):
        # Xử lý đầu vào cho người chơi
        if self.game_started:
            valid_move = False
            if event.keysym in ["w", "s", "a", "d", "Up", "Down", "Left", "Right"]:
                if event.keysym == "w" or event.keysym == "Up":
                    valid_move = True
                    self.GAME_MAP_1.move_player_1(0, -1, self)

                elif event.keysym == "s" or event.keysym == "Down":
                    valid_move = True
                    self.GAME_MAP_1.move_player_1(0, 1, self)

                elif event.keysym == "a" or event.keysym == "Left":
                    valid_move = True
                    self.GAME_MAP_1.move_player_1(-1, 0, self)

                elif event.keysym == "d" or event.keysym == "Right":
                    valid_move = True
                    self.GAME_MAP_1.move_player_1(1, 0, self)

                if valid_move and self.comparison_choice.get() == "Step":
                    self.player_steps += 1
                    self.update_gui_info_player(self.player_steps)
                    self.check_results()

def main():
    game = SokobanGame()

    game.bind("<Key>", game.on_key)
    game.mainloop()
    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()