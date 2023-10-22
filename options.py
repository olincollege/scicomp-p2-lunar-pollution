"""
Running and plotting options for simulation
"""
import matplotlib.pyplot as plt
# Extra library! All it does is create a progress bar in the terminal
from tqdm import tqdm

from agent import Particle
import helpers as h

def plot_option_journey(ax, start_option, model_option):
    """
    Plots the journey of a single particle hopping until it is removed

    Args:
        ax: Axes on which to plot
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either Butler's 1993 or 1997 paper
    """
    # Declare instance of a hopping particle
    particle = Particle(start_option, model_option)

    # In arbitrary large range, move and plot particles
    for i in range(1000):
        # Plot particle, label with iteration number
        h.plot_points(ax, particle.phi, particle.beta)
        ax.text(*h.coord_converter(particle.phi, particle.beta), i, fontsize = 6)

        # Move particle
        particle.move()

        # Check for photodestruction and plot
        if particle.is_photodestroy():
            print(f"Destroyed after {i} hops")
            h.plot_points(ax, particle.phi, particle.beta, color='g')
            break

        # Check for capture and plot
        if particle.is_captured():
            print(f"Captured after {i} hops")
            h.plot_points(ax, particle.phi, particle.beta, color='b')
            break

        # Update particle hop conditions appropriately
        particle.update_conditions()

def plot_option_one_run(ax, start_option, model_option, num_particles = 100):
    """
    Plot one run of the entire simulation with (default hundred) particles

    Args:
        ax: Axes on which to plot
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either Butler's 1993 or 1997 paper
        num_particles: Number of particles to run in simulation, default 100
    """
    # Track number of destroyed and captured particles
    n_destroyed = 0
    n_captured = 0

    # Run entire hopping journey for each particle
    for _ in range(num_particles):
        # Declare instance of a particle
        particle = Particle(start_option, model_option)

        # In arbitrary large range, move particles
        for _ in range(1000):
            particle.move()

            # Check for photodestruction and plot
            if particle.is_photodestroy():
                n_destroyed += 1
                h.plot_points(ax, particle.phi, particle.beta, color='g')
                break

            # Check for capture and plot
            if particle.is_captured():
                n_captured += 1
                h.plot_points(ax, particle.phi, particle.beta, color='b')
                break

            # Update particle conditions for next hop
            particle.update_conditions()

    # Print total number of photodestroyed and captured particles
    print(f"Photodestroyed: {n_destroyed}, Captured: {n_captured}")

def option_journey(start_option, model_option):
    """
    Consolidate all plotting for single particle journey

    Args:
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either Butler's 1993 or 1997 paper
    """
    # Create figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot sphere, points
    h.plot_sphere(ax)
    plot_option_journey(ax, start_option, model_option)
    h.plot_finish(ax, "Journey of single molecule")


def option_one_run(start_option, model_option):
    """
    Consolidate all plotting for final state of one run of the simulation

    Args:
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either Butler's 1993 or 1997 paper
    """
    # Create figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot sphere, points
    h.plot_sphere(ax)
    plot_option_one_run(ax, start_option, model_option)
    h.plot_finish(ax, "Final positions of 100 particles")

def option_all_runs(start_option, model_option, num_particles = 100, runs = 50):
    """
    Do multiple (default fifty) runs of the entire simulation and find average
    proportion of particles captured

    Args:
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either Butler's 1993 or 1997 paper
        num_particles: Number of particles to run in simulation, default 100
        runs: Number of runs of entire simulation
    """
    # Track total number of destroyed and captured particles across all runs
    total_destroyed = 0
    total_captured = 0

    # Run entire simulation a given number of times
    for _ in tqdm(range(runs)):

        # Track number of destroyed and captured particles
        n_destroyed = 0
        n_captured = 0

        # Run entire hopping journey for each particle
        for _ in range(num_particles):
            # Declare new instance of a particle
            particle = Particle(start_option, model_option)

            # In arbitrary large range, move particles
            for _ in range(1000):
                particle.move()
                # Check for photodestruction
                if particle.is_photodestroy():
                    n_destroyed += 1
                    break

                # Check for capture
                if particle.is_captured():
                    n_captured += 1
                    break

                # Update particle conditions for next hop
                particle.update_conditions()

        # Add to total photodestroyed and captured particles
        total_destroyed += n_destroyed
        total_captured += n_captured

    # Calcule total percentage captured and print
    perc_captured = total_captured / (total_captured + total_destroyed)
    print(f"Percentage captured: {perc_captured*100}%")
