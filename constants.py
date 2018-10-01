import math as m

# ------- #
#  Units  #
# ------- #
KM = 1000.
PW = 1.e15
DAY = 24*3600
MONTH = 30*DAY
YEAR = 12*MONTH
MB = 100.           # millibar (100 Pa)
SV = 1.e09          # Sverdrup - mass transport unit (kg/s)

# ---------------------------------- #
#  Planetary and Physical constants  #
# ---------------------------------- #
RADIUS = 6371*KM    # Earth radius (km)
GRAVI = 9.81        # Earth gravity (m s-2)
SIGMA = 5.67*1.e-08 # Stefan Boltzmann const. (W m-2 K-4)
S0 = 1367.          # Solar const. (W m-2)
ALPHAp = .3         # Planetary albedo (non dim.)

# ------- #
#  Ocean  #
# ------- #
RHO = 1000.         # Density of water (kg m-3)
CPO = 4000.         # Specific heat capacity of water (J kg-1 m-2)
HM = 50.            # Mixed layer thickness (m)
HO = 500.           # Thermocline thickness (m)
HCM = RHO*CPO*HM    # Heat capacity of mixed layer (J K-1 m-2)
HCO = RHO*CPO*HO    # Heat capacity of thermocline (J K-1 m-2) 

# ------------ #
#  Atmosphere  #
# ------------ #
PA = 750.           # Low level pressure (mb)
RHA = 0.6           # Relative humidity at PA
CPA = 1000.         # Specific heat capacity of dry air (J kg-1 K-1)
CAHEAT = 2*CPA      # Pseudo-heat capacity (to include moisture effects)
PATM = 1000*MB      # Surface atm. pressure (Pa)
LV = 2.5*1.e06      # Latent heat of vaporisation (J kg-1)
HCA = CAHEAT*PATM/GRAVI     # Atmospheric heat capacity (J K-1 m-2)

# ---------------------------------------------- #
#  Convective and circulation paramaterisations  #
# ---------------------------------------------- #
DTCRIT_CONV = 40.   # Moist adiabatic lapse rate (K)
PSIFRAC = 0.1       # Ratio PSIo/PSIa of circulation intensity
BIGONE = 100.
KEFF = 100*SV/15    # Linear parameterisation

# ----------- #
#  Radiation  #
# ----------- #
TEMI  = ( S0*(1-ALPHAp) / (4*SIGMA) )**.25   # Global mean emission temp (K)
TEMI1 = ( ( S0*(1-ALPHAp) * (m.pi/3+0.5*m.sqrt(3.0)) ) / \
                   ( 2*m.pi*SIGMA) )**.25            # Box1 emission temp (K)
TEMI2 = ( ( S0*(1-ALPHAp) * (2*m.pi/3-0.5*m.sqrt(3.0)) ) / \
                   ( 2*m.pi*SIGMA) )**.25            # Box2 emission temp (K)
GAMMA = 1.25    # Factor for H2O emissivity calc. (non dim.) (see Emanuel, 2002)
ALPHA = .0012   # Factor for CO2 emissivity calc. (non dim.) (see Emanuel, 2002)



