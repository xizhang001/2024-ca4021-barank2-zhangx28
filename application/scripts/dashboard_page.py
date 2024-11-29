# Import necessary libraries
import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Progressbar as Progressbar
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
import ctypes

# Change the window resolution
ctypes.windll.shcore.SetProcessDpiAwareness(0)

# Child window displaying a dashboard based on results data
class Dashboard_page(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the window
        self.parent = parent
        self.title('Dashboard')
        self.wm_state('zoomed')
        self.geometry('1000x700+300+100')
        self.minsize(1000, 700)
        self.background = 'white'
        self.config(background=self.background)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Style dictionary
        self.dashboard_label_options = {'font': ('Segoe UI', 13), 'anchor': 'center', 'background': self.background,
                                        'foreground': 'black', 'borderwidth': 0, 'relief': 'solid', 'wraplength': 350, 'justify': 'center'}
        
        # Total Forecasted Revenue Label
        self.forecasted_revenue = tk.StringVar()
        self.forecasted_revenue.set(f'Total Forecasted Revenue = {np.round(self.parent.final_df.Revenue.sum(), 2):.2f}')
        self.forecasted_revenue_label = tk.Label(self, textvariable = self.forecasted_revenue, **self.dashboard_label_options)
        self.forecasted_revenue_label.place(relx=0.28, rely=0.05, width=400, height=50, anchor=tk.N)

        # Total Forecasted Demand Label
        self.forecasted_demand = tk.StringVar()
        self.forecasted_demand.set('Total Forecasted Demand = ' + str(np.round(self.parent.final_df['Energy (kWh)'].sum(), 3)) + ' kWh')
        self.forecasted_demand_label = tk.Label(self, textvariable = self.forecasted_demand, **self.dashboard_label_options)
        self.forecasted_demand_label.place(relx=0.72, rely=0.05, width=400, height=50, anchor=tk.N)

        # Process datasets for plotting
        self.max_num_ticks = 8
        self.process_historical_data()
        self.process_forecast_data()

        # Time formats for plots' x-axes
        hour_formatter = DateFormatter('%d/%m-%H:%M')
        day_formatter = DateFormatter('%d/%m/%y')

        # Configure chart figure
        self.figure, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)      # Create (3x2) subplots
        self.figure.patch.set_facecolor('xkcd:white')
        self.figure.set_figheight(6)
        self.figure.set_figwidth(10)

        # Historical Demand by Day Chart
        self.chart('bar', ax1, self.historical_day_df.Day, self.historical_day_df['Energy (kWh)'],
                        self.day_historical_xticks, 'Historical Demand by Day', 'Energy (kWh)', day_formatter)

        # Historical Demand by Hour Chart
        self.chart('line', ax2, self.parent.uploaded_df.Hour, self.parent.uploaded_df['Energy (kWh)'], self.hour_historical_xticks,
                        'Historical Demand by Hour', 'Energy (kWh)', hour_formatter)

        # Forecasted Demand by Day Chart
        self.chart('bar', ax3, self.forecast_day_df.Day, self.forecast_day_df['Energy (kWh)'],
                        self.day_forecast_xticks, 'Forecasted Demand by Day', 'Energy (kWh)', day_formatter)

        # Forecasted Demand by Hour Chart
        self.chart('line', ax4, self.parent.final_df.Hour, self.parent.final_df['Energy (kWh)'], self.hour_forecast_xticks,
                        'Forecasted Demand by Hour', 'Energy (kWh)', hour_formatter)

        # Forecasted Revenue by Day Chart
        self.chart('bar', ax5, self.forecast_day_df.Day, self.forecast_day_df['Revenue'],
                        self.day_forecast_xticks, 'Forecasted Revenue by Day', 'Revenue', day_formatter)

        # Forecasted Demand & Price by Hour Chart
        ax62 = ax6.twinx()
        self.double_chart(ax6, ax62, self.parent.final_df.Hour, self.parent.final_df['Energy (kWh)'],
                        self.parent.final_df['Price'], self.hour_forecast_xticks, self.price_set_yticks,
                        'Price Proportionality to Demand', 'Energy (kWh)', 'Price', hour_formatter, 'blue', 'orange', 'Demand', 'Price')

        plt.tight_layout(h_pad=3)

        # Create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().place(relx=0.5, rely=0.85, relheight=0.7, relwidth=1, anchor=tk.S)

        # Create the toolbar
        NavigationToolbar2Tk(self.figure_canvas, self)

        # Download Data Button
        self.button = tk.Button(self, text='Download Results', command=self.download_data, **self.parent.parent.button_style)
        self.button.place(relx=0.5, rely=0.89, width=200, height=50, anchor=tk.CENTER)

        # Go Back Button
        self.button = tk.Button(self, command=self.go_back, image=self.parent.parent.back_button_image, compound='left', background='white',
                                 width=60, height=60,activebackground='white', relief='flat', borderwidth=0).pack(anchor='nw')

    # Function preparing historical data for plotting
    def process_historical_data(self):
        # Prepare historical daily data
        self.historical_day_df = self.parent.uploaded_df.resample('D', on='Hour').sum()                     # Aggregate data on day
        self.historical_day_df.reset_index(inplace=True)
        self.historical_day_df.rename(columns={'Hour': 'Day'}, inplace=True)
        self.historical_day_df['Day'] = self.historical_day_df['Day'].dt.date
        day_historical_skip_num = (self.historical_day_df.Day.count() // self.max_num_ticks) + 1            # Select a subset of x_ticks
        self.day_historical_xticks = self.historical_day_df.Day[::day_historical_skip_num]

        # Prepare historical hourly data
        hour_historical_filtered = self.parent.uploaded_df[(self.parent.uploaded_df.Hour.dt.hour == 0) |    # Filter x_ticks
                    (self.parent.uploaded_df.Hour.dt.hour == 3) | (self.parent.uploaded_df.Hour.dt.hour == 6) | 
                    (self.parent.uploaded_df.Hour.dt.hour == 9) | (self.parent.uploaded_df.Hour.dt.hour == 12) | 
                    (self.parent.uploaded_df.Hour.dt.hour == 15) | (self.parent.uploaded_df.Hour.dt.hour == 18) | 
                    (self.parent.uploaded_df.Hour.dt.hour == 21)].Hour
        hour_historical_skip_num = (hour_historical_filtered.count() // self.max_num_ticks) + 1             # Select a subset of filtered x_ticks
        self.hour_historical_xticks = hour_historical_filtered[::hour_historical_skip_num]

    # Function preparing forecasted data for clean plotting
    def process_forecast_data(self):
        # Prepare forecasted daily data
        self.forecast_day_df = self.parent.final_df.resample('D', on='Hour').sum()                          # Aggregate data on day
        self.forecast_day_df.drop('Price', axis=1, inplace=True)
        self.forecast_day_df.reset_index(inplace=True)
        self.forecast_day_df.rename(columns={'Hour': 'Day'}, inplace=True)
        self.forecast_day_df['Day'] = self.forecast_day_df['Day'].dt.date
        day_forecast_skip_num = (self.forecast_day_df.Day.count() // self.max_num_ticks) + 1                # Select a subset of x_ticks
        self.day_forecast_xticks = self.forecast_day_df.Day[::day_forecast_skip_num]

        # Prepare forecasted hourly data
        if len(self.parent.final_df.Hour) <= self.max_num_ticks:                                            # No need to filter x_ticks
            self.hour_forecast_xticks = self.parent.final_df.Hour
        else:
            hour_forecast_filtered_midnight = self.parent.final_df[(self.parent.final_df.Hour.dt.hour == 0) |    # Filter x_ticks
                    (self.parent.final_df.Hour.dt.hour == 3) | (self.parent.final_df.Hour.dt.hour == 6) |
                    (self.parent.final_df.Hour.dt.hour == 9) | (self.parent.final_df.Hour.dt.hour == 12) |
                    (self.parent.final_df.Hour.dt.hour == 15) | (self.parent.final_df.Hour.dt.hour == 18) |
                    (self.parent.final_df.Hour.dt.hour == 21)].Hour
            hour_forecast_skip_num = (hour_forecast_filtered_midnight.count() // self.max_num_ticks) + 1    # Select a subset of filtered x_ticks
            self.hour_forecast_xticks = hour_forecast_filtered_midnight[::hour_forecast_skip_num]

        # Prepare price set
        if len(self.parent.price_set) <= 5:                                                                 # No need to filter price set
                    self.price_set_yticks = self.parent.price_set
        else:
            price_set_skip_num = (len(self.parent.price_set) // 5) + 1                                      # Select a subset of price set
            self.price_set_yticks = self.parent.price_set[::price_set_skip_num]

    # Function to plot bar and line charts    
    def chart(self, chart_type, axis, x, y, x_ticks, title, y_label, x_formatter):
        if chart_type == 'bar':
            axis.bar(x, y)
        else:
            axis.plot(x, y)
        axis.set_xticks(x_ticks)
        axis.set_xticklabels(x_ticks, rotation=30)
        axis.set_title(title)
        axis.set_ylabel(y_label)
        axis.xaxis.set_major_formatter(x_formatter)

    # Function to plot a line chart with double y-axis
    def double_chart(self, axis1, axis2, x, y1, y2, x_ticks, y_ticks2, title, y_label1, y_label2, x_formatter, colour1, colour2, label1, label2):
        line1 = axis1.plot(x, y1, color=colour1, label=label1)
        line2 = axis2.plot(x, y2, color=colour2, label=label2)
        plt.setp(((axis2)), yticks=y_ticks2)
        axis1.set_xticks(x_ticks)
        axis1.set_xticklabels(x_ticks, rotation=30)
        axis1.set_title(title)
        axis1.set_ylabel(y_label1)
        axis2.set_ylabel(y_label2)
        axis1.xaxis.set_major_formatter(x_formatter)
        lines = line1+line2
        labels = [l.get_label() for l in lines]
        axis1.legend(lines, labels, loc='upper left', fontsize=8)

    # Function to download results data
    def download_data(self):
        self.file_name = self.parent.chosen_demand_model.get() + '_' + self.parent.chosen_pricing_method.get() + '_Forecast.xlsx'
        try:
            with pd.ExcelWriter('../data/' + self.file_name) as writer:           # Four Excel sheets are included in the .xlsx file
                self.parent.uploaded_df.to_excel(writer, sheet_name='Historical Data by Hour', index=False)
                self.historical_day_df.to_excel(writer, sheet_name='Historical Data by Day', index=False)
                self.parent.final_df.to_excel(writer, sheet_name='Forecasted Data by Hour', index=False)
                self.forecast_day_df.to_excel(writer, sheet_name='Forecasted Data by Day', index=False)
            self.information_message('Results were downloaded into ' + self.file_name + '.')

        except PermissionError:                                             # If PermissionError is raised
            self.error_message('Results could not be downloaded because the file ' + self.file_name + ' is currently open.')

    # Return to parent window
    def go_back(self):
        self.parent.progressbar.place_forget()          # Delete the progressbar
        self.update_idletasks()
        self.parent.focus_force()                       # Ensure the user sees the Specification Page
        self.destroy()                                  # Close the window

    # Show an information message on the screen
    def information_message(self, message):
        showinfo(parent=self, title='Information', message=message)

    # Show an error message on the screen
    def error_message(self, message):
        showerror(parent=self, title='Error', message=message)

    # When the user exits he is asked to confirm
    def on_exit(self):
        if tk.messagebox.askyesno("Exit", "Do you want to quit the application?", parent=self):
            self.parent.parent.destroy()                # Quit the app