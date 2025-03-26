import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("./plots", exist_ok=True)

lengths = np.linspace(5, 100, 100)
file_lengths = [5, 10, 32.5, 55, 77.5, 100]
materials = ["iron", "copper", "aluminum", "silver", "nickel", "titanium", "cobalt"]
metal_colors = {
    "iron": "#0F0F0F", "copper": "#b87333", "aluminum": "#428050",
    "silver": "#708090", "nickel": "#C7A642", "titanium": "#6A0DAD", "cobalt": "#1047AB"
}
material_properties = {
    "copper": (8.022215732, 1.3495724), "aluminum": (2.386318826, 1.0296111),
    "iron": (7.01447878, 1.6458166), "silver": (9.316033813, 0.92283334),
    "nickel": (7.87288543, 1.8046309), "titanium": (4.13557492, 1.5101234),
    "cobalt": (7.723223, 1.7738322),
}

intersection_times = {m: {l: np.nan for l in file_lengths} for m in materials}
x_condition_times = {m: {l: np.nan for l in file_lengths} for m in materials}

for length in file_lengths:
    try:
        df = pd.read_csv(f"./data/lengths_{length}.csv").replace("NA", float("nan"))
        target_x = length * 1e-6 * (2 ** (2 / 3))

        for mat in materials:
            x_col, y_col = f"Length_x_{mat}{length}um2M", f"Length_y_{mat}{length}um2M"
            if x_col in df and y_col in df:
                diff = df[x_col] - df[y_col]
                idx = np.where(np.diff(np.sign(diff)))[0]
                if idx.size:
                    t1, t2 = df.iloc[idx[0]]["Time"], df.iloc[idx[0] + 1]["Time"]
                    x1, x2, y1, y2 = df.iloc[idx[0]][x_col], df.iloc[idx[0] + 1][x_col], df.iloc[idx[0]][y_col], df.iloc[idx[0] + 1][y_col]
                    intersection_times[mat][length] = t1 + (t2 - t1) * abs(x1 - y1) / abs((x1 - y1) - (x2 - y2))

                idx_x = np.where(np.diff(np.sign(df[x_col] - target_x)))[0]
                if idx_x.size:
                    t1, t2, x1, x2 = df.iloc[idx_x[0]]["Time"], df.iloc[idx_x[0] + 1]["Time"], df.iloc[idx_x[0]][x_col], df.iloc[idx_x[0] + 1][x_col]
                    x_condition_times[mat][length] = t1 + (t2 - t1) * abs(x1 - target_x) / abs(x1 - x2)
    except FileNotFoundError:
        continue

theoretical_values = {m: 2**(2/3) * (lengths / 2 / 1e6)**2 * ((1000 * rho) / (sigma * (lengths / 2 / 1e6)))**0.5
                      for m, (rho, sigma) in material_properties.items()}

base_marker_size = 60
marker_sizes = {m: base_marker_size * 1.8 if m == "nickel" else base_marker_size for m in materials}
line_lengths = {m: 3 if m != "nickel" else 4.5 for m in materials}

plt.figure(figsize=(8, 6))
for mat in materials:
    times = [intersection_times[mat][l] for l in file_lengths]
    plt.scatter(file_lengths, times, color=metal_colors[mat], s=marker_sizes[mat], label=mat.capitalize())
    for i, length in enumerate(file_lengths):
        plt.hlines(times[i], length - line_lengths[mat], length + line_lengths[mat], color=metal_colors[mat], alpha=0.8, linewidth=1.5)
plt.xlabel("R0: Starting Spheres Radius (μm)")
plt.ylabel("Coalescence Time")
plt.title("Coalescence Time Based on Length_x = Length_y")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.savefig("./plots/coalescence_intersection.png")
plt.close()

plt.figure(figsize=(8, 6))
for mat in materials:
    times = [x_condition_times[mat][l] for l in file_lengths]
    plt.scatter(file_lengths, times, color=metal_colors[mat], s=marker_sizes[mat], label=f"Simulation {mat.capitalize()}")
    for i, length in enumerate(file_lengths):
        plt.hlines(times[i], length - line_lengths[mat], length + line_lengths[mat], color=metal_colors[mat], alpha=0.8, linewidth=1.5)
for mat, values in theoretical_values.items():
    plt.plot(lengths, values, linestyle="dashed", color=metal_colors[mat], label=f"Theoretical {mat.capitalize()}")
plt.xlabel("R0: Starting Spheres Radius (μm)")
plt.ylabel("Coalescence Time")
plt.title("Coalescence Time with Theoretical Model")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.savefig("./plots/coalescence_theoretical.png")
plt.close()
