import pygame
import tkinter as tk
from tkinter import *
import os
_ROOT = os.path.abspath(os.path.dirname(__file__))
def start_GUI_Start():
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(_ROOT,"music_game.mp3"))
    pygame.mixer.music.play(-1)

    root = tk.Tk()
    root.resizable(False, False)
    root.title("Sokoban game")
    root.geometry("1295x645")
    canvas = Canvas(root, height=645, width=1295, bd=0, highlightthickness=1, relief="ridge")
    canvas.place(x=0, y=0)
    background_img = PhotoImage(file=os.path.join(_ROOT,f"images/background4_1.png"))
    background = canvas.create_image(650.0, 320.0, image=background_img)


    def start_game():
        mode_selected = selected_mode.get()
        root.destroy()
        # Thực hiện các hành động cần thiết để bắt đầu trò chơi
        print("Game started!")
        from GUI_level_selection import select_modePlay
        select_modePlay(mode_selected)
        import GUI_level_selection
        GUI_level_selection.main()

    start_img = PhotoImage(file=os.path.join(_ROOT,f"images/start_game.png"))
    start = Button(image=start_img, borderwidth=0, highlightthickness=0, relief="flat", command = start_game)
    start.place(x=630, y=500, width=150, height=70)

    # Danh sách chọn chế độ chơi
    game_modes = ["1 Player", "2 Player", "AI VS AI", "Player VS AI"]
    selected_mode = StringVar(value=game_modes[0])

    # Label hiển thị chế độ chơi
    mode_label = Label(root, textvariable=selected_mode, bg="#CFB58D", fg="#86603E", font=("Goudy Stout", 10))
    mode_label.place(x=600, y=400, width=200, height=50)

    # Nút "<" để di chuyển sang chế độ trước đó
    def previous_mode():
        current_index = game_modes.index(selected_mode.get())
        previous_index = (current_index - 1) % len(game_modes)
        selected_mode.set(game_modes[previous_index])

    previous_button = Button(root, text="<", command=previous_mode)
    previous_button.place(x=575, y=400, width=25, height=50)

    # Nút ">" để di chuyển sang chế độ kế tiếp
    def next_mode():
        current_index = game_modes.index(selected_mode.get())
        next_index = (current_index + 1) % len(game_modes)
        selected_mode.set(game_modes[next_index])

    next_button = Button(root, text=">", command=next_mode)
    next_button.place(x=800, y=400, width=25, height=50)

    root.mainloop()
    pygame.mixer.music.stop()

if __name__ == "__main__":
    start_GUI_Start()