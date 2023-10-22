"""
Main code run for lunar hopping simulation
"""

import options

def choose_start():
    """
    Choose the starting coordinate calculation option of the particles based on
    user input

    Return:
        String with starting coordinate option, either random or
        seventy_deg_south - starting point for simulations in Dr. Prem's paper
    """
    # Print out options
    print("Choose your starting point:")
    print("A) Random")
    print("B) 70 degrees South (Dr. Prem)")
    # Ask for user input
    start_point = input("Enter your starting point option (just the letter): ")

    # Return relevant starting option based on user input
    if start_point == "A":
        return "random"
    if start_point == "B":
        return "seventy_deg_south"

    # Print error if invalid input and try again by recursively calling
    print("ERROR: Please enter a valid option!")
    print("")
    return choose_start()

def choose_model():
    """
    Choose the model to run simulation with - either the model from Butler's
    1993 paper or 1997 paper

    Return:
        String specifying either the "1993" paper or "1997" paper
    """
    # Print out options
    print("Choose your model:")
    print("A) Butler (1997)")
    print("B) Butler (1993)")
    # Ask for user input
    model = input("Enter your starting point option (just the letter): ")

    # Return relevant model option based on user input
    if model == "A":
        return "1997"
    if model == "B":
        return "1993"

    # Print error if invalid input and try again by recursively calling
    print("ERROR: Please enter a valid option!")
    print("")
    return choose_model()

def choose_run(start_option, model_option):
    """
    Choose type of run

    Either plotting journey of one particle, plotting final positions of run of
    one simulation (default hundred particles), or average proportion of
    particles captured in many runs of simulation (default fifty runs)

    Args:
        start_option: String specifying method of choosing initial positions
        model_option: String specifying model used in simulations
    """
    # Print out options
    print("Choose your run type:")
    print("A) Plot of journey of one particle")
    print("B) Final destinations of multiple particles in model")
    print("C) Average of 50 runs of simulation")
    # Ask for user input
    run_type = input("Enter your model type option (just the letter): ")

    # Run relevant option based on user input
    if run_type == "A":
        options.option_journey(start_option, model_option)
    elif run_type == "B":
        options.option_one_run(start_option, model_option)
    elif run_type == "C":
        options.option_all_runs(start_option, model_option)
    else:
        # Print error if invalid input and try again by recursively calling
        print("ERROR: Please enter a valid option!")
        print("")
        choose_run(start_option, model_option)



my_start = choose_start()
my_model = choose_model()
choose_run(my_start, my_model)
