# # To do:
# 1) Implement "hopping" by distance moved based on constant speed
# 2) Figure out how distance can be moved on the "surface", random direction
# 3) Include time into hopping
# 4) With model of many molecules hopping, implement capture
# 5) Implement photodissociation
# 6) (Stretch) implement for different amu's - will involve updating movement function

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def coord_converter(beta, phi):
    # Spherical coordinates to Cartesian coordinates conversion
    x = np.sin(beta) * np.sin(phi)
    y = np.sin(beta) * np.cos(phi)
    z = np.cos(beta)
    return (x, y, z)

# Create a meshgrid of phi and theta values
# (phi is 'longitude', theta is 'latitude')
# Figure out - what does j mean?? Without j, sphere doesn't display
phi, theta = np.mgrid[0.0:2.0*np.pi:100j, 0.0:np.pi:50j]

(x, y, z) = coord_converter(theta, phi)

# Create a 3D figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D sphere in blue color
# (Note: Reducing size of sphere does not work)
ax.plot_surface(x, y, z, color='#EEEEEE', alpha=0.5, linewidth=0)

b = np.pi - 1
p = 0
ax.scatter(*coord_converter(b, p), color='r', s = 10)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Sphere with a Colored Point')

# Show the plot
plt.show()
