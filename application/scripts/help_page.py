# Import necessary libraries
import tkinter as tk
from tkinter import scrolledtext
import ctypes

# Change the window resolution
ctypes.windll.shcore.SetProcessDpiAwareness(0)

# Child window explaining the project
class Help_page(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the window
        self.parent = parent
        self.title('Help Screen')
        self.geometry('1300x600+100+100')
        self.minsize(1300, 600)
        self.wm_state('zoomed')
        self.config(background=self.parent.background)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Help page ScrolledText 
        self.text_area = scrolledtext.ScrolledText(self, font=("Times New Roman", 15)) 
        self.text_area.place(relx=0.5, rely=0.5, width=1170, relheight=1, anchor='c')
        
        # Inserting text 
        self.text_area.insert(tk.INSERT, """\n       How to upload historical demand data?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        Click the orange button below the "Upload Data" text on the Specifications Screen. Find your data file in the file dialog and select it.
        Once your data is uploaded, its file name will appear on the orange button.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """What format should the uploaded data file have?""", 'title')
        self.text_area.insert(tk.INSERT,
        """

        It is important that your data file satisfies the following requirements:
        1. Is a CSV or Excel file
        2. Has a header in the first row
        3. The first column contains datetimes representing hours and the second column contains floats representing demand in given hour
        4. The rows are ordered in ascending order of time and do not have missing hour entries

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """How to choose a demand model / pricing method?""", 'title')
        self.text_area.insert(tk.INSERT, 
        """

        Click the orange buttons below the "Select Demand Model" / "Select Pricing Method" texts respectively and choose a parameter each. If
        nothing is chosen, the application will default with SARIMA and Range pricing.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """What values are acceptable in the white entry fields?""", 'title')
        self.text_area.insert(tk.INSERT, 
        """

        Only integers are acceptable. "Min. Price", "Max. Price" and "Interval" are accepted in units of cents while "Forecast Duration"
        represents the number of hours to forecast. In addition, the application validates that "Min. Price" is less than "Max. Price", "Interval"
        is a factor of the difference between "Min. Price" and "Max. Price" as well as that "Interval" and "Forecast Duration" are greater than
        zero.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """Why does forecasting using GRU and LSTM take long to process?""", 'title')
        self.text_area.insert(tk.INSERT, 
        """

        This is because both methods are machine learning algorithms and require a lot of number-crunching to build a model, fit data to it and
        use it to forecast ahead. According to experiments, the models take at least a minute to forecast and the time necessary increases the
        higher the forecast duration. SARIMA on the other hand is a statistical forecasting method and in this application has pre-defined
        parameters ((0,0,0), (1,1,1)) so it takes less time to forecast.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """How can the charts in the dashboard be panned / enlarged / saved?""", 'title')
        self.text_area.insert(tk.INSERT, 
        """

        These actions are supported by clicking the buttons on the gray navigation bar below the dashboard. The plots can be zoomed in once the
        magnifying glass button is selected and a rectangular area selected on the plot. When saving the plot as an image, the user can name it and
        choose a directory to save it in.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """How can I return to the previous page?""", 'title')
        self.text_area.insert(tk.INSERT, 
        """

        Clicking the arrow icon in the top-left corner of the screen will navigate the user to the previous page. When returning from the 
        Specifications Screen to the Home Screen, all parameters chosen and data uploaded will be reset. This is not the case when returning from
        the Dashboard.

        -------------------------------------------------------------------------------------------------------------------------------------------------------------

        """, 'normal') 
        self.text_area.insert(tk.INSERT, """How to quit the application?""", 'title')
        self.text_area.insert(tk.INSERT, 
        """

        The user may quit the application by clicking on the "Quit" button on the Home Screen or by clicking on the "X" in the top-right corner of
        any screen and confirming.
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