# Import necessary libraries
import tkinter as tk
from tkinter import scrolledtext
import ctypes

# Change the window resolution
ctypes.windll.shcore.SetProcessDpiAwareness(0)

# Child window explaining the project
class About_page(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the window
        self.parent = parent
        self.title('About Screen')
        self.geometry('1300x600+100+100')
        self.minsize(1300, 600)
        self.wm_state('zoomed')
        self.config(background=self.parent.background)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # About page ScrolledText 
        self.text_area = scrolledtext.ScrolledText(self, font=("Times New Roman", 15)) 
        self.text_area.place(relx=0.5, rely=0.5, width=1170, relheight=1, anchor='c')
        
        # Inserting text 
        self.text_area.insert(tk.INSERT, """\n       What is the purpose of this application?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        This application has been designed with electric vehicle charging station owners in mind and aims to support them by generating a
        demand-proportional pricing profile for the future. The application also supports predicting demand and exploratory data analysis
        using a dashboard.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """What is meant by a demand-proportional pricing profile?""", 'title')
        self.text_area.insert(tk.INSERT,
        """
        
        What is meant is that the price per unit energy at an EV charging station in a given hour would be set high if demand is expected 
        to be high and low if demand is expected to be low. Implementing a demand-proportional pricing strategy such as range or percentile
        pricing may lead to boosting demand at off-peak times and lowering demand at peak times. This means the method has potential in 
        decreasing grid base load and increasing total customer turnover, leading to increased profits for the business while staying competitive.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """How to use the application?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        The user may use the application as follows:
        1. The EV station's historical demand may be supplied by the user to predict future demand using SARIMA, GRU or LSTM methods.
        2. Demand-proportional prices for each hour may be calculated using innovative Range and Percentile pricing methods.
        3. Once calculations are complete, a dashboard is created based on historical and forecasted data to help the user understand the results.
        4. In the end, the user may export the dashboard image or download the analysis results.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """What are range and percentile pricing methods?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        Range and percentile pricing methods assign a price from the user-defined range to an hour based on its total demand and the distribution
        of historical demand. Range pricing works by dividing the historical demand data range (max-min) into equal intervals, locating the 
        interval containing the demand value and assigning the interval's respective price to the hour. Percentile pricing method works on the 
        same principle except that intervals are based on percentile steps, so each interval has roughly the same count of demand values.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """How do different methods compare in terms of metrics?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        The application's forecasting and pricing methods have been examined in an accompanying report. Noteworthy conclusions of the tests
        carried out are that LSTM and GRU have poorer forecasting potential than SARIMA and that range pricing method is more
        demand-proportional compared to percentile pricing. It is recommended to forecast using SARIMA since it is the fastest and most accurate
        forecasting method.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """Who are the authors?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        The creators of this application are Dublin City University data science students Krzysztof Baran and Xi Zhang. The application has been
        developed in 2024 as part of their bachelor degree's final year project. The supervisor for the project was Dr. Mohammed Amine Togou.
        """, 'normal') 

        # Make titles bold
        self.text_area.tag_config('title', font='bold')

        # Making the text read only 
        self.text_area.configure(state ='disabled') 

        # Go Back Button
        self.button = tk.Button(self, command=self.destroy, **self.parent.back_button_style).pack(anchor='nw')

    # When the user exits he is asked to confirm
    def on_exit(self):
        if tk.messagebox.askyesno("Exit", "Do you want to quit the application?", parent=self):
            self.parent.destroy()           # Quit the app