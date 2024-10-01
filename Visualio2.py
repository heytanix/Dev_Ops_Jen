import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualization Tool")
        self.root.geometry("800x600")

        # Create a drag and drop area
        self.drop_area = tk.Label(self.root, text="Drag and drop an Excel or CSV file here", font=("Arial", 24), bg="gray", fg="white")
        self.drop_area.pack(fill="both", expand=True)

        # Create a button to trigger the file selection dialog
        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack()

        # Create a label to display the file path
        self.file_path_label = tk.Label(self.root, text="")
        self.file_path_label.pack()

        # Create a frame for options
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack()

        # Create a label and combo box for graph type
        self.graph_type_label = tk.Label(self.options_frame, text="Graph Type:")
        self.graph_type_label.pack(side=tk.LEFT)
        self.graph_type_combo = ttk.Combobox(self.options_frame, values=["Scatter Plot", "Bar Chart", "Histogram"])
        self.graph_type_combo.pack(side=tk.LEFT)

        # Create a label and combo box for x-axis variable
        self.x_axis_label = tk.Label(self.options_frame, text="X-axis Variable:")
        self.x_axis_label.pack(side=tk.LEFT)
        self.x_axis_combo = ttk.Combobox(self.options_frame)
        self.x_axis_combo.pack(side=tk.LEFT)

        # Create a label and combo box for y-axis variable
        self.y_axis_label = tk.Label(self.options_frame, text="Y-axis Variable:")
        self.y_axis_label.pack(side=tk.LEFT)
        self.y_axis_combo = ttk.Combobox(self.options_frame)
        self.y_axis_combo.pack(side=tk.LEFT)

        # Create a button to visualize the data
        self.visualize_button = tk.Button(self.root, text="Visualize", command=self.visualize_data)
        self.visualize_button.pack()

        # Create a frame to hold the plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack()

    def select_file(self):
        # Open a file selection dialog and get only the file path from the dialog
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

        # Check if a file was selected
        if not file_path:
            print("No file selected.")
            return

        # Load the file into a Pandas dataframe
        if file_path.endswith(".xlsx"):
            self.df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            self.df = pd.read_csv(file_path)
        else:
            print("Unsupported file type.")
            return

        # Clean the column names: Strip spaces, brackets, and remove any weird characters
        self.df.columns = self.df.columns.str.strip(' []').str.replace(r'[^A-Za-z0-9_]', '', regex=True)

        # Display the file path
        self.file_path_label.config(text=file_path)

        # Print out cleaned column names for debugging
        print("Cleaned Column Names:", self.df.columns)

        # Populate the combo boxes with column names
        self.x_axis_combo['values'] = self.df.columns
        self.y_axis_combo['values'] = self.df.columns

    def visualize_data(self):
        # Get the selected graph type and axis variables
        graph_type = self.graph_type_combo.get()
        x_axis = self.x_axis_combo.get().strip()
        y_axis = self.y_axis_combo.get().strip()

        # Check if the axis values are valid (i.e., not empty)
        if not x_axis:
            print("Error: Please select an X-axis variable.")
            return

        if graph_type in ["Scatter Plot", "Bar Chart"] and not y_axis:
            print("Error: Please select a Y-axis variable.")
            return

        # Debug: Print out selected axis values
        print(f"Selected X-axis: {x_axis}, Selected Y-axis: {y_axis}")

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))

        # Plot the data based on the selected graph type
        try:
            if graph_type == "Scatter Plot":
                sns.scatterplot(x=x_axis, y=y_axis, data=self.df)
            elif graph_type == "Bar Chart":
                sns.barplot(x=x_axis, y=y_axis, data=self.df)
            elif graph_type == "Histogram":
                sns.histplot(self.df[x_axis], kde=True)
        except KeyError as e:
            print(f"KeyError: {e}")
            return

        # Clear the previous plot if any
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Create the Tkinter root window and run the app
root = tk.Tk()
app = DataVisualizationTool(root)
root.mainloop()
