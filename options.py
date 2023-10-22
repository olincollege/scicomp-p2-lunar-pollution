from motion import Particle
import helpers as h
import matplotlib.pyplot as plt
from tqdm import tqdm

def plot_option_journey(ax, phi, beta, model_option):
    """
    Plots the journey of a single particle hopping until it is removed

    Args:
        ax: Axes on which to plot
        phi: Polar spherical coordinate as a float (in radians)
        beta: Azimuthal spherical coordinate as a float (in radians)
        model_option: String for model - either from Butler's 1993 or 1997
    """
    p = Particle(phi, beta, model_option)

    for i in range(1000):
        h.plot_points(ax, p.phi, p.beta)
        ax.text(*h.coord_converter(p.phi, p.beta), i, fontsize = 6)
        p.move()
        if p.is_photodestroy():
            print(f"Destroyed after {i} hops")
            h.plot_points(ax, p.phi, p.beta, color='g')
            break

        if p.is_captured():
            print(f"Captured after {i} hops")
            h.plot_points(ax, p.phi, p.beta, color='b')
            break
            
        p.update_conditions()

def plot_option_one_run(ax, phi, beta, model_option):
    n_destroyed = 0
    n_captured = 0
    for _ in range(100):

        p = Particle(phi, beta, model_option)

        while n_captured + n_destroyed < 100:
            p.move()
            if p.is_photodestroy():
                n_destroyed += 1
                h.plot_points(ax, p.phi, p.beta, color='g')
                break

            if p.is_captured():
                n_captured += 1
                h.plot_points(ax, p.phi, p.beta, color='b')
                break

            p.update_conditions()

    print(f"Photodestroyed: {n_destroyed}, Captured: {n_captured}")

def option_all_runs(phi, beta, model_option):
    total_destroyed = 0
    total_captured = 0
    for _ in tqdm(range(50)):

        n_destroyed = 0
        n_captured = 0

        for _ in range(100):
            p = Particle(phi, beta, model_option)

            for _ in range(1000):
                p.move()
                if p.is_photodestroy():
                    n_destroyed += 1
                    break

                if p.is_captured():
                    n_captured += 1
                    break
                
                p.update_conditions()

        total_destroyed += n_destroyed
        total_captured += n_captured
    
    perc_captured = total_captured / (total_captured + total_destroyed)
    print(f"Percentage captured: {perc_captured*100}%")

def option_journey(phi, beta, model_option):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    h.plot_sphere(ax)
    plot_option_journey(ax, phi, beta, model_option)
    h.plot_finish(ax, "Journey of single molecule")


def option_one_run(phi, beta, model_option):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    h.plot_sphere(ax)
    plot_option_one_run(ax, phi, beta, model_option)
    h.plot_finish(ax, "Positions of 100 molecules")