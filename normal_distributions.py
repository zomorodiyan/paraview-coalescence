import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd

# Constants
mean_r = 32  # micrometers
std_devs = [1, 2, 3, 4]
x = np.linspace(0.5*mean_r, 1.5*mean_r, 1000)
colors = plt.cm.tab10.colors

# Storage for results
results = []

# Plot setup
plt.figure(figsize=(12, 7))

for idx, std in enumerate(std_devs):
    y = norm.pdf(x, mean_r, std)
    color = colors[idx % len(colors)]

    # Plot the distribution
    plt.plot(x, y, label=f'σ={std}', color=color)

    # Calculate 10% lower and upper percentiles
    lower_bound = norm.ppf(0.10, mean_r, std)
    upper_bound = norm.ppf(0.90, mean_r, std)
    lower_y = norm.pdf(lower_bound, mean_r, std)
    upper_y = norm.pdf(upper_bound, mean_r, std)

    # Vertical lines for 10% tails
    plt.vlines(lower_bound, 0, lower_y, colors=color, linestyles='--')
    plt.vlines(upper_bound, 0, upper_y, colors=color, linestyles='--')

    # Annotate the cutoff points
    plt.text(lower_bound - 0.08, lower_y + 0.01, f'{lower_bound:.2f}', color=color,
             ha='center', va='bottom', fontsize=12, rotation=90)
    plt.text(upper_bound + 0.08, upper_y + 0.01, f'{upper_bound:.2f}', color=color,
             ha='center', va='bottom', fontsize=12, rotation=90)

    results.append({
        'Std Dev (σ)': std,
        'Lower 10% r value': lower_bound,
        'Upper 10% r value': upper_bound
    })

plt.title('Normal Distributions with 10% Tail Cutoff Points Labeled')
plt.xlabel('r (µm)')
plt.ylabel('Probability Density')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Create dataframe and show to user
results_df = pd.DataFrame(results)
display_dataframe_to_user(name="Tail Boundaries with Labels", dataframe=results_df)

