import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
length="10"
length_=float(length)
df = pd.read_csv("./data/lengths_"+length+".csv").replace("NA", float("nan"))

# Define colors for different metals
metal_colors = {
    "copper": "#b87333", "aluminum": "#428050", "iron": "#0F0F0F",
    "silver": "#708090", "nickel": "#C7A642", "titanium": "#6A0DAD",
    "cobalt": "#1047AB"
}

# Apply time filters
df_filtered = df.copy()
df_filtered.loc[df_filtered["Time"] > length_*0.9e-5, ["Length_x_aluminum"+length+"um2M", "Length_y_aluminum"+length+"um2M"]] = np.nan
df_filtered.loc[df_filtered["Time"] > length_*0.9e-5, ["Length_x_titanium"+length+"um2M", "Length_y_titanium"+length+"um2M"]] = np.nan

# Plot settings
ms, lw, alf = 5, 1.5, 0.8  # Marker size, line width, alpha

# Create figure
plt.figure(figsize=(10, 6))

# List of materials to plot
materials = ["copper", "aluminum", "iron", "silver", "nickel", "titanium", "cobalt"]

# Loop through materials to plot both Length_x and Length_y
for mat in materials:
    condition = mat == "nickel"
    mat_key = f"{mat}"+length+"um2M"
    plt.plot(df_filtered["Time"], df_filtered[f"Length_x_{mat_key}"], marker="o", linestyle="-",
             color=metal_colors[mat], label=f"{mat.capitalize()}_x", alpha=alf,
             markersize=ms + (4 if condition else 0), linewidth=lw + (1 if condition else 0))
    plt.plot(df_filtered["Time"], df_filtered[f"Length_y_{mat_key}"], marker="s", linestyle="--",
             color=metal_colors[mat], label=f"{mat.capitalize()}_y", alpha=alf,
             markersize=ms + (4 if condition else 0), linewidth=lw + (1 if condition else 0))

# Formatting
plt.xlabel("Time")
plt.ylabel("Length")
#plt.title("Length_x (2*neck_radius) and Length_y vs Time")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.grid(True)  # Enable grid for better readability
plt.tight_layout(rect=[0, 0, 1.0, 1.0])  # Adjust layout

# Show plot
plt.show()
