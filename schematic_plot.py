import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Function to generate sphere coordinates
def generate_sphere(center, radius, num_points=30):
    u = np.linspace(0, 2 * np.pi, num_points)
    v = np.linspace(0, np.pi, num_points)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
    return x, y, z

# Define cube dimensions
cube_size = 30  # in micrometers
half_size = cube_size / 2

# Define cube vertices
cube_vertices = np.array([
    [-half_size, -half_size, -half_size], [half_size, -half_size, -half_size],
    [half_size, half_size, -half_size], [-half_size, half_size, -half_size],
    [-half_size, -half_size, half_size], [half_size, -half_size, half_size],
    [half_size, half_size, half_size], [-half_size, half_size, half_size]
])

# Define first set of cube faces (-X, -Z, +Y)
first_faces = [
    [cube_vertices[j] for j in [0, 3, 7, 4]],  # -X face
    [cube_vertices[j] for j in [0, 1, 2, 3]],  # -Z face
    [cube_vertices[j] for j in [2, 3, 7, 6]]   # +Y face
]

# Define second set of cube faces (+X, +Z, -Y)
second_faces = [
    [cube_vertices[j] for j in [1, 2, 6, 5]],  # +X face
    [cube_vertices[j] for j in [4, 5, 6, 7]],  # +Z face
    [cube_vertices[j] for j in [0, 1, 5, 4]]   # -Y face
]

# Define sphere parameters
radius = 5  # in micrometers
center1 = [-5, 0, 0]  # First sphere center in micrometers
center2 = [5, 0, 0]   # Second sphere center in micrometers

# Generate sphere coordinates
x1, y1, z1 = generate_sphere(center1, radius)
x2, y2, z2 = generate_sphere(center2, radius)

# Create figure and 3D axis
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot first set of cube faces (-X, -Z, +Y)
ax.add_collection3d(Poly3DCollection(first_faces, facecolors='gray', linewidths=0, edgecolors=None, alpha=0.2))

# Plot solid surface spheres
ax.plot_surface(x1, y1, z1, color='darkgray', alpha=0.4)
ax.plot_surface(x2, y2, z2, color='darkgray', alpha=0.6)

# Plot second set of cube faces (+X, +Z, -Y)
ax.add_collection3d(Poly3DCollection(second_faces, facecolors='cyan', linewidths=1, edgecolors='k', alpha=0.05))

# Draw an annotation to indicate the radius R0
ax.text(center1[0], center1[1] - radius - 3, center1[2], r'$R_0$', color='black', fontsize=12)
ax.plot([center1[0], center1[0]], [center1[1], center1[1] - radius], [center1[2], center1[2]], 'k--', linewidth=1)

# Draw arrows for X and Z axes
ax.quiver(-12, 0, 0, 24, 0, 0, color='k', arrow_length_ratio=0.1)
ax.quiver(0, 0, -7, 0, 0, 14, color='k', arrow_length_ratio=0.1)

# Label axes
ax.text(13, 0, 0, 'X', color='black', fontsize=12)
ax.text(0, 0, 8, 'Y', color='black', fontsize=12)

# Draw two separate arrows for a two-way line on the -Y surface at z = -10um
ax.quiver(-5, -half_size, -10, -10, 0, 0, color='k', arrow_length_ratio=0.05)
ax.quiver(5, -half_size, -10, 10, 0, 0, color='k', arrow_length_ratio=0.05)

# Annotate the width in the middle of the line
ax.text(0, -half_size, -10.5, '141 cells wide', color='black', fontsize=12, ha='center')

# Adjust aspect ratio to avoid distortion
ax.set_box_aspect([1,1,1])

# Disable grid to prevent it from appearing over the spheres
ax.grid(False)
ax.set_axisbelow(True)

# Set limits and labels
ax.set_xlim([-half_size, half_size])
ax.set_ylim([-half_size, half_size])
ax.set_zlim([-half_size, half_size])
ax.set_xlabel('X (µm)')
ax.set_ylabel('Z (µm)')
ax.set_zlabel('Y (µm)')
#ax.set_title('Coalescence of two 10$\mu$m spheres at $t = 0$')

# Annotate boundary conditions on front surfaces (+X, -Y, +Z)
ax.text(half_size - 2, -3, -4, 'Atmosphere', color='black', fontsize=12)
ax.text(0, -half_size - 2, -2, 'Atmosphere', color='black', fontsize=12)
ax.text(0, -4, half_size + 2, 'Atmosphere', color='black', fontsize=12)

# Save the figure
import os
os.makedirs('plots', exist_ok=True)
plt.savefig('plots/domain.png', dpi=300, bbox_inches='tight')

# Show plot
plt.show()
