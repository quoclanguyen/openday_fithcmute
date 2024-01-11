import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
#from GUI_Sokoban import FILE_MAP
import os
import pygame

from Game_Sokoban.main import start_GUI_Start

_ROOT = os.path.abspath(os.path.dirname(__file__))

global FILE_MAP_level



modePlay = ""
def select_modePlay(mode):
    global modePlay
    modePlay = mode
class level_selection(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
       # self.level_selection_window = tk.Tk()
        self.title("Level Selection")
        self.geometry("800x500+500+100")
        
        
        self.canvas = Canvas(self, bg="#4392F1", height=500, width=800, bd=0, highlightthickness=1, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.background_img = PhotoImage(file=os.path.join(_ROOT,f"images/background2.png"))
        self.background = self.canvas.create_image(400.0, 250.0, image=self.background_img)
        
        self.lv1_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv1_2.png"))
        self.lv1 = tk.Button(image=self.lv1_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(1))
        self.lv1.place(x=50, y=40, width=100, height=100)
        
        
        self.lv2_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv2.png"))
        self.lv2 = tk.Button(image=self.lv2_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(2))
        self.lv2.place(x=200, y=40, width=100, height=100)
        
        
        self.lv3_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv3.png"))
        self.lv3 = tk.Button(image=self.lv3_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(3))
        self.lv3.place(x=350, y=40, width=100, height=100)
        
        self.lv4_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv4.png"))
        self.lv4 = tk.Button(image=self.lv4_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(4))
        self.lv4.place(x=500, y=40, width=100, height=100)
        
        self.lv5_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv5.png"))
        self.lv5 = tk.Button(image=self.lv5_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(5))
        self.lv5.place(x=650, y=40, width=100, height=100)
        
        self.lv6_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv6.png"))
        self.lv6 = tk.Button(image=self.lv6_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(6))
        self.lv6.place(x=50, y=165, width=100, height=100)
        
        self.lv7_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv7.png"))
        self.lv7 = tk.Button(image=self.lv7_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(7))
        self.lv7.place(x=200, y=165, width=100, height=100)
        
        self.lv8_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv8.png"))
        self.lv8 = tk.Button(image=self.lv8_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(8))
        self.lv8.place(x=350, y=165, width=100, height=100)
        
        self.lv9_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv9.png"))
        self.lv9 = tk.Button(image=self.lv9_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(9))
        self.lv9.place(x=500, y=165, width=100, height=100)
        
        
        self.lv10_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv10.png"))
        self.lv10 = tk.Button(image=self.lv10_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(10))
        self.lv10.place(x=650, y=165, width=100, height=100)
        
        self.lv11_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv11.png"))
        self.lv11 = tk.Button(image=self.lv11_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(11))
        self.lv11.place(x=50, y=300, width=100, height=100)
        
        self.lv12_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv12.png"))
        self.lv12 = tk.Button(image=self.lv12_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(12))
        self.lv12.place(x=200, y=300, width=100, height=100)
        
        self.lv13_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv13.png"))
        self.lv13 = tk.Button(image=self.lv13_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(13))
        self.lv13.place(x=350, y=300, width=100, height=100)       
        
        self.lv14_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv14.png"))
        self.lv14 = tk.Button(image=self.lv14_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(14))
        self.lv14.place(x=500, y=300, width=100, height=100)
        
        self.lv15_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/lv15.png"))
        self.lv15 = tk.Button(image=self.lv15_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.open_level(15))
        self.lv15.place(x=650, y=300, width=100, height=100)
        
    
        
        
        #back_img = PhotoImage(file=f"assets/back.png")
        self.back_img = tk.PhotoImage(file=os.path.join(_ROOT,f"images/back.png"))
        self.back = tk.Button(image=self.back_img, borderwidth=0, highlightthickness=0, relief="flat",command=self.back_to_home)
        self.back.place(x=350, y=450, width=100, height=40)
         # Import GUI_start để chuyển về GUI_start

    def back_to_home(self):
        self.destroy()  # Đóng cửa sổ SokobanGame
        start_GUI_Start()  # Mở cửa sổ GUI_Start
        
    def open_level(self, level):
        new_file_map = "map/level{}.txt".format(level)  # Đường dẫn map cho level 
        self.destroy()
        if modePlay == "1 Player":
            from GUI_Sokoban import update_file_map
            update_file_map(new_file_map)
            from GUI_Sokoban import main
            main()
        elif modePlay == "2 Player":
            from GUI_TwoPlayerSokoban import update_file_map
            update_file_map(new_file_map)
            from GUI_TwoPlayerSokoban import main
            main()
        elif modePlay == "AI VS AI":
            from GUI_TwoAI import update_file_map
            update_file_map(new_file_map)
            from GUI_TwoAI import main
            main()
        elif modePlay == "Player VS AI":
            from GUI_PlayerVSAI import update_file_map
            update_file_map(new_file_map)
            from GUI_PlayerVSAI import main
            main()

def main():
    level = level_selection()
    level.mainloop()
    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()