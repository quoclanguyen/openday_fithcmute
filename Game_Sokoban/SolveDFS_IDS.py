# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 15:50:01 2023

@author: DELL
"""

from SokobanState import *

def dfs_search(initial_state):
    stack = [(initial_state)]  # Stack để lưu trữ các trạng thái cần xem xét

    visited = set()  # Lưu trữ các trạng thái đã xem
    cell_counter = 0 
    while stack:
        current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack

        if current_state.is_complete():
            return current_state, cell_counter  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
    
        # Sinh các trạng thái kế tiếp và thêm vào stack
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                stack.append(move)
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
                cell_counter += 1 
    return None, cell_counter

def ids_search(initial_state, depth_limit):
    state_eq_limit = [initial_state]

    visited = set()  # Lưu trữ các trạng thái đã xem
    cell_counter = 0 
    while state_eq_limit:
        stack = state_eq_limit
        state_eq_limit = []
        while stack:
            current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack
    
            if current_state.is_complete():
                return current_state , cell_counter # Nếu đạt được trạng thái mục tiêu, trả về kết quả
        
            # Sinh các trạng thái kế tiếp và thêm vào stack
            for move in current_state.generate_moves():
                if tuple(map(tuple, move.state)) not in visited and move.depth <= depth_limit:
                    stack.append(move)
                    visited.add(tuple(map(tuple, move.state))) 
                    move.path = current_state.path + [move]
                    if move.depth == depth_limit:
                        state_eq_limit.append(move)
                    cell_counter += 1 
        depth_limit = depth_limit + 5
        
    return None, cell_counter