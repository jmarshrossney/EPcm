import numpy as np

from constants import *
from params import *
import model
import plot

# ------------------ #
#  Initialise model  #
# ------------------ #
box1, box2, glob = model.initialise()


# --------------------------- #
#  Integrate forward in time  #
# --------------------------- #
for n in range(nt):
    
    # Update fluxes, moisture, circulation using current temperatures
    model.update(n, box1, box2, glob)

    # Step temperatures forward
    model.step(n, box1, box2, glob)

    # Print every 'n_print' steps
    if n % n_print == 0:
        years, months, days = model.simulation_time(n)
        print "Simulation time: %dy, %dm, %dd" %(years, months, days)

    # Save every n_save steps (exluding step 0)
    if (n+1) % n_save == 0:
        years, months, days = model.simulation_time(n)
        "Saving time series at simulation time: %d years, %d months, %d days" %(years, months, days)
        
        model.save(n+1, box1, box2, glob)

# Update fluxes, moisture, circulation for final timestep
model.update(nt, box1, box2, glob)

# Print final time
years, months, days = model.simulation_time(nt)
print "Final simulation time: %d years, %d months, %d days" %(years, months, days)


# -------------- #
#  Save outputs  #
# -------------- #
print "\nSave directory: %s" %save_loc
print "Saving time series data..."
model.save(nt, box1, box2, glob)


# -------------- #
#  Save figures  #
# -------------- #
print "Saving figures..."
plot.auto(box1, box2, glob)


print "Finished"

