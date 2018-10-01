from constants import *

# Directory for saving (relative path)
save_loc = "control/"


# ----------------- #
#  Simulation time  #
# ----------------- #
# Number of years to run the simulation
nyr = 500

# Timestep (< 2 days for stability)
dt = float(1*DAY)

# Number of timesteps
nt = int(round( nyr*YEAR / dt ))

# Print, save every n_print, n_save timesteps
n_print = int(round( 10*YEAR / dt ))
n_save = int(round( 1000*YEAR / dt ))


# -------------------- #
#  Initial conditions  #
# -------------------- #
# Atmospheric temperatures (in K) (1:Tropics, 2:Extra-tropics)
Ta1_init = 260.
Ta2_init = 240.

# Ocean temperatures
To1_init = 280.
To2_init = 280.

# Surface temperatures
Ts1_init = 300.
Ts2_init = 280.

# Amplitude of random noise to add to above starting values. 'ic' will multiply
# numbers randomly drawn from a normal distribution of mean 0, standard deviation 1
ic = 0.


# --------- #
#  Forcing  #
# --------- #
# Emission temperatures (in K)
Te1 = TEMI1 
Te2 = TEMI2

# Initial and final carbon dioxide concentrations
CO2_init = 280.
CO2_final = 2*CO2_init

# Manner in which CO2 concentration increases
""" 'none'   - remain at CO2_init throughout the simulation.
    'linear' - increase linearly from (t=0, C02_init) to (t=nyr*YEAR, CO2_final)
    'exp'    - increase by a factor of (CO2_final-CO2_init) over a timescale of tau_co2, 
               at an exponentially decreasing rate: exp(-t/tau_c02). """
CO2_increase = 'none'
tau_CO2 = float(100*YEAR)

# Include water vapour feedback (True/False)
WaVa_feedback = False

