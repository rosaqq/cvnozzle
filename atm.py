import numpy as np


# ------ Atmospheric Model functions
# ----------------------------------------------------------------------------------------------------------------------
def get_ambient_pressure(height: float) -> float:
    """
    Calculates the ambient pressure at a given height
    based on https://en.wikipedia.org/wiki/Barometric_formula#Pressure_equations


    :param height: Height above sea level.
    :return: The ambient pressure at `height`.
    """

    h = height
    h_ref = [0., 11000, 20000, 32000, 47000, 51000, 71000]

    # The atm model works based on layers with different reference values to
    #   plug into our equations. We must find in which layer our height level belongs:
    # Create a list with the values from h_ref and our own height.
    find_b = h_ref + [h]
    # Sort that list in ascending order.
    find_b.sort()
    # Get the index of the value just below our height to find which layer we are on
    b = find_b.index(h) - 1 if find_b.index(h) > 0 else 0

    # Reference pressure values for each layer
    p_ref = [101325.0, 22632.1, 5474.89, 868.02, 110.91, 66.94, 3.96]
    # Reference temperature values for each layer
    t_ref = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65]
    # Reference lapse rate values for each layer
    l_ref = [-0.0065, 0, 0.001, 0.0028, 0, -0.0028, -0.002]

    # The values used for m_ref, g_zero, and r_star are in accordance with the U.S. Standard Atmosphere, 1976,
    # and the value for r_star in particular does not agree with standard values for this constant.
    # Mean molar mass of Earth's air
    m_ref = 0.0289644
    # Gas constant
    r_star = 8.3144598
    # gravitational acceleration
    g_zero = 9.80665

    if l_ref[b] == 0:
        # formula for lapse rate = 0
        pressure = p_ref[b] * np.exp((-g_zero * m_ref * (h - h_ref[b])) / (r_star * t_ref[b]))
    else:
        # formula for lapse rate != 0
        pressure = p_ref[b] * np.power((t_ref[b] + l_ref[b] * (h - h_ref[b])) / t_ref[b],
                                       -(g_zero * m_ref) / (r_star * l_ref[b]))

    return pressure


def get_ambient_density(height: float) -> float:
    """
    Calculates the ambient air density at a given height
    based on https://en.wikipedia.org/wiki/Barometric_formula#Density_equations


    :param height: Height above sea level.
    :return: The ambient density at `height`.
    """

    h = height
    h_ref = [0., 11000, 20000, 32000, 47000, 51000, 71000]

    # The atm model works based on layers with different reference values to
    #   plug into our equations. We must find in which layer our height level belongs:
    # Create a list with the values from h_ref and our own height.
    find_b = h_ref + [h]
    # Sort that list in ascending order.
    find_b.sort()
    # Get the index of the value just below our height to find which layer we are on
    b = find_b.index(h) - 1 if find_b.index(h) > 0 else 0

    # Reference density values for each layer
    rho_ref = [1.2250, 0.36391, 0.08803, 0.01322, 0.00143, 0.00086, 0.000064]
    # Reference temperature values for each layer
    t_ref = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65]
    # Reference lapse rate values for each layer
    l_ref = [-0.0065, 0, 0.001, 0.0028, 0, -0.0028, -0.002]

    # The values used for m_ref, g_zero, and r_star are in accordance with the U.S. Standard Atmosphere, 1976,
    # and the value for r_star in particular does not agree with standard values for this constant.
    # Mean molar mass of Earth's air
    m_ref = 0.0289644
    # Gas constant
    r_star = 8.3144598
    # gravitational acceleration
    g_zero = 9.80665

    if l_ref[b] == 0:
        # formula for lapse rate = 0
        rho = rho_ref[b] * np.exp((-g_zero * m_ref * (h - h_ref[b])) / (r_star * t_ref[b]))
    else:
        # formula for lapse rate != 0
        rho = rho_ref[b] * np.power(t_ref[b] / (t_ref[b] + l_ref[b] * (h - h_ref[b])),
                                    1 + (g_zero * m_ref) / (r_star * l_ref[b]))

    return rho


def get_ambient_temperature(height: float) -> float:
    h = height
    h_ref = [0., 11000, 20000, 32000, 47000, 51000, 71000]

    # The atm model works based on layers with different reference values to
    #   plug into our equations. We must find in which layer our height level belongs:
    # Create a list with the values from h_ref and our own height.
    find_b = h_ref + [h]
    # Sort that list in ascending order.
    find_b.sort()
    # Get the index of the value just below our height to find which layer we are on
    b = find_b.index(h) - 1 if find_b.index(h) > 0 else 0

    # Reference temperature values for each layer
    t_ref = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65]
    # Reference lapse rate values for each layer
    l_ref = [-0.0065, 0, 0.001, 0.0028, 0, -0.0028, -0.002]

    return t_ref[b] + l_ref[b] * (h - h_ref[b])