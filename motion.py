import numpy as np
import helpers as h

class Particle:
    def __init__(self, phi, beta, model_option):
        self.phi = phi
        self.beta = beta
        self.model_option = model_option
        self.temp = h.get_temp(self.phi, model_option)
        self.mass = h.MASS_WATER

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
        if self.model_option == "1993":
            if self.phi > (np.pi / 2):
                return (np.pi - self.phi) < h.PHI_POLE
            return self.phi < h.PHI_POLE
        
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
            self.beta = h.wrap(self.beta + epsilon)
        else:
            self.beta = h.wrap(self.beta - epsilon)

    def move(self):
        """
        Move a particle to its new position

        Currently assumes many things - water molecule, ballistic trajectory,
        constant surface temperature.
        """
        delta = h.get_delta(self.velocity, self.launch_angle)
        psi = np.random.uniform(0, 2*np.pi)
        phi_old = self.phi
        self.update_phi(delta, psi)
        self.update_beta(delta, phi_old, psi)

    def update_conditions(self):
        self.temp = h.get_temp(self.phi, self.model_option)
        self.velocity = h.velocity_rms(self.mass, self.temp)
        self.launch_angle = h.get_angle(self.model_option)
        self.hop_time = h.time_per_hop(self.velocity, self.launch_angle)
