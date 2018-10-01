import os
import numpy as np

from constants import *
from params import *
import calculations as calc


def simulation_time(n):
    """ Returns simulation time in years, months, days. """
    years = m.floor( n*dt / YEAR )
    months = m.floor( (n*dt - years*YEAR) / MONTH )
    days = m.floor( (n*dt - years*YEAR - months*MONTH) / DAY )
    
    return years, months, days

def initialise():
    """ Initialise the model using conditions specified in params.py. """

    # Create dictionaries to hold simulation data
    # Initialise with empty arrays of size = number of timesteps + 1 (for initial conditions)

    box1 = {'Ta': np.zeros(nt+1),         # Atmospheric temperature
            'Ts': np.zeros(nt+1),         # Surface temperature
            'To': np.zeros(nt+1),         # Oceanic temperature
            'Ft': np.zeros(nt+1),         # Top of atmosphere flux
            'Fs': np.zeros(nt+1),         # Surface flux
            'Feva': np.zeros(nt+1),       # Evaporation
            'MSE': np.zeros(nt+1),        # Moist static energy
            'Te': Te1                     # Emission temperature (from params)
            }
    
    box2 = {'Ta': np.zeros(nt+1),         # Atmospheric temperature
            'Ts': np.zeros(nt+1),         # Surface temperature
            'To': np.zeros(nt+1),         # Oceanic temperature
            'Ft': np.zeros(nt+1),         # Top of atmosphere flux
            'Fs': np.zeros(nt+1),         # Surface flux
            'Feva': np.zeros(nt+1),       # Evaporation
            'MSE': np.zeros(nt+1),        # Moist static energy
            'Te': Te2                     # Emission temperature (from params)
            }

    glob = {'time': np.arange(nt+1)*dt,   # simulation time in seconds
            'Fa' : np.zeros(nt+1),        # Atmospheric flux
            'Fo' : np.zeros(nt+1),        # Oceanic flux
            'Psia': np.zeros(nt+1),       # Atmospheric circulation strength
            'Psio': np.zeros(nt+1),       # Oceanic circulation strength
            'MTspt': np.zeros(nt+1),      # Moisture transport
            }

    # Carbon dioxide trajectory given in params
    if CO2_increase == 'linear':
        glob['CO2'] = np.linspace(CO2_init, CO2_final, nt+1)
    elif CO2_increase == 'exp':
        glob['CO2'] = CO2_final - (CO2_final-CO2_init) * np.exp(-np.arange(nt+1)*dt / tau_CO2)
    else:
        glob['CO2'] = np.ones(nt+1) * CO2_init
       
    # Initial conditions specified in params.py,
    # multiplied by a random noise of magnitude 'ic'.
    box1['Ta'][0] = Ta1_init + ic*np.random.normal()
    box2['Ta'][0] = Ta2_init + ic*np.random.normal()
    box1['To'][0] = To1_init + ic*np.random.normal()
    box2['To'][0] = To2_init + ic*np.random.normal()
    box1['Ts'][0] = Ts1_init + ic*np.random.normal()
    box2['Ts'][0] = Ts2_init + ic*np.random.normal()

    # Compute initial saturation water vapour pressure and specific humidity
    # If water vapour feedback is turned off, this will be used again and again
    box1['esat_init'], box1['qsat_init'] = calc.CLAUSIUS_CLAPEYRON(box1['Ts'][0], box1['Ta'][0])
    box2['esat_init'], box2['qsat_init'] = calc.CLAUSIUS_CLAPEYRON(box2['Ts'][0], box2['Ta'][0])

    return box1, box2, glob



def update(n, box1, box2, glob):
    """ Update other variables in the simulation after temperatures have been
        stepped forward. """
    
    # Compute saturation water vapour pressure and specific humidity
    esat1, qsat1 = calc.CLAUSIUS_CLAPEYRON(box1['Ts'][n], box1['Ta'][n])
    esat2, qsat2 = calc.CLAUSIUS_CLAPEYRON(box2['Ts'][n], box2['Ta'][n])

    # Emissivity calculations !!missing BB!!
    if WaVa_feedback == True:
        epsa1 = calc.EPSA(esat1, qsat1, glob['CO2'][n])
        epsa2 = calc.EPSA(esat2, qsat2, glob['CO2'][n])
    else: # use initial values for saturation, humidity
        epsa1 = calc.EPSA(box1['esat_init'], box1['qsat_init'], glob['CO2'][n])
        epsa2 = calc.EPSA(box2['esat_init'], box2['qsat_init'], glob['CO2'][n])

    # Circulation strengths
    glob['Psia'][n], glob['Psio'][n] = calc.PSI(box1['Ts'][n], box2['Ts'][n])

    # Moisture
    box1['MSE'][n] = calc.MSE(box1['Ts'][n], box1['Ta'][n], qsat1)
    box2['MSE'][n] = calc.MSE(box2['Ts'][n], box2['Ta'][n], qsat2)
    glob['MTspt'][n] = calc.MTSPT(glob['Psia'][n], qsat1, qsat2)

    # Net surface heat flux
    box1['Fs'][n], box1['Feva'][n] = calc.FS(box1['Ts'][n], box1['Ta'][n], box1['Te'], epsa1)
    box2['Fs'][n], box2['Feva'][n] = calc.FS(box2['Ts'][n], box2['Ta'][n], box2['Te'], epsa2)

    # Net top-of-atmosphere heat flux
    box1['Ft'][n] = calc.FT(box1['Ts'][n], box1['Ta'][n], box1['Te'], epsa1)
    box2['Ft'][n] = calc.FT(box2['Ts'][n], box2['Ta'][n], box2['Te'], epsa2)

    # Global heat fluxes
    glob['Fa'][n] = calc.FA(glob['Psia'][n], box1['MSE'][n], box2['MSE'][n]) # atmospheric
    glob['Fo'][n] = calc.FO(glob['Psio'][n], box1['Ts'][n], box2['To'][n]) # oceanic
    
    return



def step(n, box1, box2, glob):
    """ Step forward the temperatures. """
    
    # Rescale Psio (kg/s -> W m-2 K-1)
    Psi_res = glob['Psio'][n] * CPO / (np.pi * RADIUS**2)
    
    # Atmosphere
    Tend_atm1 = (box1['Fs'][n] + box1['Ft'][n] - glob['Fa'][n]) / HCA
    Tend_atm2 = (box2['Fs'][n] + box2['Ft'][n] + glob['Fa'][n]) / HCA

    box1['Ta'][n+1] = box1['Ta'][n] + dt*Tend_atm1
    box2['Ta'][n+1] = box2['Ta'][n] + dt*Tend_atm2

    # Surface - mixed layer
    Tend_oce1_ml = -( box1['Fs'][n] - Psi_res*(box1['To'][n] - box1['Ts'][n]) ) / HCM
    Tend_oce2_ml = -( box2['Fs'][n] - Psi_res*(box1['Ts'][n] - box2['Ts'][n]) ) / HCM
    
    box1['Ts'][n+1] = box1['Ts'][n] + dt*Tend_oce1_ml
    box2['Ts'][n+1] = box2['Ts'][n] + dt*Tend_oce2_ml
    
    # Ocean - thermocline
    Tend_oce1_th = Psi_res*(box2['To'][n] - box1['To'][n]) / HCO
    Tend_oce2_th = Psi_res*(box2['Ts'][n] - box2['To'][n]) / HCO

    box1['To'][n+1] = box1['To'][n] + dt*Tend_oce1_th
    box2['To'][n+1] = box2['To'][n] + dt*Tend_oce2_th

    return

def save(n, box1, box2, glob):
    """ Save time series data for plotting. """
  
    # Create the directory if it doesn't exist
    if save_loc not in ("", None):
        if not os.path.exists(save_loc):
            os.makedirs(save_loc)

    # ------- #
    #  Box 1  #
    # ------- #
    # (row,col) = (timestep,variable)
    box1_arr = np.zeros( (n, 7) )

    box1_arr[:,0] = box1['Ta'][:n]
    box1_arr[:,1] = box1['Ts'][:n]
    box1_arr[:,2] = box1['To'][:n]
    box1_arr[:,3] = box1['Ft'][:n]
    box1_arr[:,4] = box1['Fs'][:n]
    box1_arr[:,5] = box1['Feva'][:n]
    box1_arr[:,6] = box1['MSE'][:n]
    
    box1_save_file = save_loc + "box1.out"
    np.savetxt(box1_save_file, box1_arr)
    
    # ------- #
    #  Box 2  #
    # ------- #
    box2_arr = np.zeros( (n, 7) )

    box2_arr[:,0] = box2['Ta'][:n]
    box2_arr[:,1] = box2['Ts'][:n]
    box2_arr[:,2] = box2['To'][:n]
    box2_arr[:,3] = box2['Ft'][:n]
    box2_arr[:,4] = box2['Fs'][:n]
    box2_arr[:,5] = box2['Feva'][:n]
    box2_arr[:,6] = box2['MSE'][:n]
    
    box2_save_file = save_loc + "box2.out"
    np.savetxt(box2_save_file, box2_arr)

    # ------------- #
    #  Global data  #
    # ------------- #
    glob_arr = np.zeros( (n, 7) )

    glob_arr[:,0] = glob['time'][:n]
    glob_arr[:,1] = glob['Fa'][:n]
    glob_arr[:,2] = glob['Fo'][:n]
    glob_arr[:,3] = glob['Psia'][:n]
    glob_arr[:,4] = glob['Psio'][:n]
    glob_arr[:,5] = glob['MTspt'][:n]
    glob_arr[:,6] = glob['CO2'][:n]
    
    glob_save_file = save_loc + "global.out"
    np.savetxt(glob_save_file, glob_arr)
    
    return

