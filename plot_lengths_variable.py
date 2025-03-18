import pandas as pd
import matplotlib.pyplot as plt

variable = "density"
#variable = "viscosity"

# Load the CSV file
file_path = "data/lengths_32.5_"+variable+".csv"

df = pd.read_csv(file_path)

# Convert 'Time' column to numeric
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

# Convert other columns to numeric, handling 'NA' values
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Define line styles and markers
line_styles = ['-', '--', '-.', ':']  # Different line styles
markers = ['o', 's', 'D', '^', 'v']  # Different markers
colors = {}  # Dictionary to store colors for each density

# List of density suffixes
densities = [f"0.25{variable}", f"0.5{variable}", "1", f"2{variable}", f"4{variable}"]

# Generate unique colors for each density
cmap = plt.cm.get_cmap("tab10", len(densities))  # Use tab10 colormap for distinct colors
for i, density in enumerate(densities):
    colors[density] = cmap(i)  # Assign unique color per density

# Plot the data
plt.figure(figsize=(10, 6))
for i, density in enumerate(densities):
    x_col = f"Length_x_copper32.5um{density}"
    y_col = f"Length_y_copper32.5um{density}"
    if x_col in df.columns and y_col in df.columns:
        plt.plot(df['Time'], df[x_col], marker=markers[i % len(markers)], linestyle=line_styles[0], color=colors[density], label=f"{density} (x)")
        plt.plot(df['Time'], df[y_col], marker=markers[i % len(markers)], linestyle=line_styles[1], color=colors[density], label=f"{density} (y)")

plt.xlabel('Time (s)')
plt.ylabel('Length')
plt.title('Length vs Time for various '+variable)
plt.legend()
plt.grid()
plt.show()
