import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def calculate_sphere_centers(r1, r2, r3, r4):
    s1 = np.array([0, -r1, 0])
    s2 = np.array([0, r2, 0])

    y3 = ((r1 - r2) / (r1 + r2)) * r3
    x3 = np.sqrt((r1 + r3)**2 - (y3 + r1)**2)
    s3 = np.array([x3, y3, 0])

    y4 = ((r1 - r2) / (r1 + r2)) * r4
    x4 = ((r1 + r4)**2 - (y4 + r1)**2 - (r3 + r4)**2 + (y4 - y3)**2 + x3**2) / (2 * x3)
    z4 = np.sqrt((r1 + r4)**2 - x4**2 - (y4 + r1)**2)
    s4 = np.array([x4, y4, z4])

    return [s1, s2, s3, s4], [r1, r2, r3, r4]

def set_axes_equal(ax):
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])

def plot_spheres(ax, centers, radii, title):
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    for center, r in zip(centers, radii):
        x = center[0] + r * np.cos(u) * np.sin(v)
        y = center[1] + r * np.sin(u) * np.sin(v)
        z = center[2] + r * np.cos(v)
        ax.plot_surface(x, y, z, color=np.random.rand(3,), alpha=0.3)

    mean_center = np.mean(centers, axis=0)
    ax.scatter(mean_center[0], mean_center[1], mean_center[2], color='k', s=100, label='Mean Center')
    ax.legend()

    print("Sphere Centers:")
    for i, c in enumerate(centers, 1):
        print(f"Center {i}: {c}")
    print("\nArithmetic Mean Center:", mean_center)

    verts = [centers[0], centers[1], centers[2], centers[3]]
    hull = [[verts[0], verts[1], verts[2]],
            [verts[0], verts[1], verts[3]],
            [verts[0], verts[2], verts[3]],
            [verts[1], verts[2], verts[3]]]
    poly = Poly3DCollection(hull, alpha=0.1, facecolor='cyan', edgecolor='k')
    ax.add_collection3d(poly)

    edges = Line3DCollection(hull, colors='k', linewidths=1.5)
    ax.add_collection3d(edges)

    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    set_axes_equal(ax)

radii_set = (1, 1, 1, 1)

fig = plt.figure(figsize=(10, 8))
centers, radii = calculate_sphere_centers(*radii_set)
ax = fig.add_subplot(111, projection='3d')
plot_spheres(ax, centers, radii, f"Radii: {radii_set}")

plt.tight_layout()
plt.show()

