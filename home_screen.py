import tkinter
import tkinter.messagebox
from tkinter import Tk, filedialog
import ntpath
import json
from PIL import Image
import sys
import os
import customtkinter

class HomeScreen(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, background='#191919')
        self.controller = controller

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=160)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10 , pady=20)
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "puzzle.png")), size=(60, 60))

        self.logo = customtkinter.CTkLabel(self.sidebar_frame, text="", image=self.logo_image)
        self.logo.grid(row=0, column=0, padx=(30,10), pady=(20, 0))

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Jigsaw Genius", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Solve jigsaw & grid jigsaw", font=customtkinter.CTkFont(size=10, weight="normal"))
        self.logo_label.grid(row=2, column=0, padx=10)

        self.support = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text='Support')
        self.support.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, command=self.master.quit, text='EXIT')
        self.exit_button.grid(row=12, column=0, padx=20, pady=(10,20))

        # crate the main frame
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, rowspan=4, columnspan=4, sticky="nsew", padx=10 , pady=20)
        self.main_frame.grid_columnconfigure((0,1), weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "solving_puzzle.png")), size=(200, 200))

        self.logo = customtkinter.CTkLabel(self.main_frame, text="", image=self.logo_image)
        self.logo.grid(row=1, column=0,  columnspan=4, padx=(30,30), pady=(100, 10))
        

        self.label_3 = customtkinter.CTkLabel(self.main_frame, text="Select the type of the puzzle", font=customtkinter.CTkFont(size=24, weight="normal"))
        self.label_3.grid(row=2, column=0, columnspan=4, padx=30, pady=(10,30))
        
        self.level_1_button = customtkinter.CTkButton(self.main_frame, text='Grid Jigsaw', command=lambda: controller.show_frame("GridJigsawScreen"))
        self.level_1_button.grid(row=3, column=0, padx=30)

        self.level_2_button = customtkinter.CTkButton(self.main_frame, text='Jigsaw', command=lambda: controller.show_frame("JigsawScreen"))
        self.level_2_button.grid(row=3, column=1, padx=0)


        # set default values 
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def add_files(self):
        data = json.load(open("gui/data/videos.json", "r"))
        filename = filedialog.askopenfilename(filetypes=[("Video Files", ("*.mp4", "*.mov", "*.wmv", "*.mkv", "*.webm", "*.m4v"))])
        if filename not in data["videos"] and filename != "":
            self.update_database(filename)
            self.load_database()