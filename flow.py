import gas_dynamics as gd
import numpy as np

air_gas_constant = 287.05


def get_exit_mach(area, area_star):
    """
    Applies fsolve to area_ratio to try and get exit_mach
    :return: Mach number at the nozzle exhaust plane
    # todo: only supersonic mach being used here
    """
    return gd.mach_from_area_ratio(area / area_star)[-1]


def get_isen_pressure_ratio(mach: float, gamma: float = 1.4) -> float:
    """
    | Returns isentropic pressure ratio for design exit Mach.
    |
    | Equation from figure 5.14c, p205, Modern Compressible Flow, J. Anderson
    | Original eq: (1 + (gamma - 1)/2 * M^2)^(-gamma/(gamma-1))
    | Also NASA: https://www.grc.nasa.gov/www/k-12/rocket/rktthsum.html

    :param mach: Design exit mach
    :param gamma: default 1.4
    :return: Pressure ratio for isentropic flow
    """

    # using 1/base instead of negative exponent
    gm1 = gamma - 1.0
    fac1 = 1.0 + .5 * gm1 * np.power(mach, 2)
    return np.power(1.0 / fac1, gamma / gm1)


def get_isen_temp_ratio(mach: float, gamma: float = 1.4) -> float:
    """
    | Isentropic temperature ratio T_exit / T_stag
    | Nasa: https://www.grc.nasa.gov/www/k-12/rocket/rktthsum.html

    :param mach:
    :param gamma: Default 1.4
    :return: Temperature ratio for isentropic flow
    """

    gm1 = gamma - 1.0
    return 1.0 / (1.0 + .5 * gm1 * np.power(mach, 2))


def normal_shock_p_ratio(mach: float, gamma: float = 1.4) -> float:
    # Eq. 93, static pressure ratio across normal shockwave
    # https://www.nasa.gov/sites/default/files/734673main_Equations-Tables-Charts-CompressibleFlow-Report-1135.pdf
    # Equivalent to equation 3.57, p90, Modern Compressible Flow, J. Anderson

    gm1 = gamma - 1.0
    gp1 = gamma + 1.0
    return (2.0 * gamma * np.power(mach, 2) - gm1) / gp1


def get_v_exit(exit_area, critical_area, stagnation_temperature, stagnation_pressure,
               ambient_pressure, gamma) -> float:
    design_mach = get_exit_mach(exit_area, critical_area)
    # print(f'design_mach: {design_mach}')
    isen_exit_pressure = get_isen_pressure_ratio(design_mach) * stagnation_pressure

    print(f'Pamb is: {ambient_pressure}, Pexit isen is: {isen_exit_pressure}')

    # Basically, flow will be isentropic inside nozzle from underX to overX with shock at exit
    # Isentropic -> design Mach at exit, isen temp eqs., velocity etc, check nasa slides
    # NASA eqs -> https://www.grc.nasa.gov/www/k-12/rocket/rktthsum.html

    # under expanded nozzle, expansion waves at exit
    if ambient_pressure <= isen_exit_pressure:
        if ambient_pressure == isen_exit_pressure:
            print('Design condition!')
        else:
            print('nozzle is underX')

        exit_temp = get_isen_temp_ratio(design_mach) * stagnation_temperature
        exit_velocity = design_mach * np.sqrt(gamma * air_gas_constant * exit_temp)

        return exit_velocity

    # over expanded oblique waves at exit
    elif ambient_pressure > isen_exit_pressure:
        print('nozzle is overX')
        # But just how overX is my flow??

        # if ambient pressure >>> isen exit pressure normal shock waves will form inside nozzle
        pressure_at_shock = isen_exit_pressure * normal_shock_p_ratio(design_mach)
        if ambient_pressure <= pressure_at_shock:
            if ambient_pressure == pressure_at_shock:
                print('Shock at exit!')
            else:
                # shock is pushed outwards
                print('Oblique shock after exit!')
            # Anyway, we got isentropic flow till nozzle exit
            exit_temp = get_isen_temp_ratio(design_mach) * stagnation_temperature
            exit_velocity = design_mach * np.sqrt(gamma * air_gas_constant * exit_temp)

            return exit_velocity
        else:
            # When ambient_pressure > pressure_at_shock
            # Highly over expanded, shockwave inside nozzle
            # So that pressure after shock + divergent pressure increase => ambient_pressure
            print("Shock inside nozzle, don't give me trash nozzles please")
            return 0
