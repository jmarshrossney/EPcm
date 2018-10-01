# EPcm

EPcm is a pedagogical climate model intended for use during the undergraduate Environmental Physics course at Imperial College London.
It was originally written in Matlab by [Dr Arnaud Czaja](https://www.imperial.ac.uk/people/a.czaja) (the original code can be found [here](http://www.sp.ph.ic.ac.uk/~aczaja/EP_ClimateModel.html)).

To improve accessibility, it was reformulated in Python by Joe Marsh Rossney in Summer 2016.

## Getting started

### Prerequisites

All you need to run a simulation are the [NumPy and Matplotlib packages](https://www.scipy.org/install.html).

### Installing

Clone the repository using
```
git clone https://github.com/marshrossney/EPcm.git
```
or just download and unzip.

## Instructions for use

### Model documentation

Before you start, have a read of the [model documentation](http://www.sp.ph.ic.ac.uk/~aczaja/EP/EP2009-2010/ModelDocumentation.pdf).
It describes the model variables, equations, diagnostics, parameters and gives some example experiments.

### Choosing simulation parameters

All user-controlled parameters are found in `params.py` along with a short description of what they do.
The unaltered `params.py` file relates to the control run described in the model documentation.

### Running a simulation

To run a simulation just type
```
python main.py
```
The simulation will most likely complete in a few seconds, unless you're using a very small timestep and/or large final time (for `dt =` 1 day and `nyr =` 100 years it should take 3 or so seconds).

After the simulation has finished, the time-series data and a pdf file containing all of the plots will be saved to the directory given by `save_loc` in `params.py`.

The time-series data will be saved as arrays to three files - `box1.out`, `box2.out` and `glob.out` - corresponding to the *tropical* and *extra-tropical* boxes, and 'global' data related to both boxes.

### Plotting the results

The easiest way to view the results is to open the pdf file `figures.pdf` saved at the end of a simulation.
However, it is possible to re-run the plot script from the command line:
```
python plot.py arg1 arg2 arg3 ...
```
If you want to plot data which is saved in a different directory from the `plot.py`, then the **first** command-line argument `arg1` should be the relative path to that directory, e.g. `control/`.

If you want to save the resulting plots to a pdf (in the same directory as the data files), then one of the other command line arguments should be `save`.

Any remaining command-line arguments `argN argM ...` may specify which data you would like to view.
Possible options are:
* `temps`       -      Tropical & extra-tropical temperatures
* `transport`   -      Heat & moisture transport & circulation
* `hydro`       -      Hydrological cycle
* `flux`        -      Vertical radiation & heat fluxes
* `energy`      -      Energy & heat content
* `co2`         -      Carbon dioxide concentration & global temperatures
* `ocean`       -      Temperatures, heat content and transport in the ocean
* `atmos`       -      Temperatures, CO2, heat content and transport in the atmosphere
* `all`         -      Plot all of the above

So, if you wanted to just look at the hydrological cycle and CO2 concentration using data saved in the working directory (where `plot.py` is), you'd run
```
python plot.py hydro co2
```

If you accidentally deleted the figures from a previous run saved to `co2_doubling/tau_10years/`, and you wanted to recreate that pdf, you'd run
```
python plot.py co2_doubling/tau_10years/ save all
```

## Example plots

(Miniaturised) plots obtained using 'control' starting temperatures, but with water vapour feedback and carbon dioxide increasing over a timescale of 100 years.

![](/example_figs/temps.png) ![](/example_figs/flux.png)
![](/example_figs/hydro.png) ![](/example_figs/co2.png)


