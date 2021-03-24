import matplotlib
import matplotlib.pyplot as plt
import sys

from atm import *
from flow import *

plt_count = 0


def main(args):
    matplotlib.use('tkagg')

    gamma = 1.4
    g = 9.8
    tmin = 0
    tmax = 200
    steps = 100

    # Problem inputs

    # a / a* -> ex / crit
    critical_area = float(args[1])
    a_ratio = float(args[2])
    exit_area = critical_area * a_ratio

    stagnation_pressure = 7e6
    stagnation_temperature = 2500
    initial_mass = float(args[3])

    # atmospheric formulas
    sea_level_pressure = 101325  # Pa -> N/m^2

    def plot(data, label):
        global plt_count
        plt.figure(plt_count)
        plt.plot(x[:len(data)], data, label=label)
        plt.legend()
        plt_count += 1

    def fill_zeros(array_in):
        """
        Fills data array to match time array for plotting
        :param array_in:
        :return:
        """

        return np.pad(array_in, (0, steps - len(array_in)), constant_values=0)

    # #######################
    # ### Calc Functions  ###
    # #######################

    # ------ Rocket Functions # todo: rocket class
    # ----------------------------------------------------------------------------------------------------------------------
    def mass_flux(time):
        # m_flow is constant for a specified nozzle geometry
        # m_flow depends on throat_area
        flux = gd.mass_flux_max(stagnation_pressure, stagnation_temperature) * critical_area
        # kg/m^2

        if flux * time >= 0.6 * initial_mass:
            return 0
        return flux

    def drag(height, velocity):
        a2 = exit_area
        rho = get_ambient_density(height)
        airspeed = np.abs(velocity)
        mach = airspeed / gd.sonic_velocity(temperature=get_ambient_temperature(height))
        coef_d = -3e-6 * np.power(mach, 6) + 0.0002 * np.power(mach, 5) - 0.0046 * np.power(mach, 4) + 0.053 * \
                 np.power(mach, 3) - 0.2806 * np.power(mach, 2) + 0.6211 * mach + 0.0568

        return rho * np.power(airspeed, 2) * coef_d * a2 / 2

    def thrust(height):
        exit_mach = get_exit_mach(exit_area, critical_area)
        mass_flow = mass_flux(t)
        exit_pressure = stagnation_pressure * np.power(1 + (gamma - 1) / 2 * np.power(exit_mach, 2),
                                                       -gamma / (gamma - 1))

        ambient_pressure = get_ambient_pressure(height)

        v_exit = get_v_exit(exit_area, critical_area, stagnation_temperature, stagnation_pressure, ambient_pressure,
                            gamma)
        if v_exit < 0:
            print('shock inside, aborting')
            return 0
        pressure_ratio_data.append(ambient_pressure / stagnation_pressure)

        if mass_flow == 0:
            return 0
        return mass_flow * v_exit + exit_pressure * exit_area - ambient_pressure * exit_area

    def get_accel(height, vel, mass):
        th = thrust(height)
        thrust_data.append(th)
        dg = drag(height, vel)
        m = mass

        # print(f'thrust: {th}, drag: {dg}, mass: {m}')
        return (th - dg) / m - g

    x = np.linspace(tmin, tmax, steps)
    current_velocity = 0
    current_height = 0

    accel_data = []
    vel_data = []
    height_data = []
    top_height = 0

    pressure_ratio_data = []
    thrust_data = []

    prev_ts = 0

    current_mass = initial_mass

    for t in x:
        if mass_flux(t) > 0:
            current_mass = initial_mass - mass_flux(t) * t
            # else current mass keeps def

        # accel instant
        accel = get_accel(current_height, current_velocity, current_mass)
        # print(accel)
        dv = accel * (t - prev_ts)
        current_velocity += dv

        if current_velocity < 0:
            # print('starting to fall, stopping simulation')
            top_height = current_height
            break

        dh = current_velocity * (t - prev_ts)
        current_height += dh

        # if current_height < 0:
        #     current_height = 0
        #     accel = 0
        #     current_velocity = 0

        accel_data.append(accel)
        # print(f'accel_data: {accel_data}, curr_accel: {accel}')
        vel_data.append(current_velocity)
        # print(f' vel_data: {vel_data}, curr_vel: {current_velocity}')
        height_data.append(current_height)
        # print(f' height_data: {height_data}, curr_height: {current_height}')

        prev_ts = t

    # plot(fill_zeros(accel_data), 'accel')
    # plot(fill_zeros(vel_data), 'vel')
    # plot(fill_zeros(height_data), 'height')
    # plot(fill_zeros(thrust_data), 'thrust')

    # plot(accel_data, 'accel')
    # plot(vel_data, 'vel')
    # plot(height_data, 'height')
    # plot(thrust_data, 'thrust')
    # plt.show()

    # print(f'top height: {top_height}, reached at t = {x[height_data.index(top_height)]}')
    return top_height, x[height_data.index(top_height)]


if __name__ == '__main__':
    # print(main(sys.argv))
    print(main(['', 0.1562, 1.3673, 5959.183673469387]))
