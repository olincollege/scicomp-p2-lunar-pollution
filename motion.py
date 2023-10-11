import numpy as np

G_MOON = 1 # Change to moon g
T_0 = 100 # Unclear what T_0 and T_1 mean for modelling
T_1 = 100
N_UNKNOWN = 0.25 # I can't figure out what this does
PHOTOLOSS_TIMESCALE = 10000 # See paper for exact value

def time_per_hop(v_initial):
    return np.sqrt(2) * v_initial / G_MOON

def distance_per_hop(time, v_initial):
    return 0.5 * v_initial * time

# But also this is binned every 10 degrees - figure out what's going on
def surface_temp(phi):
    return T_0 + (T_1 * (np.cos(phi - (np.pi / 2)) ** N_UNKNOWN))  

def probs_photodestroy(t_hop):
    return 1 - np.exp(t_hop / PHOTOLOSS_TIMESCALE)

# TODO - figure out
def prob_capture():
    pass