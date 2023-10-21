# # To do:
# 1) Implement for different amu to see rocket pollutants - uses water 20% is cold trapped released at 70 latitude
# 2) Create plotting/runing options by reorganizing everything
# These include 1993 vs. 1997 paper params, maybe an animation, possible loading bar for long runs
# 3) Write documentation

# # Notes:
# Existing monte carlo simulation may not accurately model lunar transport, argued by Dr. Prem
# ^^ Since water interactions with each other are significant, and also we know cold traps
# Very sensitive to photodissociation 


# # Options:
# 1) 1993 Simulation new decay constant journey, one run, multiple runs
# 2) 1997 Simulation new decay constant journey, one run, multiple runs
# 3) Dr. Prem simulation one run, multiple runs with Butler photodissociation
# 4) Dr. Prem simulation multiple runs with her photodissociation
import matplotlib.pyplot as plt
from motion import Particle
import helpers as h
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
    circle1_phi = np.full(100, h.PHI_POLE)
    circle2_phi = np.full(100, np.pi - h.PHI_POLE)

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

def plot_option_journey(ax, phi, beta, model_option):
    p = Particle(phi, beta, model_option)

    for i in range(1000):
        plot_points(ax, p.phi, p.beta)
        ax.text(*coord_converter(p.phi, p.beta), i, fontsize = 6)
        p.move()
        if p.is_photodestroy():
            print(f"Destroyed after {i} hops")
            plot_points(ax, p.phi, p.beta, color='g')
            break

        if p.is_captured():
            print(f"Captured after {i} hops")
            plot_points(ax, p.phi, p.beta, color='b')
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
                plot_points(ax, p.phi, p.beta, color='g')
                break

            if p.is_captured():
                n_captured += 1
                plot_points(ax, p.phi, p.beta, color='b')
                break

            p.update_conditions()

    print(f"Photodestroyed: {n_destroyed}, Captured: {n_captured}")

def option_all_runs(phi, beta, model_option):
    total_destroyed = 0
    total_captured = 0
    for _ in range(50):
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

    plot_sphere(ax)
    plot_option_journey(ax, phi, beta, model_option)
    plot_finish(ax, "Journey of single molecule")


def option_one_run(phi, beta, model_option):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    plot_sphere(ax)
    plot_option_one_run(ax, phi, beta, model_option)
    plot_finish(ax, "Positions of 100 molecules")

def choose_start():
    phi, beta = h.sample_spherical()

    print("Choose your starting point:")
    print("A) Random")
    print("B) 70 degrees South (Dr. Prem)")
    start_point = input("Enter your starting point option (just the letter): ")
    if start_point == "A":
        return phi, beta
    
    elif start_point == "B":
        phi = 70 * (np.pi / 180)
        beta = 0
        return phi, beta

    print("ERROR: Please enter a valid option!")
    print("")
    return choose_start()
    
def choose_model():
    model_option = "1997"

    print("Choose your model:")
    print("A) Butler (1997)")
    print("B) Butler (1993)")
    model = input("Enter your starting point option (just the letter): ")
    if model == "A":
        return model_option
    
    elif model == "B":
        model_option = "1993"
        return model_option

    print("ERROR: Please enter a valid option!")
    print("")
    return choose_model()

def choose_run(phi, beta, model_option):
    print("Choose your run type:")
    print("A) Plot of journey of one particle")
    print("B) Final destinations of multiple particles in model")
    print("C) Average of 50 runs of simulation")
    run_type = input("Enter your model type option (just the letter): ")
    if run_type == "A":
        option_journey(phi, beta, model_option)
    elif run_type == "B":
        option_one_run(phi, beta, model_option)
    elif run_type == "C":
        option_all_runs(phi, beta, model_option)
    else:
        print("ERROR: Please enter a valid option!")
        print("")
        choose_run(phi, beta, model_option)



def process_options():
    phi, beta = choose_start()
    model_option = choose_model()
    choose_run(phi, beta, model_option)
    
    

process_options()
# option_all_runs()

# option_one_run()
# # Plotting journey of single molecule for visualizing
# # Maybe include as a "menu" select item when plotting?
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')

# plot_sphere(ax)
# plot_option_journey(ax)
# plot_finish(ax, "Journey of single molecule")

# plot_sphere(ax)
# plot_option_one_run(ax)
# plot_finish(ax, "Positions of 100 molecules")