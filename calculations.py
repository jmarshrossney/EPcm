from params import *
import numpy as np

def CLAUSIUS_CLAPEYRON(Ts, Ta):
    ''' Computes saturation water vapour pressure and saturation specific humidity
        at a given temperature Ts (in K) and pressure PA (in mb).
    
        Saturation water vapour pressure (esat in mb),
        Saturation specific humidity (qsat in kg/kg).

        refs: Physics package of the MIT GCM.'''

    # Average of atmospheric and surface temperatures
    Tsa = 0.5*(Ts + Ta)

    Ts = max(Tsa, 35.0)
    Tc = Tsa - 273.15
    denom = 243.5 + Tc
    eps = 0.62197 # RD/RV
    
    if Tc >= 0:
        # Satu. vap. pressure for liquid water (mb)
        esat = 6.112 * np.exp(17.67 * Tc/denom)
    else:
        # Satu. vap. pressure for ice (mb)
        esat = np.exp(23.33086 - 6111.72784/Ts + 0.15215*np.log(Ts))
    
    # Saturation specific humidity at TS, PS
    qsat = eps * esat/(PA - esat * (1-eps))

    return esat, qsat


def EPSA(esat, qsat, co2):
    ''' Computes emissivity of atmospheric column    
        at average atmos. temperature Ta (K), surface temperature Ts (K),
        CO2 concentration co2 (in ppm), assuming fixed relative humidity. '''

    # Compute (low level) specific humidity
    qa = 1000 * RHA * qsat # in g/kg 
        
    # Compute optical depth
    tauinf = ALPHA*co2 + GAMMA*qa
        
    # Compute emissivity
    epsa = 1 - np.exp(-tauinf)

    return epsa


def PSI(Ts1, Ts2):
    '''Calculates circulation strength of ocean and atmosphere for given SST's.'''

    Psia = KEFF * (Ts1 - Ts2) # kg/s
    Psio = Psia * PSIFRAC # kg/s
    
    return Psia, Psio


def MSE(Ts, Ta, qsat):
    ''' Computes moist static energy at low level.
        Geopotential set to zero.'''

    # Compute (low level) specific humidity
    qa = RHA * qsat # kg/kg
    
    mse = LV*qa + CPA * 0.5*(Ts + Ta)
    
    return mse


def MTSPT(Psia, qsat1, qsat2):
    ''' Computes moisture transport in kg/s.'''

    # Computes (low level) specific humidity
    qa1 = RHA * qsat1 # kg/kg
    qa2 = RHA * qsat2 # kg/kg
    
    # Moisture transport
    MTspt = Psia * (qa1-qa2)

    return MTspt


def FS(Ts, Ta, Te, epsa):
    ''' Calculates surface fluxes.'''

    # Radiative surface flux
    Frad = SIGMA * (Ts**4 - Te**4 - epsa*Ta**4)
    
    # Evaporation
    if Ts-Ta > DTCRIT_CONV:
        Feva = BIGONE * (1 + 0.05*np.random.normal()) * (Ts - Ta - DTCRIT_CONV)
    else: 
        Feva = 0
    
    # Net surface heat flux
    Fs = Frad + Feva
    
    return Fs, Feva


def FT(Ts, Ta, Te, epsa):
    ''' Calculates top-of-atmosphere fluxes.'''
    
    Ft_down = SIGMA * Te**4
    Ft_up = SIGMA * (epsa*Ta**4 + (1-epsa)*Ts**4)
    Ft = Ft_down-Ft_up # >0 downward
    return Ft


def FA(Psia, MSE1, MSE2):
    ''' Calculates atmospheric fluxes.'''
    
    Fa = Psia * (MSE1-MSE2) / (np.pi*RADIUS**2) # W m-2
    return Fa


def FO(Psio, Ts1, To2):
    ''' Calculates oceanic fluxes.'''
    
    Fo = Psio * CPO * (Ts1-To2) / (np.pi*RADIUS**2) # W m-2
    return Fo

