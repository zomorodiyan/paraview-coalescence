import pandas as pd
import matplotlib.pyplot as plt

# Variable setting
#variable = "viscosity"
variable = "density"

# Load the CSV file
file_path = f"data/lengths_32.5_{variable}.csv"
df = pd.read_csv(file_path)

# Convert 'Time' column to numeric
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

# Convert other columns to numeric, handling 'NA' values
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Define line styles and markers
line_styles = ['-', '--']  # Consistent line styles
markers = ['o', 's']  # One marker for all Length_x, another for Length_y

# List of density suffixes
densities = [f"0.25{variable}", f"0.5{variable}", "1", f"2{variable}", f"4{variable}"]
labels = [f"0.25x{variable}", f"0.5x{variable}", f"1x{variable}", f"2x{variable}", f"4x{variable}"]

# Generate unique colors for each density
cmap = plt.cm.get_cmap("Set1", len(densities))  # Use tab10 for distinct colors
colors = {density: cmap(i) for i, density in enumerate(densities)}

# Plot the data
plt.figure(figsize=(10, 6))
for i, density in enumerate(densities):
    x_col = f"Length_x_copper32.5um{density}"
    y_col = f"Length_y_copper32.5um{density}"
    if x_col in df.columns and y_col in df.columns:
        # Plot Length_x with a specific marker and line style
        plt.plot(df['Time'], df[x_col], marker=markers[0],
                 linestyle=line_styles[0], color=colors[density],
                 label=f"{labels[i]} (lx)")
        # Plot Length_y with a different marker and line style
        plt.plot(df['Time'], df[y_col], marker=markers[1],
                 linestyle=line_styles[1], color=colors[density],
                 label=f"{labels[i]} (ly)")

plt.xlabel('Time (s)', fontsize=14)
plt.ylabel('Length', fontsize=14)
plt.title(f'Length vs Time for various {variable}', fontsize=16)
#plt.legend(fontsize=13, ncol=2, loc="center left")
plt.legend(fontsize=13, ncol=2, loc="upper right")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()
plt.show()

