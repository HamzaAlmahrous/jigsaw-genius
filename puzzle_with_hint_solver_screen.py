import tkinter
import tkinter.messagebox
from tkinter import Tk, filedialog
import ntpath
import json
from PIL import Image
import sys
import os
import customtkinter
from tkinter import messagebox

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x_folder_path = os.path.join(parent_dir, 'cv_project\\solvers\\part_1_hint\\')
sys.path.append(x_folder_path)

from puzzle_with_hint_solver import solve_puzzle_with_hint

class PuzzleWithHintSolverScreen(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, background='#191919')
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # crate the main frame
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew", padx=10 , pady=20)
        self.main_frame.grid_columnconfigure((0,1), weight=1)
        # self.main_frame.grid_rowconfigure((1), weight=1)

        # create search options frame
        self.back_button = customtkinter.CTkButton(self.main_frame, text='back', command=lambda: controller.show_frame("GridJigsawScreen"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.back_button.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="w")
        
        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Select The Puzzle & The Hint:", font=customtkinter.CTkFont(size=24, weight="normal"))
        self.label_1.grid(row=2, column=0, columnspan=4, padx=30, pady=(30,30))
        
        self.puzzle_button = customtkinter.CTkButton(self.main_frame, text='puzzle', command=lambda: controller.show_frame("GridJigsawScreen"))
        self.puzzle_button.grid(row=3, column=0, padx=30, pady = (50,50), sticky="n")
        
        self.hint_button = customtkinter.CTkButton(self.main_frame, text='hint', command=lambda: controller.show_frame("HomeScreen"))
        self.hint_button.grid(row=3, column=1, padx=30, pady = (50,50), sticky="n")

        self.label_2 = customtkinter.CTkLabel(self.main_frame, text="Enter the number of rows & columns:", font=customtkinter.CTkFont(size=24, weight="normal"))
        self.label_2.grid(row=4, column=0, columnspan=4, padx=30, pady=(30,30))

        self.rows_button = customtkinter.CTkEntry(self.main_frame, placeholder_text="rows")
        self.rows_button.grid(row=5, column=0, padx=30, pady = (50,50), sticky="n")
        
        self.cols_button = customtkinter.CTkEntry(self.main_frame, placeholder_text="cols")
        self.cols_button.grid(row=5, column=1, padx=30, pady = (50,50), sticky="n")
        
        self.solve_button = customtkinter.CTkButton(self.main_frame, text='solve', command=lambda: controller.show_frame("HomeScreen"))
        self.solve_button.grid(row=6, column=0, padx=30, pady = (50,50), sticky="n")

        # Variables to store puzzle and hint image paths
        self.puzzle_image_path = None
        self.hint_image_path = None

        self.puzzle_button.configure(command=self.select_puzzle_image)
        self.hint_button.configure(command=self.select_hint_image)
        self.solve_button.configure(command=self.solve)

    def select_puzzle_image(self):
        self.puzzle_image_path = filedialog.askopenfilename(title="Select Puzzle Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.puzzle_image_path:
            print(f"Puzzle Image Selected: {self.puzzle_image_path}")  # You can handle this path as needed

    def select_hint_image(self):
        self.hint_image_path = filedialog.askopenfilename(title="Select Hint Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.hint_image_path:
            print(f"Hint Image Selected: {self.hint_image_path}")  # Handle this path as needed

    def solve(self):
        try:
            rows = int(self.rows_button.get())
            cols = int(self.cols_button.get())
            
            if(self.hint_image_path == None or self.puzzle_image_path == None):
                messagebox.showerror("Error", "Enter Puzzle and Hint")
            else:
                self.puzzle_image_path = self.puzzle_image_path.replace("/", "\\")
                self.hint_image_path = self.hint_image_path.replace("/", "\\")
                solve_puzzle_with_hint(self.hint_image_path, self.puzzle_image_path, rows, cols)

        except ValueError:
            tkinter.messagebox.showerror("Error", "Enter Rows and Columns")
            return None, None

# The rest of your code to initialize and run the Tkinter application
