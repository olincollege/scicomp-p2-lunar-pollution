import numpy as np

# Acceleration due to gravity at the moon (m/s^2)
G_MOON = 1.625
# Timescale for loss by photodestruction (s)
PHOTOLOSS_TIMESCALE = 2e4
# Radius of moon (m)
R_MOON = 1738100
# Radius of ice caps (m)
R_POLE = 3e5
# Angle at which in polar regions (radians)
PHI_POLE = R_POLE / R_MOON
# Molar mass of water (kg/mol)
MOLAR_WATER = 18.015e-3
# Avagadro's number
AVOGADRO = 6.0221e23
# Mass of one molecule of water (kg)
MASS_WATER = MOLAR_WATER / AVOGADRO
# Boltzmann's constant
BOLTZMANN = 1.38e-23
# Temperature of moon's surface
T_SURFACE = 500
# Angle of particle launch
ANGLE = np.pi / 4


def wrap(angle, lims = (0, 2*np.pi)):
    """
    Helper function to wrap around values that go beyond limits

    Args:
        angle: Float input angle to check (radians)
        lims: Tuple with 2 values for lower and upper limit, default 0 and 2*pi

    Return:
        Float angle, wrapped within limits
    """
    # Wrap around positive
    if angle < lims[0]:
        return angle + (lims[1] - lims[0])
    # Wrap around negative
    if angle > lims[1]:
        return angle - (lims[1] - lims[0])
    # Angle is within range
    return angle


def velocity_rms(mass_molecule, t_surface):
    """
    Calculate emergent speed of molecule at given temperature

    Args:
        mass_molecule: Float mass of molecule (kg)
        t_surface: Integer value for surface temperature (K)

    Return:
        Float emergent speed of particle at surface (m/s)
    """
    return np.sqrt((3 * BOLTZMANN * t_surface) / mass_molecule)

def time_per_hop(v_initial, launch_angle):
    """
    Calculate time taken per hop of a particle

    Assumes ballistic motion for now with a constant gravitational field on the
    flat surface of the moon. Calculates time from initial speed, launch angle

    Args:
        v_initial: Float initial speed of molecule at surface (m/s)
        launch_angle: Float angle of launch (radians between 0 to pi)

    Return:
        Float with total time of travel (s)
    """
    return  2 * v_initial * np.sin(launch_angle) / G_MOON

def distance_per_hop(v_initial, launch_angle):
    """
    Calculate distance travelled per hop of a particle

    Assumes ballistic motion for now with a constant gravitational field on the
    flat surface of the moon. Uses time from time_per_hop with same initial
    speed and launch angle.

    Args:
        t_hop: Float total time taken for the hop (s)
        v_initial: Float initial speed of molecule at surface (m/s)
        launch_angle: Float angle of launch (radians between 0 to pi)

    Return:
        Float with total distance of travel (m)
    """
    t_hop = time_per_hop(v_initial, launch_angle)
    return v_initial * np.cos(launch_angle) * t_hop
        

def is_photodestroy(t_hop):
    """
    If a particle is photodestroyed for a certain hop time

    Uses time from time_per_hop, probability of destruction in given hop
    Arg:
        t_hop: Float time spent in the hop

    Return:
        Boolean of whether particle has been destroyed or not
    """
    prob = 1 - np.exp(-t_hop / PHOTOLOSS_TIMESCALE)
    return np.random.uniform(0, 1) < prob

def is_captured(phi):
    """
    Check if given particle has been captured at polar regions

    Currently assumes that if particle is in polar region, it has 100% chance
    of being captured.

    Arg:
        phi: Float polar angle indicating 'latitude' (radians)
    
    Return:
        Boolean whether particle is captured or not
    """
    if phi > (np.pi / 2):
        return (np.pi - phi) < PHI_POLE
    return phi < PHI_POLE

def update_phi(phi, delta, psi):
    """
    Update value of phi based on given parameters

    Args:
        phi: Current value of phi coordinate (polar angle)
        delta: Angle between starting and final position (i.e. 'arc length')
        psi: Random angle between 0 and 2*pi for new direction

    Return:
        New value of phi
    """
    expression = (np.cos(phi) * np.cos(delta)) + (np.sin(phi) * np.sin(delta) * np.cos(psi))
    return np.arccos(expression)

def update_beta(delta, phi_new, phi_old, beta, psi):
    """
    Update value of beta based on given parameters

    Args:
        delta: Angle between starting and final position (i.e. 'arc length')
        phi_new: Current (new) value of phi coordinate (polar angle)
        phi_old: Previous value of phi coordinate (polar angle)
        beta: Current value of beta coordinate (azimuthal angle)
        psi: Random angle between 0 and 2*pi for new direction

    Return:
        New value of beta
    """
    expression = (np.cos(delta) - (np.cos(phi_new) * np.cos(phi_old))) / (np.sin(phi_new) * np.sin(phi_old))
    epsilon = np.arccos(expression)
    if psi > np.pi:
        return wrap(beta + epsilon)
    return wrap(beta - epsilon)

def get_delta():
    """
    Get angle between initial and final position

    Currently assumed to be a fixed arc length calculated from initial velocity

    Returns: Float with angle in radians
    """
    v_water = velocity_rms(MASS_WATER, T_SURFACE)
    d_water = distance_per_hop(v_water, ANGLE)
    return d_water / R_MOON

def move(phi, beta):
    """
    Move a particle to its new position

    Currently assumes many things - water molecule, ballistic trajectory,
    constant surface temperature.

    Args:
        phi: Float current 'lattitude' polar spherical coordinate
        beta: Float current 'longitude' azimuthal spherical coordinate

    Returns:
        Tuple with new phi and beta values as floats (radians)
    """
    delta = get_delta()
    psi = np.random.uniform(0, 2*np.pi)
    phi_new = update_phi(phi, delta, psi)
    beta_new = update_beta(delta, phi_new, phi, beta, psi)
    return(phi_new, beta_new)


# Make movement function
# def move(beta_current, phi_current, distance):
#     relative_distance = distance/R_MOON
#     # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA HOW DO I DO THIS
#     return (beta_new, phi_new)










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
