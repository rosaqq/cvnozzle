import gas_dynamics as gd
import numpy as np


def get_exit_mach(area, area_star):
    """
    Applies fsolve to area_ratio to try and get exit_mach
    :return: Mach number at the nozzle exhaust plane
    # todo: only supersonic mach being used here
    """
    return gd.mach_from_area_ratio(area / area_star)[-1]


def get_isen_pressure_ratio(mach: float, gamma: float = 1.4) -> float:
    """
    Returns isentropic pressure ratio for design exit Mach.

    Equation from figure 5.14c, p205, Modern Compressible Flow, J. Anderson

    Original eq: (1 + (gamma - 1)/2 * M^2)^(-gamma/(gamma-1))

    :param mach: Design exit mach
    :param gamma: default 1.4
    :return: Pressure ratio for isentropic flow
    """

    # using 1/base instead of negative exponent
    gm1 = gamma - 1.0
    fac1 = 1.0 + .5 * gm1 * np.power(mach, 2)
    return np.power(1.0 / fac1, gamma / gm1)


def what_is_happening_in_my_nozzle(exit_area, critical_area, stagnation_pressure, ambient_pressure):
    design_mach = get_exit_mach(exit_area, critical_area)
    # print(f'design_mach: {design_mach}')
    isen_exit_pressure = get_isen_pressure_ratio(design_mach) * stagnation_pressure

    print(f'Pamb is: {ambient_pressure}, Pexit isen is: {isen_exit_pressure}')

    # under expanded nozzle, expansion waves at exit
    if ambient_pressure < isen_exit_pressure:
        print('nozzle is underX')

    elif ambient_pressure == isen_exit_pressure:
        print('Design condition!')

    # oblique waves at exit
    elif ambient_pressure > isen_exit_pressure:
        print('nozzle is overX')
        # if ambient pressure >>> isen exit pressure normal shock waves will form inside nozzle

