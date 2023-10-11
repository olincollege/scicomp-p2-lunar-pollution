import numpy as np

G_MOON = 1.625 # Change to moon g
PHOTOLOSS_TIMESCALE = 2 * np.power(10, 4) # See paper for exact value
R_MOON = 1738.1 * np.power(10, 3) # Radius of Moon in Meters
R_POLE = 300 * np.power(10, 3) # Radius of ice caps in meters (approximate)
BETA_POLE = R_POLE / R_MOON # This is very neat using radians
MOLAR_WATER = 18.015 * np.power(10.0, -3) # Molar mass of water
AVOGADRO = 6.0221e23
MASS_WATER = MOLAR_WATER / AVOGADRO
BOLTZMANN = 1.38 * np.power(10.0, -23)
T_SURFACE = 500

def velocity_rms(mass_molecule, t_surface):
    return np.sqrt((3 * BOLTZMANN * t_surface) / mass_molecule)

def time_per_hop(v_initial):
    return np.sqrt(2) * v_initial / G_MOON

def distance_per_hop(t_hop, v_initial):
    return 0.5 * v_initial * t_hop

def probs_photodestroy(t_hop):
    return 1 - np.exp(t_hop / PHOTOLOSS_TIMESCALE)

def is_captured(beta):
    if beta > (np.pi / 2):
        return (np.pi - beta) < BETA_POLE
    return beta < BETA_POLE

# print((3 * BOLTZMANN * T_SURFACE) / MASS_WATER)
# print(AVOGADRO)
v_water = velocity_rms(MASS_WATER, T_SURFACE)
t_water = time_per_hop(v_water)
print(t_water)

## Implement the functions below after completing version one of capture

# # But also this is binned every 10 degrees - figure out what's going on
# def surface_temp(phi):
#     return T_0 + (T_1 * (np.cos(phi - (np.pi / 2)) ** N_UNKNOWN))  

# # TODO - figure out
# def prob_capture():
#     pass




# ## Code Graveyard
# # Constants for iteration two 
# T_0 = 100 # Unclear what T_0 and T_1 mean for modelling
# T_1 = 100
# N_UNKNOWN = 0.25 # I can't figure out what this does
# Plots uniformly distributed points on sphere
# for theta in np.linspace(0, np.pi, 20):
#     for phi in np.linspace(0, 2*np.pi, 20):
#         # Plot the point on the sphere in red color
#         ax.scatter(*coord_converter(theta, phi), color='r', s = 10)