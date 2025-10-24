## Calorically perfect air CV nozzle simulation

- Considers rocket and propellant mass (dry = 0.6 * total)
- will let you know if your proposed nozzle geometry is garbage (does not accept shock waves)
- long time ago hobby project for a friend's aerospace course (no warranty, express or implied)

### Setup / installation

REQUIRES PYTHON 3.13  

1. Make sure build tools are upgraded `pip install --upgrade pip setuptools wheel`
2. `pip install -r requirements.txt`
3. Original dependency gas_dynamics requires incompatible numpy version, so we build it from this fork instead, 
   which has removed the dependency version constraints from gas_dynamics.  
   Note that this might break some stuff but for our usage it seems to work.  
   `pip install git+https://github.com/SamuelHelbling/gas_dynamics.git`

#### Extra notes:
- numpy and matplotlib are required by gas_dynamics and my code  
- scipy is just required by gas_dynamics

### Usage
Run: `python calculate.py [A*] [A/A*] [initial mass] [0 | 1]`
Last 0 or 1 param specifies if the following graphs are generated:
- `Acceleration = f(t)`
- `Velocity = f(t)`
- `Height = f(t)`
- `Thrust = f(t)`
- `Drag = f(t)`

#### Usage tips
- For small-scale supersonic nozzles, area ratios are often `2–10`. For rocket engines, ratios can be up to `50–100`.
- Typical throat areas `0.0003-0.03` for small and lab nozzles, `0.7-12` for large rocket engines.
- Throat area affects mass flow!
- This program considers 60% initial mass as dry mass (hardcoded - but easy to change)

## Explicações beca beca
This script simulates a rocket powered by perfect air (γ=1.4) with the following input parameters:
- Critical Area (= area at throat) [m<sup>2</sup>] -> `A*`
- Area Ratio -> `A/A*`
- Rocket Mass

![img.png](img.png)  
The frontal area considered for drag calculations is equal to the nozzle exit area.

Stagnation pressure (P<sub>0</sub>) and temperature (T<sub>0</sub>) may also be specified by editing the script file.

## Opt.py
Runs several iterations looking for the combination that produces the highest flying rocket.  
At the moment this is ridiculously slow (optimization required xd)  
Tweak the parameter ranges directly in the code  