# Import necessary libraries
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import ctypes

# Child window explaining the project
from about_page import About_page

# Child window explaining the project
from help_page import Help_page

# Child window for selecting parameters and forecasting
from specifications_page import Specifications_page

# Change the window resolution
ctypes.windll.shcore.SetProcessDpiAwareness(0)

# Root window
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the root window
        self.attributes('-topmost', True)                       # Ensure app appears on top at start-up
        self.title('Home Screen')
        self.geometry('1000x600+300+100')
        self.minsize(1000, 600)
        self.wm_state('zoomed')
        self.background = 'paleturquoise'
        widget_colour = '#ffdb58'
        self.config(background=self.background)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
    
        # Back button image
        self.back_button_image = ImageTk.PhotoImage(Image.open("../images/back_button.png").resize((50, 50)))

        # Logo image
        self.logo_image = ImageTk.PhotoImage(Image.open("../images/app_logo.png").resize((200, 150)))

        # Style dictionaries
        self.button_style = {'anchor': 'center', 'font': ('Segoe UI', 13), 'background': widget_colour, 'foreground': 'black',
                'borderwidth': 1, 'relief': 'solid', 'activebackground': widget_colour, 'wraplength': 180}

        self.back_button_style = {'image': self.back_button_image, 'compound': 'left', 'background': self.background, 'width': 60, 'height': 60,
                                'activebackground': self.background, 'relief': 'flat', 'borderwidth': 0}
        
        self.option_menu_style = {'font': ('Segoe UI', 13), 'background': widget_colour, 'activebackground': widget_colour,
                               'border': 1,'highlightthickness': 0, 'relief': 'solid'}
        
        self.label_style = {'anchor': 'center', 'background': self.background, 'foreground': 'black', 'borderwidth': 0, 'relief': 'solid'}

        self.dropdown_style = tkFont.Font(size=13)

        # Header Label
        self.label = tk.Label(self, image=self.logo_image, background=self.background)
        self.label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Start Button
        self.button = tk.Button(self, text='Start', command=self.specifications_page, **self.button_style)
        self.button.place(relx=0.5, rely=0.4, width=200, height=50, anchor=tk.CENTER)

        # About Button
        self.button = tk.Button(self, text='About', command=self.about_page, **self.button_style)
        self.button.place(relx=0.5, rely=0.52, width=200, height=50, anchor=tk.CENTER)

        # User Manual Button
        self.button = tk.Button(self, text='Help', command=self.help_page, **self.button_style)
        self.button.place(relx=0.5, rely=0.64, width=200, height=50, anchor=tk.CENTER)

        # Quit Button
        self.button = tk.Button(self, text='Quit', command=self.destroy, **self.button_style)
        self.button.place(relx=0.5, rely=0.76, width=200, height=50, anchor=tk.CENTER)

    # Open next window
    def specifications_page(self):
        self.child = Specifications_page(self)
        self.attributes('-topmost', False)                       # Allow other windows to appear in front
        self.child.grab_set()

    # Open next window
    def about_page(self):
        self.child = About_page(self)
        self.attributes('-topmost', False)                       # Allow other windows to appear in front
        self.child.grab_set()

    # Open next window
    def help_page(self):
        self.child = Help_page(self)
        self.attributes('-topmost', False)                       # Allow other windows to appear in front
        self.child.grab_set()

    # When the user exits he is asked to confirm
    def on_exit(self):
        if tk.messagebox.askyesno("Exit", "Do you want to quit the application?", parent=self):
            self.destroy()                  # Quit the app