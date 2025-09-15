import numpy as np
import pandas as pd

# Generate 10 values mirrored around the mean (32 µm), evenly spaced
mean_value = 32
num_values = 9
range_values = np.linspace(28, 36, num_values)

# Compute normal distribution values with mean=32 and sigma=1
sigma = 1
normal_values = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((range_values - mean_value) / sigma) ** 2)

# Normalize the values so that their sum is 1
normalized_values = normal_values / np.sum(normal_values)
print(range_values)
print(100*normalized_values)




