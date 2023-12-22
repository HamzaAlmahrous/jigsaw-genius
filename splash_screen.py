import tkinter
from PIL import Image
import sys
import os
import customtkinter

class SplashScreen(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, background='#191919')
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # crate the main frame
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10 , pady=20)
        self.main_frame.grid_columnconfigure((0), weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        # create sidebar frame with widgets
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "puzzle.png")), size=(300, 300))

        self.logo = customtkinter.CTkLabel(self.main_frame, text="", image=self.logo_image)
        self.logo.grid(row=0, column=0, padx=(50,50), pady=(100, 10))

        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="Jigsaw Genius", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="Solve jigsaw & grid jigsaw", font=customtkinter.CTkFont(size=18, weight="normal"))
        self.logo_label.grid(row=2, column=0, padx=10)

        # self.progressbar = customtkinter.CTkProgressBar(self.main_frame)
        # self.progressbar.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.start_button = customtkinter.CTkButton(self.main_frame, text='Start', command=lambda: controller.show_frame("HomeScreen"))
        self.start_button.grid(row=4, column=0, padx=20, pady=10)

        # self.progressbar.configure(mode="indeterminnate")
        # self.progressbar.start()

