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

    circle_beta = np.linspace(0, 2*np.pi, 100)
    circle1_phi = np.full(100, motion.PHI_POLE)
    circle2_phi = np.full(100, np.pi - motion.PHI_POLE)

    ax.plot(*coord_converter(circle1_phi, circle_beta))
    ax.plot(*coord_converter(circle2_phi, circle_beta))

def plot_points(ax, phi, beta, color='r'):
    ax.scatter(*coord_converter(phi, beta), color=color, s = 10)

def plot_finish(ax, title):
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Show the plot
    plt.show()

def plot_option_journey(ax, phi, beta):
    v_initial = motion.velocity_rms(motion.MASS_WATER, motion.T_SURFACE)
    t_hop = motion.time_per_hop(v_initial, motion.ANGLE)

    for i in range(1000):
        plot_points(ax, phi, beta)
        ax.text(*coord_converter(phi, beta), i, fontsize=6)
        (phi, beta) = motion.move(phi, beta)
        if motion.is_photodestroy(t_hop):
            print(i)
            plot_points(ax, phi, beta, color='g')
            break

        if motion.is_captured(phi):
            print(i)
            print("Captured!")
            plot_points(ax, phi, beta, color='b')
            break

def plot_option_results(ax):
    # Randomly uniformly distribute a bunch of particles on sphere
    # Keep looping till they are captured or destroyed
    # Maybe implement it one-by-one first
    # And then try doing it in numpy arrays
    pass

# # Plotting journey of single molecule for visualizing
# # Maybe include as a "menu" select item when plotting?
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')

# plot_sphere(ax)
# plot_option_journey(ax, phi = np.pi / 2, beta = 0)
# plot_finish(ax, "Journey of single molecule")