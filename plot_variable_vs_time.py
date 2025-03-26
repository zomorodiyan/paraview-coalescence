import numpy as np
import matplotlib.pyplot as plt

# Given values
length = 32.5  # micrometers
copper_density, copper_sigma = 8.022215732, 1.3495724

# Convert length to meters
length_m = length / 2 / 1e6  # divide by 2 and convert to meters

# Define the analytical formula as a function of density
def theoretical_t_coalescence(rho):
    return 1.05 * 2**(2/3) * (length_m)**2 * ((1000 * rho) / (copper_sigma * length_m))**0.5

# --- First plot: Theoretical vs Simulation (Density) ---

# Generate density values between 0.25 * rho and 4 * rho
density_vals = np.linspace(0.25 * copper_density, 4 * copper_density, 300)
theoretical_vals = theoretical_t_coalescence(density_vals)

# Given data points
simulation_rho = np.array([
    0.25 * copper_density,
    0.5 * copper_density,
    1 * copper_density,
    2 * copper_density,
    4 * copper_density
])
simulation_t_density = np.array([
    0.45e-5,
    0.63e-5,
    0.88e-5,
    1.21e-5,
    1.68e-5
])

# Plotting first figure
plt.figure(figsize=(8, 6))
plt.plot(density_vals, theoretical_vals, linestyle='--', label='Theoretical')
plt.scatter(simulation_rho, simulation_t_density, color='red', s=60, label='Simulation Data')

plt.xlabel('Density (g/cm^3)')
plt.ylabel('t_coalescence (s)')
plt.title('Theoretical vs Simulation t_coalescence (Density Variation)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Second plot: Theoretical vs Simulation (Viscosity) ---

# Define copper viscosity (mu)
copper_mu = copper_sigma  # Assuming given sigma is viscosity in this context

# Theoretical value is constant
constant_theoretical_value = 0.85e-5

# Times of copper viscosity
mu_multipliers = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
experimental_mu = mu_multipliers * copper_mu
experimental_t_viscosity = np.array([
    0.94e-5,
    0.91e-5,
    0.87e-5,
    0.83e-5,
    0.82e-5
])

# Theoretical values (constant)
constant_vals = np.full_like(mu_multipliers, constant_theoretical_value)

# Plotting second figure
plt.figure(figsize=(8, 6))
plt.plot(mu_multipliers, constant_vals, linestyle='--', label='Theoretical')
plt.scatter(mu_multipliers, experimental_t_viscosity, color='green', s=60, label='Simulation Data')

plt.xlabel('Times Copper Viscosity')
plt.ylabel('t_coalescence (s)')
plt.title('Theoretical vs Simulation t_coalescence (Viscosity Variation)')
plt.xlim([0.2, 4.2])
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
