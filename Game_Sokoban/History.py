# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:11:07 2023

@author: DELL
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class TableApp(tk.Tk):
    def __init__(self, data):
        tk.Tk.__init__(self)
        self.title("History")
        self.geometry("950x600")
        
        self.data = data
        self.canvas = None
        
        self.table = ttk.Treeview(self, columns=("Level", "Search Method", "Elapsed Time", "Cell Count", "Step Counter"))
        self.table.heading("#0", text="Index")
        self.table.heading("Level", text="Level")
        self.table.heading("Search Method", text="Search Method")
        self.table.heading("Elapsed Time", text="Elapsed Time")
        self.table.heading("Cell Count", text="Cell Count")
        self.table.heading("Step Counter", text="Step Counter")
        tree_height = min(10, len(data) + 1)  # Set a maximum height of 10 rows
        self.table["height"] = tree_height
        self.table.pack(fill="both", expand=True)
        # Create a horizontal scrollbar
        xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.table.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.table.configure(xscrollcommand=xscrollbar.set)
        
        self.draw_table()
        btnOutputexcel = tk.Button(self, text = "Output Excel",  font = ("Times", 12, "bold"), borderwidth = 3, background = "floralwhite", fg = "black", command=self.output_excel)
        btnOutputexcel.pack()
        ttk.Label(self, text = "Choose level :",
                  font = ("Times New Roman", 10)).pack()
              
        # Combobox creation
        n = tk.StringVar()
        self.choosenLevel = ttk.Combobox(self, width = 27, textvariable = n, state="readonly")
        levels =[]
        for entry in self.data:
            level, algorithm, elapsed_time, cell_count, step_counter = entry
            if level not in levels:
                levels.append(level)

        self.choosenLevel['values'] = tuple(levels)
        self.choosenLevel.pack()
        self.choosenLevel.current()
        
        ttk.Label(self, text = "Parameter :",
                  font = ("Times New Roman", 10)).pack()
        
        n2 = tk.StringVar()
        self.choosenParameter = ttk.Combobox(self, width = 27, textvariable = n2, state="readonly")
              

        self.choosenParameter['values'] = tuple(["Elapsed Time", "Cell Count", "Step Counter"])
        self.choosenParameter.pack()
        self.choosenParameter.current()
        
        btnConfirm = tk.Button(self, text = "Confirm",  font = ("Times", 12, "bold"), borderwidth = 3, background = "floralwhite", fg = "black", command=self.draw_chart)
        btnConfirm.pack()
    
    def draw_table(self):
        for index, row in enumerate(self.data, start=1):
            self.table.insert(parent="", index="end", iid=index, text=str(index), values=row)
            
    def draw_chart(self):
        algorithms = []
        elapsed_times = []
        cell_counts = []
        step_counters = []

        for entry in self.data:
            level, algorithm, elapsed_time, cell_count, step_counter = entry
            if level == self.choosenLevel.get():
                algorithms.append(algorithm)
                elapsed_times.append(elapsed_time)
                cell_counts.append(cell_count)
                step_counters.append(step_counter)
                
        plt.figure(figsize=(8, 4))
        if self.choosenParameter.get() == "Elapsed Time":
            plt.bar(algorithms, elapsed_times)
        elif self.choosenParameter.get() == "Cell Count":
            plt.bar(algorithms, cell_counts)
        elif self.choosenParameter.get() == "Step Counter":
            plt.bar(algorithms, step_counters)
        plt.xlabel("Algorithms")
        plt.ylabel(self.choosenParameter.get())
        plt.title(f"{self.choosenParameter.get()} by Algorithm - {self.choosenLevel.get()}")

        # Tạo FigureCanvasTkAgg từ biểu đồ
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        canvas.draw()

        # Hiển thị biểu đồ trên Tkinter
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = canvas
        self.canvas.get_tk_widget().pack()

        plt.show()
        
    def output_excel(self):
        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(self.data, columns=["Level", "Algorithm", "Elapsed Time", "Cell Count", "Step Counter"])
        
        # Chọn đường dẫn và tên tệp Excel để xuất
        excel_file_path = "history_data.xlsx"
        
        # Xuất DataFrame vào tệp Excel
        df.to_excel(excel_file_path, index=False)
    
        messagebox.showinfo("Notification",f"The data has been exported successfull {excel_file_path}")

def History(data):
    app = TableApp(data)
    app.mainloop()
    
# data = [
#     (1, "Algorithm A", 10.5, 100, 50),
#     (1, "Algorithm B", 12.3, 120, 60),
#     (2, "Algorithm A", 8.2, 80, 40),
#     (2, "Algorithm B", 9.5, 95, 45),
#     (3, "Algorithm A", 11.0, 110, 55),
#     (3, "Algorithm B", 13.1, 130, 65),
#     # Add more data as needed
# ]

# History(data)
#output_excel(data)