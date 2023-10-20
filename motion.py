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

def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    x, y, z = vec
    phi = np.arccos(y)
    beta = (x/abs(x)) * np.arccos(z / np.sqrt(np.square(z) + np.square(x)))
    return phi, beta

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

def get_temp(phi):
    return T_0 + T_1 * np.power(np.cos(phi - np.pi/2), N)

def get_angle():
    return np.arccos(np.random.uniform(0, 1))

class Particle:
    def __init__(self, id):
        self.phi, self.beta = sample_spherical(1)
        self.temp = get_temp(self.phi)

        self.launch_angle = get_angle()
        self.velocity = velocity_rms(MASS_WATER, self.temp)

        self.hop_time = time_per_hop(self.velocity, self.launch_angle)
        self.delta = get_delta(self.velocity, self.launch_angle)
        self.id = id
    
    def is_photodestroy(self):
        """
        If a particle is photodestroyed for a certain hop time

        Uses time from time_per_hop, probability of destruction in given hop

        Return:
            Boolean of whether particle has been destroyed or not
        """
        prob = 1 - np.exp(-self.hop_time / PHOTOLOSS_TIMESCALE)
        return np.random.uniform(0, 1, size = prob.shape) < prob

    def is_captured(self):
        """
        Check if given particle has been captured at polar regions

        Probabilities of capture are binned as percentages.
        
        Return:
            Boolean whether particle is captured or not
        """
        # Convert to degrees and center on zero
        angle = abs(np.rad2deg(self.phi) - 90)
        if angle > 80:
            return np.random.uniform(0, 100) < 11
        elif angle > 70:
            return np.random.uniform(0, 100) < 4
        elif angle > 60:
            return np.random.uniform(0, 100) < 0.9
        elif angle > 50:
            return np.random.uniform(0,100) < 0.4
        else:
            return False

    def update_phi(self, delta, psi):
        """
        Update value of phi based on given parameters

        Args:
            delta: Angle between starting and final position (i.e. 'arc length')
            psi: Random angle between 0 and 2*pi for new direction
        """
        expression = (np.cos(self.phi) * np.cos(delta)) + (np.sin(self.phi) * np.sin(delta) * np.cos(psi))
        self.phi = np.arccos(expression)

    def update_beta(self, delta, phi_old, psi):
        """
        Update value of beta based on given parameters

        Args:
            delta: Angle between starting and final position (i.e. 'arc length')
            phi_old: Previous value of phi coordinate (polar angle)
            psi: Random angle between 0 and 2*pi for new direction
        """
        expression = (np.cos(delta) - (np.cos(self.phi) * np.cos(phi_old))) / (np.sin(self.phi) * np.sin(phi_old))
        epsilon = np.arccos(expression)
        if psi > np.pi:
            self.beta = wrap(self.beta + epsilon)
        else:
            self.beta = wrap(self.beta - epsilon)


    def move(self):
        """
        Move a particle to its new position

        Currently assumes many things - water molecule, ballistic trajectory,
        constant surface temperature.
        """
        delta = get_delta(self.velocity, self.launch_angle)
        psi = np.random.uniform(0, 2*np.pi)
        phi_old = self.phi
        self.update_phi(delta, psi)
        self.update_beta(delta, phi_old, psi)

    def update_conditions(self):
        self.temp = get_temp(self.phi)
        self.velocity = velocity_rms(MASS_WATER, self.temp)
        self.launch_angle = get_angle()
        self.hop_time = time_per_hop(self.velocity, self.launch_angle)
