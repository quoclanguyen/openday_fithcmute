import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.font import Font
from PIL import ImageTk, Image
import numpy as np
import cv2
import time
import queue

wn = Tk()
WIN_TITLE = '8 puzzle'
SCREEN_WIDTH = wn.winfo_screenwidth()
SCREEN_HEIGHT = wn.winfo_screenheight()
WIN_WIDTH = 1200
WIN_HEIGHT = 600
X_WIN = (SCREEN_WIDTH - WIN_WIDTH)//2
Y_WIN = (SCREEN_HEIGHT - WIN_HEIGHT)//2
USE_DEFAULT_IMAGE = True
algo_btn_width = 11

wn.title(WIN_TITLE)
wn.geometry("{}x{}+{}+{}".format(WIN_WIDTH, WIN_HEIGHT, X_WIN, Y_WIN))
wn.attributes('-fullscreen', True)
wn.configure(bg = '#C4AFAB')

coord = np.array([
    np.array([110, 110]), np.array([250, 110]), np.array([390, 110]), 
    np.array([110, 250]), np.array([390, 250]), np.array([110, 390]), 
    np.array([250, 390]), np.array([390, 390]), np.array([250, 250])])

pieces = [tkinter.Label() for i in range(8)]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
random_index = np.arange(8)
current_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
checkpoint = []
rollback = False
first = 0
moves_played = 0
nodes_created = 0

def solvable(array):
    inv = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if (array[j] > array[i]):
                inv += 1
    return (inv % 2 == 0)

def dispose():
    global first, var_moves
    var_moves.set("Moves played: 0")
    if (first == 0):
        first += 1
    else:
        for i in range(8): 
            pieces[i].destroy()
            pieces[i] = tkinter.Label()

def start():
    global USE_DEFAULT_IMAGE, current_state, moves_played, nodes_created, checkpoint, rollback
    dispose()
    moves_played = 0
    var_nodes.set("Nodes created: 0")
    np.random.shuffle(random_index)
    while (not solvable(random_index)):
        np.random.shuffle(random_index)
    if rollback:
        current_state = checkpoint.copy()
    else:
        current_state = (random_index + 1).tolist().copy()
        checkpoint = current_state.copy()
    rollback = False
    for i in range(8):
        if USE_DEFAULT_IMAGE:
            image = Image.open("./res_8puzz/wood{}.png".format(current_state[i]))
        else:
            image = Image.open("./custom_pieces/wood{}.png".format(current_state[i]))
        test = ImageTk.PhotoImage(image)
        label = tkinter.Label(image=test)
        label.image = test
        pieces[i] = label
        pieces[i].place(x = coord[i][0], y = coord[i][1])
    current_state.insert(4, 0)

def load_state():
    global USE_DEFAULT_IMAGE, current_state, moves_played, checkpoint, rollback
    dispose()
    rollback = True
    start()

def browse_image():
    global USE_DEFAULT_IMAGE, goalLabel
    USE_DEFAULT_IMAGE = False
    goalLabel.destroy()
    accepted_ft = [
        ('Supported image types', '*.png *.jpg *.jpeg'),
        ('PNG images', '*.png'),
        ('JPG images', '*.jpg'),
        ('JPEG images', '*.jpeg')
    ]
    coin = np.random.randint(1, 1000)
    filename = "./res_8puzz/logo.png" if coin % 2 == 0 else "./res_8puzz/fit.png"
    # filename = fd.askopenfilename(title = 'Open a file', initialdir = './', filetypes = accepted_ft)
    try:
        im = cv2.imread(filename)
        w = im.shape[1]
        r = 410.0/w
        dim = (410, int(w*r))
        im = cv2.resize(im, dim)
        cv2.imwrite('./custom_pieces/resized.png', im)
        for i in range(8):
            rows = (i//3)*140
            cols = (i%3)*140
            cutImg = im[rows:rows+130, cols:cols+130]
            cv2.imwrite('./custom_pieces/wood{}.png'.format(i + 1), cutImg)
        image = Image.open('./custom_pieces/resized.png')
        test = ImageTk.PhotoImage(image)
        goalLabel = tkinter.Label(image=test)
        goalLabel.image = test
        goalLabel.place(x = 900, y = 110)
    except:
        messagebox.showinfo(title='Thông báo', message='Không mở file được')
        USE_DEFAULT_IMAGE = True
    start()
def use_default_image():
    global USE_DEFAULT_IMAGE
    USE_DEFAULT_IMAGE = True
    goalLabel.destroy()
    start()
### Algorithms
def go_left(state):
    copy = state.copy()
    zi = copy.index(0) #zero index
    if zi % 3 != 2:
        copy[zi], copy[zi + 1] = copy[zi + 1], copy[zi]
    return copy

def go_right(state):
    copy = state.copy()
    zi = copy.index(0) #zero index
    if zi % 3 != 0:
        copy[zi], copy[zi - 1] = copy[zi - 1], copy[zi]
    return copy

def go_up(state):
    copy = state.copy()
    zi = copy.index(0) #zero index
    if zi // 3 != 2:
        copy[zi], copy[zi + 3] = copy[zi + 3], copy[zi]
    return copy

def go_down(state):
    copy = state.copy()
    zi = copy.index(0) #zero index
    if zi // 3 != 0:
        copy[zi], copy[zi - 3] = copy[zi - 3], copy[zi]
    return copy

def bfs():
    list_state = []
    list_state.append(current_state.copy())
    tree = [[0, 'root', 0]]
    i = 0
    index = i
    goal_index = 0
    direct = ['left', 'right', 'up', 'down']
    while goal_index == 0:
        for j in range(4):
            go = globals()['go_' + direct[j]]
            if (list_state[i] == go(list_state[i])):
                continue
            try:
                list_state.index(go(list_state[i]))
            except:
                list_state.append(go(list_state[i]))
                index += 1
                tree.append([index, direct[j], i])
            
            if list_state[-1][:3] == goal_state[:3]:
                goal_index = index
                break
        i += 1
    prev_goal_index = goal_index
    while goal_index == prev_goal_index:
        for j in range(4):
            go = globals()['go_' + direct[j]]
            if (list_state[i] == go(list_state[i])):
                continue
            if ((go(list_state[i]))[:3] != goal_state[:3]):
                continue
            try:
                list_state.index(go(list_state[i]))
            except:
                list_state.append(go(list_state[i]))
                index += 1
                tree.append([index, direct[j], i])
            
            if list_state[-1] == goal_state:
                goal_index = index
                break
        i += 1
    move = []
    while (goal_index != 0):
        move.append(tree[goal_index][1])
        goal_index = tree[goal_index][2]
    move = move[::-1]
    var_nodes.set("Nodes created: {} with bfs".format(len(list_state)))
    for i in range(len(move)):
        action = 'move_' + move[i]
        dir = globals()[action]
        time.sleep(0.1)
        dir()
        wn.update()
    
def dfs():
    stack = []  
    visited = set()  
    stack.append((current_state, []))  
    inc = 0
    while stack:
        state, moves = stack.pop()  
        inc+=1
        if state == goal_state:
            print('Done with ' + str(inc) + ' nodes')
            for move in moves:
                action = 'move_' + move
                dir = globals()[action]
                time.sleep(0.1)
                dir()
                wn.update()
            var_nodes.set("Nodes created: {} with dfs".format(inc))
            return
        if len(moves) >= 40:
            continue
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        for action in ['left', 'right', 'up', 'down']:
            new_state = globals()['go_' + action](state)
            if new_state:
                new_moves = moves + [action]
                stack.append((new_state, new_moves))

def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        goal_index = goal_state.index(state[i])
        current_row, current_col = i // 3, i % 3
        goal_row, goal_col = goal_index // 3, goal_index % 3
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def ucs():
    priority_queue = queue.PriorityQueue()
    visited = set()
    
    priority_queue.put((0, current_state, []))  
    inc = 0
    while not priority_queue.empty():
        cost, state, moves = priority_queue.get()
        inc += 1
        if state == goal_state:
            for move in moves:
                action = 'move_' + move
                dir = globals()[action]
                time.sleep(0.1)
                dir()
                wn.update()
            var_nodes.set("Nodes created: {} with ucs".format(inc))
            return
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        for action in ['left', 'right', 'up', 'down']:
            new_state = globals()['go_' + action](state)
            if new_state:
                new_cost = cost + 1 # + manhattan_distance(new_state) 
                new_moves = moves + [action]
                priority_queue.put((new_cost, new_state, new_moves))

def greedy():
    priority_queue = queue.PriorityQueue()
    visited = set()
    
    priority_queue.put((manhattan_distance(current_state), current_state, []))  
    inc = 0
    while not priority_queue.empty():
        _, state, moves = priority_queue.get()
        inc += 1
        if state == goal_state:
            for move in moves:
                action = 'move_' + move
                dir = globals()[action]
                time.sleep(0.1)
                dir()
                wn.update() 
            var_nodes.set("Nodes created: {} with greedy".format(inc))
            return

        if tuple(state) in visited:
            continue 

        visited.add(tuple(state))
        for action in ['left', 'right', 'up', 'down']:
            new_state = globals()['go_' + action](state)
            if new_state:
                new_moves = moves + [action]
                priority_queue.put((manhattan_distance(new_state), new_state, new_moves))

def astar():
    priority_queue = queue.PriorityQueue()
    visited = set()
    
    priority_queue.put((manhattan_distance(current_state), current_state, []))  
    inc = 0
    while not priority_queue.empty():
        _, state, moves = priority_queue.get()
        inc += 1
        if state == goal_state:
            for move in moves:
                action = 'move_' + move
                dir = globals()[action]
                time.sleep(0.1)
                dir()
                wn.update() 
            var_nodes.set("Nodes created: {} with a*".format(inc))
            return

        if tuple(state) in visited:
            continue  

        visited.add(tuple(state))
        for action in ['left', 'right', 'up', 'down']:
            new_state = globals()['go_' + action](state)
            if new_state:
                new_moves = moves + [action]
                f = len(new_moves) + manhattan_distance(new_state) # f = g + h
                priority_queue.put((f, new_state, new_moves))

def hill():
    stack = []  
    visited = set()  
    stack.append((current_state, []))  
    inc = 0
    while stack:
        state, moves = stack.pop()  
        inc+=1
        if state == goal_state:
            print('Done with ' + str(inc) + ' nodes')
            for move in moves:
                action = 'move_' + move
                dir = globals()[action]
                time.sleep(0.1)
                dir()
                wn.update()
            var_nodes.set("Nodes created: {} with hill".format(inc))
            return
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        for action in ['left', 'right', 'up', 'down']:
            new_state = globals()['go_' + action](state)
            print(manhattan_distance(new_state))
            if manhattan_distance(new_state) <= manhattan_distance(state):
                new_moves = moves + [action]
                stack.append((new_state, new_moves))

def calcMahattan():
    sum = 0
    for i in range(9):
        sum += abs(current_state[i] - goal_state[i])
    print((sum))


txt_font = Font(family='EB Garamond', size=20)

btn_load_image = Button(text = "Load image", bg = "#03DAC6", fg = "#000000", \
                        font = txt_font, command = browse_image)
btn_load_image.place(x = 175, y = 50, anchor = CENTER)
btn_use_default_image = Button(text = "Load default", bg = "#3700B3", fg = "White",
                        font = txt_font, command = use_default_image)
btn_use_default_image.place(x = 455, y = 50, anchor = CENTER)

btn_start = Button(text = "Scramble", bg = "#BB86FC", fg = "#000000",
                   font = txt_font, command = start)
btn_start.place(x = 315, y = 50, anchor = CENTER)
btn_load_state = Button(text = "Restart", bg = "#BB86FC", fg = "#000000",
                   font = txt_font, command = load_state)
btn_load_state.place(x = 315, y = 580, anchor = CENTER)
btn_bfs = Button(text = "BFS", bg = "#B3261E", fg = "#FBFAFE", width = algo_btn_width,
                        font = txt_font, command = bfs)
btn_bfs.place(x = 570, y = 100)
btn_ucs = Button(text = "UCS", bg = "#3700B3", fg = "#FBFAFE", width = algo_btn_width,
                        font = txt_font, command = ucs)
btn_ucs.place(x = 570, y = 180)
btn_dfs = Button(text = "DFS", bg = "#03DAC6", fg = "#FBFAFE", width = algo_btn_width,
                        font = txt_font, command = dfs)
btn_dfs.place(x = 570, y = 260)
btn_greedy = Button(text = "Greedy", bg = "#CC6E69", fg = "#FBFAFE", width = algo_btn_width,
                        font = txt_font, command = greedy)
btn_greedy.place(x = 570, y = 340)
btn_astar = Button(text = "A*", bg = "#7955CC", fg = "#FBFAFE", width = algo_btn_width,
                        font = txt_font, command = astar)
btn_astar.place(x = 570, y = 420)


var_moves = StringVar()
var_moves.set("Moves played: ")
lbl_moves_played = Label(textvariable = var_moves, font = txt_font, bg = '#C4AFAB', fg = '#292929')
lbl_moves_played.place(x = 570, y = 60)

var_nodes = StringVar()
var_nodes.set("Nodes created: 0")
lbl_nodes_created = Label(textvariable = var_nodes, font = txt_font, bg = '#C4AFAB', fg = '#292929')
lbl_nodes_created.place(x = 570, y = 500)

fithcmute_image = Image.open('./res_8puzz/fithcmute.png')
test = ImageTk.PhotoImage(fithcmute_image)
goalLabel = tkinter.Label(image=test)
goalLabel.image = test
goalLabel.place(x = 383, y = 650)

goalLabel = tkinter.Label()

def get_state():
    sumx = 0
    sumy = 0
    for i in range(8):
        sumx += pieces[i].winfo_x()
        sumy += pieces[i].winfo_y()
    hole = np.array([2250, 2250]) - np.array([sumx, sumy])
    return hole
    
def move_left(*e):
    global moves_played, var_moves
    hole = get_state()
    index = -1
    for i in range(8):
        if ((pieces[i].winfo_x() - 140 == hole[0]) and (pieces[i].winfo_y() == hole[1])):
            index = i
    if (index != -1): #movable
        pieces[index].place(x = hole[0], y = hole[1])
        zi = current_state.index(0) #zero index
        current_state[zi], current_state[zi + 1] = current_state[zi + 1], current_state[zi]
        moves_played += 1
        var_moves.set("Moves played: {}".format(moves_played))
        # if current_state == goal_state:
        #     messagebox.showinfo(title='Thông báo', message='Bạn đã giải thành công!')
        #     start()

def move_right(*e):
    global moves_played, var_moves
    hole = get_state()
    index = -1
    for i in range(8):
        if ((pieces[i].winfo_x() + 140 == hole[0]) and (pieces[i].winfo_y() == hole[1])):
            index = i
    if (index != -1):
        pieces[index].place(x = hole[0], y = hole[1])
        zi = current_state.index(0) #zero index
        current_state[zi], current_state[zi - 1] = current_state[zi - 1], current_state[zi]
        moves_played += 1
        var_moves.set("Moves played: {}".format(moves_played))
        # if current_state == goal_state:
        #     messagebox.showinfo(title='Thông báo', message='Bạn đã giải thành công!')
        #     start()

def move_up(*e):
    global moves_played, var_moves
    hole = get_state()
    index = -1
    for i in range(8):
        if ((pieces[i].winfo_x() == hole[0]) and (pieces[i].winfo_y() - 140 == hole[1])):
            index = i
    if (index != -1):
        pieces[index].place(x = hole[0], y = hole[1])
        zi = current_state.index(0) #zero index
        current_state[zi], current_state[zi + 3] = current_state[zi + 3], current_state[zi]
        moves_played += 1
        var_moves.set("Moves played: {}".format(moves_played))
        # if current_state == goal_state:
        #     messagebox.showinfo(title='Thông báo', message='Bạn đã giải thành công!')
        #     start()

def move_down(*e):
    global moves_played, var_moves
    hole = get_state()
    index = -1
    for i in range(8):
        if ((pieces[i].winfo_x() == hole[0]) and (pieces[i].winfo_y() + 140 == hole[1])):
            index = i
    if (index != -1):
        pieces[index].place(x = hole[0], y = hole[1])
        zi = current_state.index(0) #zero index
        current_state[zi], current_state[zi - 3] = current_state[zi - 3], current_state[zi]
        moves_played += 1
        var_moves.set("Moves played: {}".format(moves_played))
        # if current_state == goal_state:
        #     messagebox.showinfo(title='Thông báo', message='Bạn đã giải thành công!')
        #     start()

def key_press(e):
    start()
start()

wn.bind('<Left>', move_left)
wn.bind('<Right>', move_right)
wn.bind('<Up>', move_up)
wn.bind('<Down>', move_down)
wn.bind('<KeyPress-r>', key_press)

wn.mainloop()