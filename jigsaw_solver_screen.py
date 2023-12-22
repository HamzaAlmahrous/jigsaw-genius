import tkinter
import tkinter.messagebox
from tkinter import Tk, filedialog
import ntpath
import json
from PIL import Image
import sys
import os
import customtkinter

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x_folder_path = os.path.join(parent_dir, 'cv_project\\solvers\\part_2\\')
sys.path.append(x_folder_path)

from main import solve_jigsaw

class JigsawSolverScreen(tkinter.Frame):
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
        self.back_button = customtkinter.CTkButton(self.main_frame, text='back', command=lambda: controller.show_frame("JigsawScreen"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.back_button.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="w")
        
        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Select The Jigsaw:", font=customtkinter.CTkFont(size=24, weight="normal"))
        self.label_1.grid(row=2, column=0, columnspan=4, padx=30, pady=(30,30))
        
        self.jigsaw_button = customtkinter.CTkButton(self.main_frame, text='Jigsaw', command=lambda: controller.show_frame("GridJigsawScreen"))
        self.jigsaw_button.grid(row=3, column=0, padx=30, pady = (50,50), sticky="n")
        
        self.solve_button = customtkinter.CTkButton(self.main_frame, text='solve', command=lambda: controller.show_frame("HomeScreen"))
        self.solve_button.grid(row=4, column=0, padx=30, pady = (50,50), sticky="n")

        # Variables to store puzzle and hint image paths
        self.jigsaw_image_path = None

        self.jigsaw_button.configure(command=self.select_jigsaw_image)
        self.solve_button.configure(command=self.get_rows_cols)

    def select_jigsaw_image(self):
        self.jigsaw_image_path = filedialog.askopenfilename(title="Select Jigsaw Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.jigsaw_image_path:
            print(f"jigsaw Image Selected: {self.jigsaw_image_path}")  # You can handle this path as needed

    def get_rows_cols(self):
        print(self.jigsaw_image_path)
        if(self.jigsaw_image_path == None):
            tkinter.messagebox.showerror("Error", "Enter Jigsaw")
        else:
            self.jigsaw_image_path = self.jigsaw_image_path.replace("/", "\\")
            solve_jigsaw(self.jigsaw_image_path)