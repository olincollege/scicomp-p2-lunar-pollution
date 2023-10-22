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
import helpers
import numpy as np
import options

def choose_start():
    phi, beta = helpers.sample_spherical()

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
        options.option_journey(phi, beta, model_option)
    elif run_type == "B":
        options.option_one_run(phi, beta, model_option)
    elif run_type == "C":
        options.option_all_runs(phi, beta, model_option)
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