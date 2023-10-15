# # To do:
# 1) Implement "hopping" by distance moved based on constant speed
# 2) Figure out how distance can be moved on the "surface", random direction
# 3) Include time into hopping
# 4) With model of many molecules hopping, implement capture
# 5) Implement photodissociation
# 6) (Stretch) implement for different amu's - will involve updating movement function

import matplotlib.pyplot as plt
import motion
import numpy as np

def coord_converter(phi, beta):
    # Spherical coordinates to Cartesian coordinates conversion
    x = np.sin(phi) * np.sin(beta)
    y = np.cos(phi)
    z = np.sin(phi) * np.cos(beta)
    return (x, y, z)

def plot_sphere(ax):
    # Create a meshgrid of phi and beta values
    # (phi is 'lattitude', beta is 'longitude')
    # Figure out - what does j mean?? Without j, sphere doesn't display
    phi, beta = np.mgrid[0.0:2.0*np.pi:100j, 0.0:np.pi:50j]

    (x, y, z) = coord_converter(beta, phi)

    # Plot the 3D sphere in blue color
    # (Note: Reducing size of sphere does not work)
    ax.plot_surface(x, y, z, color='#EEEEEE', alpha=0.5, linewidth=0)

def plot_points(ax, phi_start, beta_start, phi_end, beta_end, is_captured):
    ax.scatter(*coord_converter(phi_start, beta_start), color='r', s = 10)

    if is_captured:
        ax.scatter(*coord_converter(phi_end, beta_end), color='b', s = 10)
    else:
        ax.scatter(*coord_converter(phi_end, beta_end), color='g', s = 10)

def finish(ax):
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Sphere with a Colored Point')

    # Show the plot
    plt.show()

phi_start = np.pi / 2
beta_start = 0
(phi_end, beta_end) = motion.move(phi_start, beta_start)
is_captured = True # Dummy just as a placeholder for plotting

# Create a 3D figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

plot_sphere(ax)
plot_points(ax, phi_start, beta_start, phi_end, beta_end, is_captured)
finish(ax)