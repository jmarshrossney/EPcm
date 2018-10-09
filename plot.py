import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as mpl_pdf
from sys import argv

from constants import *
from params import *

# Set default plotting parameters
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.size'] = 8
# Prevent axis offset: doing this via rcParams only works for some matplotlib versions
# Can do it individually for each axis ( ax.ticklabel_format(useOffset=False) ) but ughh
if 'axes.formatter.useoffset' in plt.rcParams.keys():
    plt.rcParams['axes.formatter.useoffset'] = False
    plt.rcParams['axes.formatter.limits'] = (-2,4) # also use scientific notation

# Colour scheme
cs = {
      'x': 'black',
      
      'atm': 'skyblue',
      'surf': 'lightseagreen',
      'oce': 'darkblue',
      'oatot': 'royalblue',
      
      'T': 'mediumturquoise',
      'ET': 'darkblue',
      'T2': 'limegreen',
      'ET2': 'darkgreen',
      'T3': 'peru',
      'ET3': 'saddlebrown',
      'T4': 'fuchsia',
      'ET4': 'indigo',
      'av': 'orange',
      'tot': 'red',
      } 

def load_data(loc):
    """ Load output data from a simulation, from loc/box1.out, loc/box2.out, loc/glob.out """
    # ------- #
    #  Box 1  #
    # ------- #
    box1_arr = np.loadtxt(loc+"box1.out")
    
    box1 = {'Ta': box1_arr[:,0],         # Atmospheric temperature
            'Ts': box1_arr[:,1],         # Surface temperature
            'To': box1_arr[:,2],         # Oceanic temperature
            'Ft': box1_arr[:,3],         # Top of atmosphere flux
            'Fs': box1_arr[:,4],         # Surface flux
            'Feva': box1_arr[:,5],       # Evaporation
            'MSE': box1_arr[:,6],        # Moist static energy
            'Te': Te1                    # Emission temperature (from params)
            }
    
    # ------- #
    #  Box 2  #
    # ------- #
    box2_arr = np.loadtxt(loc+"box2.out")
    
    box2 = {'Ta': box2_arr[:,0],         # Atmospheric temperature
            'Ts': box2_arr[:,1],         # Surface temperature
            'To': box2_arr[:,2],         # Oceanic temperature
            'Ft': box2_arr[:,3],         # Top of atmosphere flux
            'Fs': box2_arr[:,4],         # Surface flux
            'Feva': box2_arr[:,5],       # Evaporation
            'MSE': box2_arr[:,6],        # Moist static energy
            'Te': Te2                    # Emission temperature (from params)
            }

    # ------------- #
    #  Global data  #
    # ------------- #
    glob_arr = np.loadtxt(loc+"global.out")
    
    glob = {'time': glob_arr[:,0],       # simulation time in seconds
            'Fa' : glob_arr[:,1],        # Atmospheric flux
            'Fo' : glob_arr[:,2],        # Oceanic flux
            'Psia': glob_arr[:,3],       # Atmospheric circulation strength
            'Psio': glob_arr[:,4],       # Oceanic circulation strength
            'MTspt': glob_arr[:,5],      # Moisture transport
            'CO2': glob_arr[:,6]         # Carbon dioxide
            }

    return box1, box2, glob


#####################################
##  Plotting function definitions  ##
#####################################

def temperatures(box1, box2, glob):
    """ Plot all individual temperatures from both boxes. 

                    python plot.py temps              """

    time = glob['time'] / YEAR

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='all')
    fig.suptitle("Temperatures")

    ax1.set_title("Tropics")
    ax1.set_ylabel("Temperature (K)")
    atm, = ax1.plot(time, box1['Ta'], color=cs['atm'], label="Atm.")

    ax2.set_title("Extra-Tropics")
    ax2.plot(time, box2['Ta'], color=cs['atm'])
    
    ax3.set_ylabel("Temperature (K)")
    surf, = ax3.plot(time, box1['Ts'], color=cs['surf'], label="Surf.")

    ax4.plot(time, box2['Ts'], color=cs['surf'])

    ax5.set_xlabel("Time (years)")
    ax5.set_ylabel("Temperature (K)")
    oce, = ax5.plot(time, box1['To'], color=cs['oce'], label="Oce.")

    ax6.set_xlabel("Time (years)")
    ax6.plot(time, box2['To'], color=cs['oce'])
   
    handles = [atm, surf, oce]
    labels = [h.get_label() for h in handles]
    fig.legend(handles=handles, labels=labels, loc=(0.85,0.45))
    
    fig.tight_layout(rect=[0,0.03,1,0.95])

    return fig


def transport(box1, box2, glob):
    """ Plot heat and moisture transport and circulation strength.
            
                    python plot.py transport        """

    time = glob['time'] / YEAR

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='all')
    fig.suptitle("Transport")

    ax1.set_title("Heat transport")
    ax1.set_ylabel("Power ($10^{15}W$)")
    atm, = ax1.plot(time, (glob['Fa'] * np.pi*RADIUS**2) / PW, color=cs['atm'], label="Atm.")

    ax2.set_title("Circulation strength")
    ax2.set_ylabel("Flow ($10^9 kg/s$)")
    ax2.plot(time, glob['Psia'] / SV, color=cs['atm'])
    
    ax3.set_ylabel("Power ($10^{15}W$)")
    oce, = ax3.plot(time, (glob['Fo'] * np.pi*RADIUS**2) / PW, color=cs['oce'], label="Oce.")

    ax4.set_ylabel("Flow ($10^9 kg/s$)")
    ax4.plot(time, glob['Psio'] / SV, color=cs['oce'])

    ax5.set_xlabel("Time (years)")
    ax5.set_ylabel("Power ($10^{15}W$)")
    atmoce, = ax5.plot(time, ((glob['Fo']+glob['Fa']) * np.pi*RADIUS**2) / PW, color=cs['oatot'], label="Atm.+Oce.")

    ax6.set_title("Moisture transport")
    ax6.set_xlabel("Time (years)")
    ax6.set_ylabel("Flow ($10^9 kg/s$)")
    ax6.plot(time, glob['MTspt'] / SV, color=cs['x'])
   
    handles = [atm, oce, atmoce]
    labels = [h.get_label() for h in handles]
    fig.legend(handles=handles, labels=labels, loc=(0.8,0.45))

    fig.tight_layout(rect=[0,0.03,1,0.95])
    
    return fig


def hydro(box1, box2, glob):
    """ Plot hydrological cycle (except moisture transport which in in 'transport')
                    
                    python plot.py hydro            """

    time = glob['time'] / YEAR

    # Box 1
    evap1 = box1['Feva'] * (np.pi*RADIUS**2) / LV           # Evaporation in kg/s
    prcp1 = evap1 - glob['MTspt']                           # Precipitation in kg/s
    prcp1_mmday = (1000*prcp1*DAY) / (RHO*np.pi*RADIUS**2)  # in mm/day
    q1 = (box1['MSE'] - CPA*0.5*(box1['Ta']+box1['Ts']))/LV # Low level spec. humidity in kg/kg
    
    # Box 2
    evap2 = box2['Feva'] * (np.pi*RADIUS**2) / LV           # Evaporation in kg/s
    prcp2 = evap2 + glob['MTspt']                           # Precipitation in kg/s
    prcp2_mmday = (1000*prcp2*DAY) / (RHO*np.pi*RADIUS**2)  # in mm/day
    q2 = (box2['MSE'] - CPA*0.5*(box2['Ta']+box2['Ts']))/LV # Low level spec. humidity in kg/kg
    
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='all')
    fig.suptitle("Hydrological cycle")

    ax1.set_title("Tropics")
    ax1.set_ylabel("Evaporation\n($10^9$ kg/s)")
    ax1.plot(time, evap1 / SV, color=cs['T'], label="Trop.")
    
    ax2.set_title("Extra-Tropics")
    ax2.plot(time, evap2 / SV, color=cs['ET'], label="E-Trop.")

    ax3.set_ylabel("Precipitation\n($10^9$ kg/s)")
    ax3.plot(time, prcp1 / SV, color=cs['T2'], label="Trop.")
    
    ax4.plot(time, prcp2 / SV, color=cs['ET2'], label="E-Trop.")

    ax5.set_xlabel("Time (years)")
    ax5.set_ylabel("Specific humidity\n(kg/kg)")
    ax5.plot(time, q1, color=cs['T3'], label="Trop.")
    
    ax6.set_xlabel("Time (years)")
    ax6.plot(time, q2, color=cs['ET3'], label="E-Trop.")

    fig.tight_layout(rect=[0,0.03,1,0.95])

    return fig


def fluxes(box1, box2, glob):
    """ Plot vertical fluxes

                    python plot.py flux         """

    time = glob['time'] / YEAR
    
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='all')
    fig.suptitle("Fluxes")

    ax1.set_title("Tropics")
    ax1.set_ylabel("TOA flux\n($Wm^{-2}$)")
    ax1.plot(time, box1['Ft'], color=cs['T'], label="Trop.")
    
    ax2.set_title("Extra-Tropics")
    ax2.plot(time, box2['Ft'], color=cs['ET'], label="E-Trop")

    ax3.set_ylabel("Surf. heat flux\n($Wm^{-2}$)")
    ax3.plot(time, box1['Fs'], color=cs['T2'], label="Trop.")
    
    ax4.plot(time, box2['Fs'], color=cs['ET2'], label="E-Trop")

    ax5.set_xlabel("Time (years)")
    ax5.set_ylabel("Evap. flux\n($Wm^{-2}$)")
    ax5.plot(time, box1['Feva'], color=cs['T3'], label="Trop.")
    
    ax6.set_xlabel("Time (years)")
    ax6.plot(time, box2['Feva'], color=cs['ET3'], label="E-Trop")

    fig.tight_layout(rect=[0,0.03,1,0.95])
    
    return fig


def energy(box1, box2, glob):
    """ Plot energy content

                python plot.py energy           """

    time = glob['time'] / YEAR

    # Compute heat content
    hc1_at = HCA * box1['Ta']       # atmos?
    hc1_ml = HCM * box1['Ts']       # mixed layer
    hc1_th = HCO * box1['To']       # thermocline
    hc1_tot = hc1_ml + hc1_th       # oce. total for box 1

    hc2_at = HCA * box2['Ta']       # atmos?
    hc2_ml = HCM * box2['Ts']       # mixed layer
    hc2_th = HCO * box2['To']       # thermocline
    hc2_tot = hc2_ml + hc2_th       # oce. total for box 2
    
    hc_tot = hc1_tot + hc2_tot      # oce. global total
    hc_tot_at = hc1_at + hc2_at      # atm. global total

    MSE_tot = box1['MSE'] + box2['MSE']

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) \
            = plt.subplots(4, 2, sharex='all')
    fig.suptitle("Energy/heat content")

    ax1.set_title("Tropics")
    ax1.set_ylabel("Atmosphere\n($10^9 Jm^{-2}$)")
    ax1.plot(time, hc1_at / SV, color=cs['T'], label="Trop.")
    
    ax2.set_title("Extra-Tropics")
    ax2.plot(time, hc2_at / SV, color=cs['ET'], label="E-Trop.")
    
    ax3.set_ylabel("Mixed Layer\n($10^9 Jm^{-2}$)")
    ax3.plot(time, hc1_ml / SV, color=cs['T2'], label="Trop.")
    
    ax4.plot(time, hc2_ml / SV, color=cs['ET2'], label="E-Trop.")

    ax5.set_ylabel("Thermocline\n($10^9 Jm^{-2}$)")
    ax5.plot(time, hc1_th / SV, color=cs['T3'], label="Trop.")
    
    ax6.plot(time, hc2_th / SV, color=cs['ET3'], label="E-Trop.")
    
    ax7.set_xlabel("Time (years)")
    ax7.set_ylabel("Moist static energy\n($10^6 Jm^{-2}$)")
    ax7.plot(time, box1['MSE'] / 1e6, color=cs['T4'], label="Trop.")
    
    ax8.set_xlabel("Time (years)")
    ax8.plot(time, box2['MSE'] / 1e6, color=cs['ET4'], label="E-Trop.")

    fig.tight_layout(rect=[0,0.03,1,0.95])

    return fig


def carbon_dioxide(box1, box2, glob):
    """ Plot carbon dioxide concentration and global temperature
                    python plot.py co2              """


    time = glob['time'] / YEAR
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='all')
    
    ax1.set_title("Carbon dioxide")
    ax1.set_ylabel("Concentration (ppm)")
    ax1.plot(time, glob['CO2'], color=cs['x'])

    ax2.set_title("Average temperature")
    ax2.set_ylabel("Temperature (K)")
    atm, = ax2.plot(time, 0.5*(box1['Ta']+box2['Ta']), color=cs['atm'], label="Atm.")
    
    ax3.set_title("Average temperature")
    ax3.set_xlabel("Time (years)")
    ax3.set_ylabel("Temperature (K)")
    surf, = ax3.plot(time, 0.5*(box1['Ts']+box2['Ts']), color=cs['surf'], label="Surf.")
    
    ax4.set_xlabel("Time (years)")
    oce, = ax4.plot(time, 0.5*(box1['To']+box2['To']), color=cs['oce'], label="Oce.")

    handles = [atm, surf, oce]
    labels = [h.get_label() for h in handles]
    fig.legend(handles=handles, labels=labels, loc=(0.85, 0.6))
    
    fig.tight_layout()
    
    return fig


def ocean(box1, box2, glob):
    """ Plot things to do with the ocean

                python plot.py ocean            """

    time = glob['time'] / YEAR
    
    # Compute heat content
    hc1_ml = HCM * box1['Ts']       # mixed layer
    hc1_th = HCO * box1['To']       # thermocline
    hc1_tot = hc1_ml + hc1_th       # total for box 1

    hc2_ml = HCM * box2['Ts']       # mixed layer
    hc2_th = HCO * box2['To']       # thermocline
    hc2_tot = hc2_ml + hc2_th       # total for box 2

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='all')
    fig.suptitle("Ocean")

    ax1.set_title("Sea Surface Temperatures")
    ax1.set_ylabel("Temperature (K)")
    ax1.plot(time, box1['Ts'], color=cs['T'], label="Trop.")
    ax1.plot(time, box2['Ts'], color=cs['ET'], label="E-Trop.")
    ax1.plot(time, 0.5*(box1['Ts']+box2['Ts']), color=cs['av'], label="Av.")

    ax2.set_title("Ocean Temperatures")
    ax2.set_ylabel("Temperature (K)")
    ax2.plot(time, box1['To'], color=cs['T'], label="Trop.")
    ax2.plot(time, box2['To'], color=cs['ET'], label="E-Trop.")
    ax2.plot(time, 0.5*(box1['To']+box2['To']), color=cs['av'], label="Av.")
    ax2.legend()

    ax3.set_title("Heat transport")
    ax3.set_xlabel("Time (years)")
    ax3.set_ylabel("Power ($10^{15}W$)")
    ax3.plot(time, (glob['Fo'] * np.pi*RADIUS**2) / PW, color=cs['x'])

    ax4.set_title("Change in heat content")
    ax4.set_xlabel("Time (years)")
    ax4.set_ylabel("Energy ($10^9 Jm^{-2}$)")
    ax4.plot(time, (hc1_ml-hc1_ml[0]) / SV, color=cs['T'], label="Trop. ML")
    ax4.plot(time, (hc2_ml-hc2_ml[0]) / SV, color=cs['ET'], label="E-Trop. ML")
    ax4.plot(time, (hc1_th-hc1_th[0]) / SV, color=cs['T2'], label="Trop. Th")
    ax4.plot(time, (hc2_th-hc2_th[0]) / SV, color=cs['ET2'], label="E-Trop. Th")
    ax4.legend(loc=2)
    
    fig.tight_layout(rect=[0,0.03,1,0.95])

    return fig

def atmosphere(box1, box2, glob):
    """ Plot things to do with the atmosphere
                    
                    python plot.py atmos            """

    time = glob['time'] / YEAR
    
    # Compute heat content
    hc1 = HCA * box1['Ta'] 
    hc2 = HCA * box2['Ta']

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='all')
    fig.suptitle("Atmosphere")

    ax1.set_title("Atmospheric Temperatures")
    ax1.set_ylabel("Temperature (K)")
    ax1.plot(time, box1['Ta'], color=cs['T'], label="Trop.")
    ax1.plot(time, box2['Ta'], color=cs['ET'], label="E-Trop.")
    ax1.plot(time, 0.5*(box1['Ta']+box2['Ta']), color=cs['av'], label="Av.")
    ax1.legend(loc=1)

    ax2.set_title("Carbon dioxide")
    ax2.set_xlabel("Time (years)")
    ax2.set_ylabel("Concentration (ppm)")
    ax2.plot(time, glob['CO2'], cs['x'])

    ax3.set_title("Heat transport")
    ax3.set_xlabel("Time (years)")
    ax3.set_ylabel("Power ($10^{15}W$)")
    ax3.plot(time, (glob['Fa'] * np.pi*RADIUS**2) / PW, color=cs['x'])

    ax4.set_title("Change in heat content")
    ax4.set_xlabel("Time (years)")
    ax4.set_ylabel("Energy ($10^9 Jm^{-2}$)")
    ax4.plot(time, (hc1-hc1[0]) / SV, color=cs['T'], label="Trop.")
    ax4.plot(time, (hc2-hc2[0]) / SV, color=cs['ET'], label="E-Trop.")
    ax4.legend(loc=4)
    
    fig.tight_layout(rect=[0,0.03,1,0.95])

    return fig


def all_figs(box1, box2, glob):
    """ Just run all plotting functions and return all the figures """
    
    # Initialise list to hold figures
    fig_list = []

    fig_list.append( temperatures(box1, box2, glob) )
    fig_list.append( transport(box1, box2, glob) )
    fig_list.append( hydro(box1, box2, glob) )
    fig_list.append( fluxes(box1, box2, glob) )
    fig_list.append( energy(box1, box2, glob) )
    fig_list.append( carbon_dioxide(box1, box2, glob) )
    fig_list.append( ocean(box1, box2, glob) )
    fig_list.append( atmosphere(box1, box2, glob) )

    return fig_list
    
def save_figs(fig_list, loc):    
    """ Save all figures to one pdf.
        Assumes 'loc' exists, which should always be the case """
    
    save_pdf = mpl_pdf.PdfPages(loc+"figures.pdf")
        
    for fig in fig_list:
        save_pdf.savefig(fig)

    save_pdf.close()

    return

########################
##  Script execution  ##
########################

def auto(box1, box2, glob):
    """ Called from main.py. Plots the simulation that's just run """
    
    fig_list = all_figs(box1, box2, glob)

    save_figs(fig_list, save_loc)

    return

# If running as a command-line script
if __name__ == '__main__':
    
    # Create dictionary with argv strings as keys and plotting funcs as values
    plot_dict = {
                'temps': temperatures,
                'transport': transport,
                'hydro': hydro,
                'flux': fluxes,
                'energy': energy,
                'co2': carbon_dioxide,
                'ocean': ocean,
                'atmos': atmosphere
                }
    
    # Check if save location specified as argv[1]
    if argv[1] not in plot_dict.keys() and \
            argv[1] not in ('all', 'save'):
        loc = argv[1]
        if loc[-1] != '/': loc = loc + '/'
    else:
        loc = ""
    
    # Load data
    box1, box2, glob = load_data(loc)
    
    # Plot figures
    if 'all' in argv:
        fig_list = all_figs(box1, box2, glob)
    
    else:
        fig_list = []
        
        # Plot according to argument variables
        for key in plot_dict.keys():
            if key in argv:
            
                # Add figure to list
                fig_list.append( plot_dict[key](box1, box2, glob) )

    
    if 'save' in argv:
        save_figs(fig_list, loc)

    plt.show()


