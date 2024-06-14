import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#%%
def plot_experiments(file_path, save_path, nrepetitions):
    
    with open(file_path) as file:
        lines = file.readlines()
        speed_values = get_values(lines[7])
        selectivity_values = get_values(lines[8])
        min_temp_values = get_values(lines[10])
        max_temp_values = get_values(lines[9])
        df_values = lines[23:2023]
        # Split each string into a list of integers, converting empty strings to 0
        data = [
[int(x.strip()) if x.strip() else None for x in s.replace('"', '').split(',')[1:]]
    for s in df_values
]
        # Create a DataFrame from the list of lists
        df = pd.DataFrame(data)
        
        for i in range(0, int(df.shape[1]/3), nrepetitions):
            
            speed = speed_values[i]
            selectivity = selectivity_values[i]
            min_temp = min_temp_values[i]
            max_temp = max_temp_values[i]
            
            subdf = df.iloc[:, 0+3*i : 60+3*i]
            subdf = subdf.drop(list(range(0+3*i,60+3*i,3)), axis=1)
            
            # Find columns where the first value is 2000
            columns_1 = []
            for col in subdf.columns:
                if subdf[col].iloc[0] == 2000:
                    columns_1.append(col)
            
            min_1 = subdf[columns_1].min(axis=1)
            mean_1 = subdf[columns_1].mean(axis=1)
            max_1 = subdf[columns_1].max(axis=1)

            columns_2 = [col for col in subdf.columns if col not in columns_1]
            min_2 = subdf[columns_2].min(axis=1)
            mean_2 = subdf[columns_2].mean(axis=1)
            max_2 = subdf[columns_2].max(axis=1)
            
            # Plotting
            plt.figure(figsize=(12, 6))
        
            # Plot mean line
            plt.plot(df.index, mean_1, label='Mean', color='yellow')
            plt.plot(df.index, mean_2, label='Mean', color='red')
        
            # Plot shaded area between min and max
            plt.fill_between(df.index, min_1, max_1, color='yellow', alpha=0.5, label='Min-Max Range')
            plt.fill_between(df.index, min_2, max_2, color='red', alpha=0.3, label='Min-Max Range')
                    
            # Add labels and title
            plt.xlabel('Step')
            plt.ylabel('Number of turtles')
            plt.title(f"""Experiment for turtle-speed={speed}, 
                      mating-selectivity={selectivity}, 
                      min-temperature={min_temp}, 
                      max-temperature={max_temp}
                      """)
            plt.legend()
        
            # Show and save plot
            plt.tight_layout()
            file_name = f"sp{speed}_sel{selectivity}_t{max_temp}.png"
            plt.savefig(os.path.join(save_path, file_name))
            plt.show()
        

          
def get_values(line):
    elements = line.split(',')
    
    # Function to check if a string is a valid integer (including negatives)
    def is_valid_integer(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    
    # Skip the first element and filter out empty strings and non-numeric strings
    filtered_elements = []
    for x in elements[1:]:
        x = x.strip().strip('"')
        if is_valid_integer(x):
            filtered_elements.append(int(x))
    
    return filtered_elements 


#%%
script_dir = os.path.dirname(os.path.abspath(__file__))
files = [
    "Echo temp_range_-50-50_v2-spreadsheet.csv",
    "Echo temp_range_-30-30_v2-spreadsheet.csv",
    "Echo temp_range_-10-10_v2-spreadsheet.csv"
    ]
save_path = os.path.join(script_dir, "plots")
for filename in files:
    file_path = os.path.join(script_dir, filename)
    plot_experiments(file_path, save_path, 20)