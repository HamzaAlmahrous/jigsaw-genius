import tkinter
import tkinter.messagebox
from tkinter import Tk, filedialog
import ntpath
import json
from PIL import Image
import sys
import os
import customtkinter

class GridJigsawScreen(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, background='#191919')
        self.controller = controller

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # crate the main frame
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew", padx=10 , pady=20)
        self.main_frame.grid_columnconfigure((0,1), weight=1)
        # self.main_frame.grid_rowconfigure((1), weight=1)

        # create search options frame
        self.back_button = customtkinter.CTkButton(self.main_frame, text='back', command=lambda: controller.show_frame("HomeScreen"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.back_button.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="w")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "solve_puzzle.png")), size=(200, 200))

        self.logo = customtkinter.CTkLabel(self.main_frame, text="", image=self.logo_image)
        self.logo.grid(row=2, column=0,  columnspan=4, padx=(30,30), pady=(10, 10))
        
        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Grid Jigsaw", font=customtkinter.CTkFont(size=28, weight="normal"))
        self.label_1.grid(row=3, column=0, columnspan=4, padx=30, pady=(30,30))
        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Select the type:", font=customtkinter.CTkFont(size=24, weight="normal"))
        self.label_1.grid(row=4, column=0, columnspan=4, padx=30, pady=(30,30))
        
        self.normal_button = customtkinter.CTkButton(self.main_frame, text='puzzle', command=lambda: controller.show_frame("PuzzleSolverScreen"))
        self.normal_button.grid(row=5, column=0, padx=30, pady = (50,100), sticky="n")
        
        self.hint_button = customtkinter.CTkButton(self.main_frame, text='puzzle + hint', command=lambda: controller.show_frame("PuzzleWithHintSolverScreen"))
        self.hint_button.grid(row=5, column=1, padx=30, pady = (50,100), sticky="n")

    def add_files(self):
        data = json.load(open("gui/data/videos.json", "r"))
        filename = filedialog.askopenfilename(filetypes=[("Images Files", ("*.png", "*.jpg"))])
        if filename not in data["videos"] and filename != "":
            self.update_database(filename)
            self.load_database()