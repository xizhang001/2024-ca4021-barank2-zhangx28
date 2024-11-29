# Import necessary libraries
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Progressbar as Progressbar
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
# Tensorflow configurations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, LSTM, Dense
import ctypes

# Child window displaying a dashboard based on results data
from dashboard_page import Dashboard_page

# Change the window resolution
ctypes.windll.shcore.SetProcessDpiAwareness(0)

# Child window for selecting parameters and forecasting
class Specifications_page(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the window
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.title('Specifications Screen')
        self.geometry('1000x600+300+100')
        self.minsize(1000, 600)
        self.wm_state('zoomed')
        self.config(background=self.parent.background)

        # Initialise variables
        self.demand_models = ('SARIMA', 'LSTM', 'GRU')                  # Initialise demand models choice list
        self.chosen_demand_model = tk.StringVar(self, value='SARIMA')   # Set up variable to hold selected model
        self.pricing_methods = ('Range', 'Percentile')                  # Initialise pricing method choice list
        self.chosen_pricing_method = tk.StringVar(self, value='Range')  # Set up variable to hold selected pricing method
        self.uploaded_file_label = tk.StringVar()                       # Set up variable to hold uploaded file's name
        self.uploaded_file_label.set('No Data Uploaded')

        # Validate Command
        self.vcmd = (self.register(self.callback))                      # Make sure typed characters are integers

        # Upload Data Label
        self.forecast_duration_label = tk.Label(self, text='Upload Data', font=('Segoe UI', 13), wraplength=300, **self.parent.label_style)
        self.forecast_duration_label.place(relx=0.27, rely=0.27, width=400, height=50, anchor=tk.CENTER)

        # Uploaded File Button
        self.button = tk.Button(self, textvariable=self.uploaded_file_label, command=self.read_data, **self.parent.button_style)
        self.button.place(relx=0.27, rely=0.35, width=200, height=50, anchor=tk.CENTER)

        # Select Demand Model Label
        self.demand_option_label = tk.Label(self, text='Select Demand Model', font=('Segoe UI', 13), wraplength=300, **self.parent.label_style)
        self.demand_option_label.place(relx=0.5, rely=0.27, width=200, height=50, anchor=tk.CENTER)

        # Select Demand Model Option Menu
        self.demand_option_menu = tk.OptionMenu(self, self.chosen_demand_model, *self.demand_models)
        self.demand_option_menu.place(relx=0.5, rely=0.35, width=200, height=50, anchor=tk.CENTER)
        self.demand_option_menu.config(**self.parent.option_menu_style)
        self.dropdown = self.nametowidget(self.demand_option_menu.menuname)
        self.dropdown.config(font=self.parent.dropdown_style)

        # Select Pricing Method Label
        self.demand_option_label = tk.Label(self, text='Select Pricing Method', font=('Segoe UI', 13), wraplength=300, **self.parent.label_style)
        self.demand_option_label.place(relx=0.73, rely=0.27, width=200, height=50, anchor=tk.CENTER)

        # Select Pricing Method Option Menu
        self.pricing_option_menu = tk.OptionMenu(self, self.chosen_pricing_method, *self.pricing_methods)
        self.pricing_option_menu.place(relx=0.73, rely=0.35, width=200, height=50, anchor=tk.CENTER)
        self.pricing_option_menu.config(**self.parent.option_menu_style)
        self.dropdown = self.nametowidget(self.pricing_option_menu.menuname)
        self.dropdown.config(font=self.parent.dropdown_style)

        # Min. Price Label
        self.min_price_label = tk.Label(self, text='Min. Price', font=('Segoe UI', 13), wraplength=150, **self.parent.label_style)
        self.min_price_label.place(relx=0.26, rely=0.47, width=150, height=50, anchor=tk.CENTER)

        # Min. Price Entry
        self.min_price_entry = tk.Entry(self, justify='center', font=('Segoe UI', 13), validate='all', validatecommand=(self.vcmd, '%P'))
        self.min_price_entry.place(relx=0.26, rely=0.55, width=100, height=50, anchor=tk.CENTER)

        # Max. Price Label
        self.max_price_label = tk.Label(self, text='Max. Price', font=('Segoe UI', 13), wraplength=300, **self.parent.label_style)
        self.max_price_label.place(relx=0.42, rely=0.47, width=150, height=50, anchor=tk.CENTER)

        # Max. Price Entry
        self.max_price_entry = tk.Entry(self, justify='center', font=('Segoe UI', 13), validate='all', validatecommand=(self.vcmd, '%P'))
        self.max_price_entry.place(relx=0.42, rely=0.55, width=100, height=50, anchor=tk.CENTER)

        # Price Interval Label
        self.price_interval_label = tk.Label(self, text='Price Interval', font=('Segoe UI', 13), wraplength=150, **self.parent.label_style)
        self.price_interval_label.place(relx=0.58, rely=0.47, width=150, height=50, anchor=tk.CENTER)

        # Price Interval Entry
        self.price_interval_entry = tk.Entry(self, justify='center', font=('Segoe UI', 13), validate='all', validatecommand=(self.vcmd, '%P'))
        self.price_interval_entry.place(relx=0.58, rely=0.55, width=100, height=50, anchor=tk.CENTER)

        # Forecast Duration Label
        self.forecast_duration_label = tk.Label(self, text='Forecast Duration', font=('Segoe UI', 13), wraplength=150, **self.parent.label_style)
        self.forecast_duration_label.place(relx=0.74, rely=0.47, width=150, height=50, anchor=tk.CENTER)

        # Forecast Duration Entry
        self.forecast_length_entry = tk.Entry(self, justify='center', font=('Segoe UI', 13), validate='all', validatecommand=(self.vcmd, '%P'))
        self.forecast_length_entry.place(relx=0.74, rely=0.55, width=100, height=50, anchor=tk.CENTER)

        # Next Button
        self.button = tk.Button(self, text='Next', command=self.dashboard_page, **self.parent.button_style)
        self.button.place(relx=0.5, rely=0.77, width=200, height=50, anchor=tk.CENTER)
  
        # Progress bar widget 
        self.progressbar = Progressbar(self, orient='horizontal', length=100, mode='determinate')

        # Go Back Button
        self.button = tk.Button(self, command=self.go_back, **self.parent.back_button_style).pack(anchor='nw')

    # Check that typed characters for Forecast Duration are integers
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    # Read provided data into a pandas DataFrame
    def read_data(self):
        self.filepath = tk.filedialog.askopenfilename(initialdir='../data',   # Opens a file dialog window to select a CSV or Excel file.
                                            title='Choose Data File',
                                            filetypes=(('CSV files', '*.csv'), ('Excel files', '*.xls?')),
                                            parent=self)    
        if self.filepath[-3:] == 'csv':
            self.uploaded_df = pd.read_csv(self.filepath)               # Reads the selected CSV file into a pandas DataFrame.
        else:
            self.uploaded_df = pd.read_excel(self.filepath)             # Reads the selected Excel file into a pandas DataFrame.
        
        if len(self.uploaded_df) > 744:                                 # Trim data to last 31 days
            self.uploaded_df = self.uploaded_df.iloc[-744:]
                                                                        # Pre-process dataset
        self.uploaded_df[self.uploaded_df.columns[0]] = pd.to_datetime(self.uploaded_df[self.uploaded_df.columns[0]], dayfirst=True)
        self.uploaded_df.rename(columns={'Energy': 'Energy (kWh)'}, inplace=True)
        self.uploaded_df['Energy (kWh)'] = self.uploaded_df['Energy (kWh)'].round(3)

        self.filename = self.filepath.split('/')[-1]                    # Modify uploaded file label with file name
        self.uploaded_file_label.set(self.filename)

    # Function for forecasting using SARIMAX
    def predict_SARIMAX(self, train, test_steps, order, seasonal_order):
        (p,d,q) = order
        (P,D,Q) = seasonal_order
        self.model = SARIMAX(train, order=(p,d,q), seasonal_order=(P,D,Q,24))       # Initialise model
        self.progressbar['value'] = 30                                              # Change progressbar gradually
        self.update_idletasks()
        self.fitted = self.model.fit(disp=0)                                        # Fit model to training data
        self.progressbar['value'] = 50
        self.update_idletasks()
        self.demand_predictions = self.fitted.forecast(test_steps)                  # Forecast demand
        self.demand_predictions[self.demand_predictions < 0] = 0                    # Ensure energy values are not negative
        self.demand_predictions = self.demand_predictions.reset_index(drop=True)
        self.progressbar['value'] = 70
        self.update_idletasks()
        self.demand_predictions = [np.round(f, 3) for f in self.demand_predictions]

    # Function for preparing training data for GRU and LSTM
    def create_dataset (self, input_data, look_back):
        features, values = [], []
        
        for i in range(len(input_data)-look_back):
            feature = input_data[i:i+look_back]
            features.append(feature)
            values.append(input_data[i+look_back])
            self.progressbar['value'] = 30
            self.update_idletasks()
            
        return np.array(features), np.array(values)
    
    # Function for creating a GRU model
    def create_gru_model(self, nodes_per_layer, trainX):
        self.model = Sequential()
        self.model.add(tf.keras.Input(shape=(trainX.shape[1], trainX.shape[2])))     # Define shape
        self.model.add(GRU(units = nodes_per_layer, return_sequences = True))        # Input layer
        self.model.add(GRU(units = nodes_per_layer))                                 # Hidden layer
        self.model.add(Dense(units = 1))                                             # Output layer 
        self.model.compile(optimizer='adam', loss='mse')                             # Compile model
        self.progressbar['value'] = 50
        self.update_idletasks()

    # Function for creating an LSTM model
    def create_lstm_model(self, nodes_per_layer, trainX):
        self.model = Sequential()
        self.model.add(tf.keras.Input(shape=(trainX.shape[1], trainX.shape[2])))     # Define shape
        self.model.add(LSTM(units = nodes_per_layer, return_sequences = True))       # Input layer
        self.model.add(LSTM(units = nodes_per_layer))                                # Hidden layer
        self.model.add(Dense(units = 1))                                             # Output layer 
        self.model.compile(optimizer='adam', loss='mse')                             # Compile model
        self.progressbar['value'] = 50
        self.update_idletasks()

    # Function for making predictions iteratively using self-feedback
    def iterative_forecast(self, look_back):
        forecast = []                                # Results
        look_back_data = self.trainY[-look_back:]    # Initial input
        train_mean = self.trainY[:,1].mean()         # Mean demand value
        train_max = self.trainY[:,1].max()           # Max. demand value

        # Predict iteratively
        i = 0
        while i < self.forecast_length:
            prediction = self.model.predict(np.expand_dims(look_back_data, axis=0), verbose=0)

            # Round predictions below mean to zero
            if prediction[0][0] < train_mean:
                prediction[0][0] = 0
            # Cap predictions at max. demand value
            elif prediction[0][0] > train_max:
                prediction[0][0] = train_max
            
            look_back_minus_last = np.delete(look_back_data, 0, axis=0)             # Remove oldest input sample
            next_hour = np.array((look_back_minus_last[-1,0] + 1) % 24)             # Calculate next hour feature
            new_point = pd.DataFrame({'hour': next_hour, 'energy': prediction[0]})  # Combine next hour and predicted demand
            look_back_data = np.append(look_back_minus_last, new_point, axis=0)     # Add predicted values as input for next prediction
            forecast.append(prediction[0][0])                                       # Record result
            i = i + 1

        return forecast

    # Function for creating a price profile using the range pricing method
    def range_pricing(self):

        # The range of demand is split into equal bins, one for each possible price
        max_demand = max(self.demand_predictions)
        min_demand = min(self.demand_predictions)
        price_set_count = len(self.price_set)
        bin_size = (max_demand - min_demand) / price_set_count

        # Demand thresholds for each price are calculated
        demand_thresholds = []
        j = 1
        while j < price_set_count + 1:
            demand_thresholds.append(min_demand + bin_size * j)
            j = j + 1

        # To tackle float representation imprecision, the highest demand threshold is increased a little
        demand_thresholds[-1] = demand_thresholds[-1] + 1

        # Every demand value is compared with the demand thresholds and assigned a demand-proportional price
        self.price_profile = []
        i = 0
        while i < len(self.demand_predictions):
            j = 0
            while j < price_set_count:
                if self.demand_predictions[i] <= demand_thresholds[j]:
                    self.price_profile.append(self.price_set[j])
                    break
                j = j + 1
            i = i + 1

    # Function for creating a price profile using the percentile pricing method
    def percentile_pricing(self):

        # Percentile thresholds for each price are calculated
        price_set_count = len(self.price_set)
        bin_size = 100 / price_set_count
        percentile_thresholds = []
        j = 1
        while j < price_set_count + 1:
            percentile_thresholds.append(bin_size * j)
            j = j + 1

        # Demand thresholds for each price are calculated
        demand_thresholds = []
        for k in percentile_thresholds:
            demand_thresholds.append(np.percentile(self.demand_predictions, k))

        # Every demand value is compared with the demand thresholds and assigned a demand-proportional price
        self.price_profile = []
        i = 0
        while i < len(self.demand_predictions):
            j = 0
            while j < price_set_count:
                if self.demand_predictions[i] <= demand_thresholds[j]:
                    self.price_profile.append(self.price_set[j])
                    break
                j = j + 1
            i = i + 1

    # Forecast demand, employ a pricing method, calculate forecasted revenue and prepare result datasets for downloading
    def start_forecast(self):
        # Collect chosen parameters as variables
        self.demand_model = self.chosen_demand_model.get()
        self.pricing_method = self.chosen_pricing_method.get()
        self.forecast_length = int(self.forecast_length_entry.get())
        self.min_price = int(self.min_price_entry.get())
        self.max_price = int(self.max_price_entry.get())
        self.price_interval = int(self.price_interval_entry.get())

        # Validate the provided parameters
        assert self.min_price < self.max_price
        assert self.forecast_length != 0
        assert self.price_interval != 0
        self.price_set = np.arange(self.min_price, self.max_price + 1, self.price_interval)/100 # List of all possible prices
        assert self.price_set[0] == self.min_price / 100
        assert self.price_set[-1] == self.max_price / 100

        # Calculate the time values to forecast
        self.forecasted_time_range = self.uploaded_df.iloc[-1,0] + pd.Timedelta(hours=1) + pd.to_timedelta(np.arange(self.forecast_length), 'h') 

        self.progressbar['value'] = 10         # Change progressbar gradually
        self.update_idletasks()

        # Forecast demand
        ## SARIMA
        if self.demand_model == 'SARIMA':
            self.predict_SARIMAX(self.uploaded_df.iloc[:,1], self.forecast_length, (0,0,0), (1,1,1)) # Fixed parameters for SARIMA

        ## GRU
        elif self.demand_model == 'GRU':
            look_back = 24          # How many past values are considered as features
            nodes_per_layer = 128   # How many nodes in each of the model's layers

            # If the training data is too short, modify look_back
            if look_back > len(self.uploaded_df):
                look_back = len(self.uploaded_df) // 2

            # Prepare dataset for training the GRU model
            features = pd.DataFrame({'hour': self.uploaded_df.iloc[:,0].dt.hour, 'energy': self.uploaded_df.iloc[:,1].values})
            self.trainX, self.trainY = self.create_dataset(np.array(features), look_back)
    
            # Create and train the GRU model
            self.create_gru_model(nodes_per_layer, self.trainX)
            self.model.fit(self.trainX, self.trainY, epochs=50, batch_size=16, verbose=0)

            # Make predictions
            self.demand_predictions = self.iterative_forecast(look_back)

        ## LSTM
        else:
            look_back = 48         # How many past values are considered as features
            nodes_per_layer = 64   # How many nodes in each of the model's layers

            # If the training data is too short, modify look_back
            if look_back > len(self.uploaded_df):
                look_back = len(self.uploaded_df) // 2

            # Prepare dataset for training the GRU model
            features = pd.DataFrame({'hour': self.uploaded_df.iloc[:,0].dt.hour, 'energy': self.uploaded_df.iloc[:,1].values})
            self.trainX, self.trainY = self.create_dataset(np.array(features), look_back)

            # Create and train the LSTM model
            self.create_lstm_model(nodes_per_layer, self.trainX)
            self.model.fit(self.trainX, self.trainY, epochs=50, batch_size=16, verbose=0)

            # Make predictions
            self.demand_predictions = self.iterative_forecast(look_back)

        self.progressbar['value'] = 80          # Change progressbar gradually
        self.update_idletasks()

        # Employ a pricing method to generate a price profile for the future
        ## Range
        if self.pricing_method == 'Range':
            self.range_pricing()

        ## Percentile
        else:
            self.percentile_pricing()

        self.progressbar['value'] = 90          # Change progressbar gradually
        self.update_idletasks()

        # Calculate revenue given forecasted demand and generated price profile
        self.revenue_predictions = np.round(np.array(self.price_profile) * np.array(self.demand_predictions), 2)
    
        # Create DataFrame with forecasted results
        self.final_df = pd.DataFrame({'Hour': self.forecasted_time_range, 'Energy (kWh)': self.demand_predictions,
                                  'Price': self.price_profile, 'Revenue': self.revenue_predictions})

        self.progressbar['value'] = 100         # Change progressbar gradually
        self.update_idletasks()

    # Conduct forecast and open next window
    def dashboard_page(self):
        # Make sure all parameters are valid
        try:
            self.progressbar.place(relx=0.5, rely=0.7, width=200, height=25, anchor=tk.CENTER)         # Make progressbar appear
            self.start_forecast()
            self.child = Dashboard_page(self)
            self.child.grab_set()

        except AttributeError:                      # Raised if no data file is submitted
            self.progressbar.place_forget()                                                            # Make progressbar disappear
            self.update_idletasks()
            self.error_message('No data uploaded!')

        except ValueError:                          # Raised if not all entry fields are filled out
            self.progressbar.place_forget()                                                            # Make progressbar disappear
            self.update_idletasks()
            self.error_message('Please fill in all fields.')

        except AssertionError:                      # Raised if parameters in entry fields are erroneous
            self.progressbar.place_forget()                                                            # Make progressbar disappear
            self.update_idletasks()
            self.error_message('The supplied parameters need to be corrected.')

    # Return to parent window
    def go_back(self):
        self.uploaded_df = pd.DataFrame()       # Reset the uploaded dataset
        self.destroy()                          # Close current window

    # Show an error message on the screen
    def error_message(self, message):
        showerror(parent=self, title='Error', message=message)

    # When the user exits he is asked to confirm
    def on_exit(self):
        if tk.messagebox.askyesno("Exit", "Do you want to quit the application?", parent=self):
            self.parent.destroy()           # Quit the app