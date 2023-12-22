from splash_screen import SplashScreen
from home_screen import HomeScreen
from grid_jigsaw_screen import GridJigsawScreen
from puzzle_with_hint_solver_screen import PuzzleWithHintSolverScreen
from puzzle_solver_screen import PuzzleSolverScreen
from jigsaw_screen import JigsawScreen
from jigsaw_solver_screen import JigsawSolverScreen
from jigsaw_with_hint_solver_screen import JigsawWithHintSolverScreen
from jigsaw_merged_solver_screen import JigsawMergedScreen
import os
import time
from PIL import Image, ImageTk
import sys
import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.geometry("900x700")
        self.title("Jigsaw Genius")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/puzzle.ico")
        self.iconbitmap(image_path)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomeScreen, SplashScreen, GridJigsawScreen, JigsawScreen, PuzzleWithHintSolverScreen, PuzzleSolverScreen, JigsawSolverScreen, JigsawWithHintSolverScreen, JigsawMergedScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")    
            self.frames[page_name] = frame

        self.show_frame("SplashScreen")

    def show_frame(self, page_name, *args, **kwargs):
        filename = kwargs.get('filename', None)
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()