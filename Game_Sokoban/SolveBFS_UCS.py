# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 17:03:52 2023

@author: HOME
"""
import heapq
from SokobanState import *

def bfs_search(initial_state):
    queue = [initial_state]  
    visited = set()  
    cell_counter = 0 
    while queue:
        current_state = queue.pop(0)  

        if current_state.is_complete():
            
            return current_state, cell_counter
    
        # Sinh các trạng thái kế tiếp và thêm vào hàng đợi
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                queue.append(move)
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
                cell_counter += 1 
    return None, cell_counter

def ucs_search(initial_state):
    queue = [(0, initial_state)]  
    visited = set() 
    cell_counter = 0  # Biến đếm số ô đã thăm

    while queue:
        queue = sorted(queue, key=lambda x: x[0])  
        cost, current_state = queue.pop(0)  

        if current_state.is_complete():
            return current_state, cell_counter  # Trả về cả trạng thái và số ô đã thăm

        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                new_cost = cost + calculate_move_cost(move, current_state)
                queue.append((new_cost, move))
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
                cell_counter += 1  # Tăng biến đếm

    return None, cell_counter
def calculate_move_cost(new_state, current_state):
    base_cost = 1  # Chi phí cơ bản cho mỗi bước di chuyển
    box_move_cost = 2  # Chi phí khi di chuyển hộp

    # Kiểm tra xem có di chuyển hộp hay không
    if moved_box(new_state, current_state):
        return base_cost + box_move_cost
    else:
        return base_cost

def moved_box(new_state, current_state):
    # Hàm này kiểm tra xem có hộp nào được di chuyển giữa hai trạng thái hay không
    new_player_pos = new_state.player_pos
    old_player_pos = current_state.player_pos

    # Lấy vị trí giữa người chơi cũ và mới
    if old_player_pos != new_player_pos:
    # Kiểm tra xem vị trí giữa có phải là vị trí của hộp trong trạng thái cũ hay không
        if current_state.state[new_player_pos[1]][new_player_pos[0]] in [Level.box, Level.box_on_target]:
            return True
    return False
