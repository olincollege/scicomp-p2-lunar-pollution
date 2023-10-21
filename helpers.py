import numpy as np

# Acceleration due to gravity at the moon (m/s^2)
G_MOON = 1.625
# Timescale for loss by photodestruction (s)
PHOTOLOSS_TIMESCALE = 6.7e4
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
# Parameters for surface temperature calculation
T_0 = 151
T_1 = 161.7
N = 0.59

def sample_spherical():
    """
    Generate a random spherical coordinate in 3-dimensional space

    Returns:
        phi: Polar spherical coordinate between 0 and pi
        beta: Azimuthal spherical coordinate between 0 and 2*pi
    """
    # Generate a 3-dimnensional vector and normalize
    vec = np.random.randn(3)
    vec /= np.linalg.norm(vec, axis=0)
    # Assign Cartesian coordinates from vector
    x, y, z = vec
    # Convert to spherical coordinates
    phi = np.arccos(y)
    beta = (x/abs(x)) * np.arccos(z / np.sqrt(np.square(z) + np.square(x)))
    return phi, beta

def wrap(angle, lims = (0, 2*np.pi)):
    """
    Wrap around values that go beyond limits

    Args:
        angle: Float input angle to check (radians)
        lims: Tuple with 2 values for lower and upper limit, default 0 and 2*pi

    Return:
        Float angle, wrapped within limits
    """
    # Wrap around positive
    angle = np.where(angle < lims[0], angle + (lims[1] - lims[0]), angle)
    # Wrap around negative
    angle = np.where(angle > lims[1], angle - (lims[1] - lims[0]), angle)
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
        

def get_delta(v_initial, launch_angle):
    """
    Get angle between initial and final position

    Currently assumed to be a fixed arc length calculated from initial velocity

    Returns: Float with angle in radians
    """
    d_water = distance_per_hop(v_initial, launch_angle)
    return d_water / R_MOON

def get_temp(phi, model_option):
    """
    Calculate surface temperature at given latitude based on thermal model

    Arg:
        phi: Polar spherical coordinate between 0 and pi
    
    Return:
        Float of temperature in Kelvin
    """
    if model_option == "1993":
        return 500
    return T_0 + T_1 * np.power(np.cos(phi - np.pi/2), N)

def get_angle(model_option):
    """
    Generate a random emergent angle between zero and pi/2

    Returns:
        Float of angle in radians
    """
    if model_option == "1993":
        return np.pi / 4
    return np.arccos(np.random.uniform(0, 1))