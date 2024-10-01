'''
tkinter
pandas
matplotlib
seaborn
'''

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

        # Create a canvas to display the visualization
        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.canvas.pack()

    def select_file(self):
        # Open a file selection dialog
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

        # Load the file into a Pandas dataframe
        if file_path.endswith(".xlsx"):
            self.df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            self.df = pd.read_csv(file_path)

        # Display the file path
        self.file_path_label.config(text=file_path)

        # Populate the combo boxes with column names
        self.x_axis_combo['values'] = self.df.columns
        self.y_axis_combo['values'] = self.df.columns

    def visualize_data(self):
        # Get the selected graph type and axis variables
        graph_type = self.graph_type_combo.get()
        x_axis = self.x_axis_combo.get()
        y_axis = self.y_axis_combo.get()

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))

        # Plot the data based on the selected graph type
        if graph_type == "Scatter Plot":
            sns.scatterplot(x=x_axis, y=y_axis, data=self.df)
        elif graph_type == "Bar Chart":
            sns.barplot(x=x_axis, y=y_axis, data=self.df)
        elif graph_type == "Histogram":
            sns.histplot(self.df[x_axis], kde=True)

        # Show the plot
        plt.tight_layout()
        plt.close()

        # Convert the plot to a Tkinter image
        fig.canvas.draw()
        img = tk.PhotoImage(file="temp.png")

        # Display the image on the canvas
        self.canvas.create_image(0, 0, image=img, anchor="nw")

root = tk.Tk()
app = DataVisualizationTool(root)
root.mainloop()