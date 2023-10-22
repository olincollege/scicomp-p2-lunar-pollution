"""
Contains the Particle agent used in this simulation
"""
import numpy as np
import helpers as h

class Particle:
    """
    A single particle

    Attributes:
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either from Butler's 1993 or 1997
        temp: Yemperature of molecule in Kelvin at surface
        mass: Mass of molecule in kg
        launch_angle: Emergent angle of particle (in radians)
        velocity: Emergent velocity of particle hop (in m/s)
        hop_time: Time taken for a given particle hop
        delta: Angle between start and final position (i.e. 'arc length')
    """
    def __init__(self, start_option, model_option):
        # Set initial coordinates (default 70 degrees south)
        self.phi = 70 * (np.pi / 180)
        self.beta = 0

        # If option is random, set initial coordinates as random
        if start_option == "random":
            self.phi, self.beta = h.sample_spherical()

        # Initialize other state attributes
        self.model_option = model_option
        self.temp = h.get_temp(self.phi, model_option)
        self.mass = h.MASS_WATER

        # Initialize motion attributes
        self.launch_angle = h.get_angle(model_option)
        self.velocity = h.velocity_rms(self.mass, self.temp)
        self.hop_time = h.time_per_hop(self.velocity, self.launch_angle)
        self.delta = h.get_delta(self.velocity, self.launch_angle)

    def is_photodestroy(self):
        """
        If a particle is photodestroyed for a certain hop time

        Uses time from time_per_hop, probability of destruction in given hop

        Return:
            Boolean of whether particle has been destroyed or not
        """
        prob = 1 - np.exp(-self.hop_time / h.PHOTOLOSS_TIMESCALE)
        return np.random.uniform(0, 1, size = prob.shape) < prob

    def is_captured(self):
        """
        Check if given particle has been captured at polar regions

        Probabilities of capture are binned as percentages.

        Return:
            Boolean whether particle is captured or not
        """
        # Check if lying within polar region if 1993 model
        if self.model_option == "1993":
            if self.phi > (np.pi / 2):
                return (np.pi - self.phi) < h.PHI_POLE
            return self.phi < h.PHI_POLE

        # Convert to degrees and center on zero
        angle = abs(np.rad2deg(self.phi) - 90)

        # Check probability of capture at different lattitude bins
        if angle > 80:
            return np.random.uniform(0, 100) < 11
        if angle > 70:
            return np.random.uniform(0, 100) < 4
        if angle > 60:
            return np.random.uniform(0, 100) < 0.9
        if angle > 50:
            return np.random.uniform(0,100) < 0.4
        return False

    def update_phi(self, delta, psi):
        """
        Update value of phi based on given parameters

        Args:
            delta: Angle between start and final position (i.e. 'arc length')
            psi: Random angle between 0 and 2*pi for new direction
        """
        expression = (np.cos(self.phi) * np.cos(delta)) + \
                        (np.sin(self.phi) * np.sin(delta) * np.cos(psi))
        self.phi = np.arccos(expression)

    def update_beta(self, delta, phi_old, psi):
        """
        Update value of beta based on given parameters

        Args:
            delta: Angle between start and final position (i.e. 'arc length')
            phi_old: Previous value of phi coordinate (polar angle)
            psi: Random angle between 0 and 2*pi for new direction
        """
        # Calculate epsilon
        expression = (np.cos(delta) - (np.cos(self.phi) * np.cos(phi_old))) / \
                        (np.sin(self.phi) * np.sin(phi_old))
        epsilon = np.arccos(expression)

        # Calculate beta value depending on magnitude of random angle psi
        if psi > np.pi:
            self.beta = h.wrap(self.beta + epsilon)
        else:
            self.beta = h.wrap(self.beta - epsilon)

    def move(self):
        """
        Move a particle to its new position
        """
        # Calculate new delta
        delta = h.get_delta(self.velocity, self.launch_angle)
        # Get new random direction of hop
        psi = np.random.uniform(0, 2*np.pi)
        # Store current value of phi
        phi_old = self.phi
        # Update phi and beta
        self.update_phi(delta, psi)
        self.update_beta(delta, phi_old, psi)

    def update_conditions(self):
        """
        Update the conditions for next hop
        """
        # Calculate new temperature from new position
        self.temp = h.get_temp(self.phi, self.model_option)
        # Calculate velocity from new temperature
        self.velocity = h.velocity_rms(self.mass, self.temp)
        # Generate new launcha angle (random or pi/4 depending on model)
        self.launch_angle = h.get_angle(self.model_option)
        # Calculate new hop time with new velocity, launc angle
        self.hop_time = h.time_per_hop(self.velocity, self.launch_angle)
