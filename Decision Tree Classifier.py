#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Elementary Logic Gate Classifier Using Decision Tree Algorithm
Corresponding Author: Shi Shuo

Description:
A Tkinter-based GUI tool to identify logic gates based on normalized 
fluorescence or absorbance input data. Designed for reproducibility in 
research publications involving molecular logic systems.

Requirements:
- Python 3.13
- pandas
- numpy
- scikit-learn
- tkinter (usually included with Python)

Usage:
Run this script using Python. Enter four intensity values corresponding 
to the binary inputs (00, 01, 10, 11), specify the maximum intensity 
and threshold if needed, and click 'Predict' to classify the logic gate.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import random
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# ------------------ Training Data Setup ------------------

# Logic gate output patterns and their intensity scaling
logic_gates = {
    'YES1':  {'values': [0, 0, 1, 1], 'intensity_max': 2000},
    'YES2':  {'values': [0, 1, 0, 1], 'intensity_max': 2000},
    'NOT1':  {'values': [1, 1, 0, 0], 'intensity_max': 2000},
    'NOT2':  {'values': [1, 0, 1, 0], 'intensity_max': 2000},
    'INH1':  {'values': [0, 1, 0, 0], 'intensity_max': 2000},
    'INH2':  {'values': [0, 0, 1, 0], 'intensity_max': 2000},
    'IMP1':  {'values': [1, 0, 1, 1], 'intensity_max': 2000},
    'IMP2':  {'values': [1, 1, 0, 1], 'intensity_max': 2000},
    'OR':    {'values': [0, 1, 1, 1], 'intensity_max': 2000},
    'NOR':   {'values': [1, 0, 0, 0], 'intensity_max': 2000},
    'PASS1': {'values': [1, 1, 1, 1], 'intensity_max': 2000},
    'PASS0': {'values': [0, 0, 0, 0], 'intensity_max': 1},     # Special case
    'XOR':   {'values': [0, 1, 1, 0], 'intensity_max': 2000},
    'XNOR':  {'values': [1, 0, 0, 1], 'intensity_max': 2000},
    'AND':   {'values': [0, 0, 0, 1], 'intensity_max': 2000},
    'NAND':  {'values': [1, 1, 1, 0], 'intensity_max': 2000}
}

# Prepare normalized training dataset
X_data = []
y_data = []

for gate, data in logic_gates.items():
    scaled = [val * data['intensity_max'] for val in data['values']]
    X_data.append(scaled)
    y_data.append(gate)

X = pd.DataFrame(X_data, columns=['00', '01', '10', '11'])
y = pd.Series(y_data)

X_normalized = X.copy()
for i in range(len(X)):
    max_val = logic_gates[y[i]]['intensity_max']
    X_normalized.iloc[i] = X.iloc[i] / max_val

# Train Decision Tree classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_normalized, y)

# ------------------ GUI Application ------------------

class LogicGateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Elementary Logic Gate Identifier")

         # Create a menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
    
        # Add Home and About menu
        menu_bar.add_command(label="Home", command=lambda: None)  # Placeholder
        menu_bar.add_command(label="About", command=self.show_about)

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Intensity max input
        intensity_frame = ttk.Frame(main_frame)
        intensity_frame.pack(pady=5, fill=tk.X)
        ttk.Label(intensity_frame, text="Maximum intensity (FL/Abs)").pack(side=tk.LEFT)
        self.max_intensity_entry = ttk.Entry(intensity_frame)
        self.max_intensity_entry.pack(side=tk.LEFT, padx=5)
        self.max_intensity_entry.insert(0, "2000")

        # Threshold input
        threshold_frame = ttk.Frame(main_frame)
        threshold_frame.pack(pady=5, fill=tk.X)
        ttk.Label(threshold_frame, text="Threshold (Range 0.00 - 1.00)").pack(side=tk.LEFT)
        self.threshold_entry = ttk.Entry(threshold_frame)
        self.threshold_entry.pack(side=tk.LEFT, padx=5)
        self.threshold_entry.insert(0, "0.45")

        # Measurement input fields
        input_frame = ttk.LabelFrame(main_frame, text="Enter measurements:", padding=10)
        input_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.entries = {}
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            frame = ttk.Frame(input_frame)
            frame.pack(pady=2, fill=tk.X)
            ttk.Label(frame, text=f"Input ({i},{j})", width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[f"{i}{j}"] = entry

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Example", command=self.generate_example).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Predict", command=self.predict).pack(side=tk.RIGHT, padx=5)

        # Result display
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=5)
        self.result_label = ttk.Label(result_frame, text="", font=('Arial', 12, 'bold'), foreground='red')
        self.result_label.pack()
        
    def generate_example(self):
        """Insert example values based on a randomly chosen logic gate"""
        max_intensity = float(self.max_intensity_entry.get() or 2000)
        try:
            threshold = float(self.threshold_entry.get())
        except ValueError:
            threshold = 0.45

        gate_name = random.choice(list(logic_gates.keys()))
        gate_values = logic_gates[gate_name]['values']

        for (i, j), val in zip([(0, 0), (0, 1), (1, 0), (1, 1)], gate_values):
            key = f"{i}{j}"
            self.entries[key].delete(0, tk.END)
            if val == 1:
                value = round(random.uniform(threshold + 0.05, 1.0) * max_intensity)
            else:
                value = round(random.uniform(0.0, max(0.01, threshold - 0.05)) * max_intensity)
            self.entries[key].insert(0, str(value))

        self.result_label.config(text="")

    def clear_inputs(self):
        """Clear measurement inputs and result label only"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.result_label.config(text="")
        
    def predict(self):
        """Normalize input, apply threshold, and classify logic gate"""
        try:
            max_intensity = float(self.max_intensity_entry.get())
            if max_intensity <= 0:
                raise ValueError("Maximum intensity must be positive")

            threshold = float(self.threshold_entry.get() or 0.45)

            input_data = {
                '00': float(self.entries['00'].get()),
                '01': float(self.entries['01'].get()),
                '10': float(self.entries['10'].get()),
                '11': float(self.entries['11'].get())
            }

            input_df = pd.DataFrame([input_data])
            input_normalized = input_df / max_intensity
            input_thresholded = input_normalized.map(lambda x: 1 if x > threshold else 0)

            prediction = clf.predict(input_thresholded)[0]
            self.result_label.config(text=f"Predicted Gate: {prediction}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception:
            messagebox.showerror("Error", "An unexpected error occurred during prediction.")
     
    def show_about(self):  # <-- Paste this at the end of the LogicGateApp class
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("500x400")

        about_text = """\
          
        Supported Logic Gates and Outputs:
        ----------------------------------
        YES1  [0, 0, 1, 1]
        YES2  [0, 1, 0, 1]
        NOT1  [1, 1, 0, 0]
        NOT2  [1, 0, 1, 0]
        INH1  [0, 1, 0, 0]
        INH2  [0, 0, 1, 0]
        IMP1  [1, 0, 1, 1]
        IMP2  [1, 1, 0, 1]
        OR    [0, 1, 1, 1]
        NOR   [1, 0, 0, 0]
        PASS1 [1, 1, 1, 1]
        PASS0 [0, 0, 0, 0]
        XOR   [0, 1, 1, 0]
        XNOR  [1, 0, 0, 1]
        AND   [0, 0, 0, 1]
        NAND  [1, 1, 1, 0]

        Usage:
        ---------------
        Enter four intensity values corresponding to the 
        binary inputs (00, 01, 10, 11), specify the 
        maximum intensity and threshold if needed, and 
        click 'Predict' to classify the logic gate.
        """

        text_widget = tk.Text(about_window, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.insert(tk.END, about_text)
        text_widget.config(state='disabled')
        text_widget.pack(expand=True, fill='both', padx=10, pady=10)
# ------------------ Launch Application ------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x350")
    root.resizable(True, True)
    app = LogicGateApp(root)
    root.mainloop()


# In[ ]:




