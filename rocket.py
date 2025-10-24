from atm import *
from flow import *


class Rocket:

    def __init__(self, stagnation_pressure, stagnation_temperature, critical_area, area_ratio, initial_mass):
        self.stagnation_pressure = stagnation_pressure
        self.stagnation_temperature = stagnation_temperature
        self.critical_area = critical_area
        self.area_ratio = area_ratio
        self.exit_area = critical_area * area_ratio
        self.initial_mass = initial_mass

        # constants
        self.gamma = 1.4
        self.g = 9.8

        self.current_accel = 0
        self.current_vel = 0
        self.current_height = 0
        self.top_height = 0

        self.accel_data = []
        self.vel_data = []
        self.height_data = []
        self.thrust_data = []
        self.drag_data = []

    def mass_flux(self, time):
        # m_flow is constant for a specified nozzle geometry
        # m_flow depends on throat_area
        flux = gd.mass_flux_max(self.stagnation_pressure, self.stagnation_temperature) * self.critical_area

        if flux * time >= 0.6 * self.initial_mass:
            return 0
        return flux

    def drag(self, height, velocity):
        a2 = self.exit_area
        rho = get_ambient_density(height)
        airspeed = np.abs(velocity)
        mach = airspeed / gd.sonic_velocity(temperature=get_ambient_temperature(height))

        coef_d = -3e-6 * np.power(mach, 6) + 0.0002 * np.power(mach, 5) - 0.0046 * np.power(mach, 4) + 0.053 * \
            np.power(mach, 3) - 0.2806 * np.power(mach, 2) + 0.6211 * mach + 0.0568

        return rho * np.power(airspeed, 2) * coef_d * a2 / 2

    def thrust(self, t, height):
        exit_mach = get_exit_mach(self.exit_area, self.critical_area)
        mass_flow = self.mass_flux(t)
        gamma = self.gamma

        exit_pressure = self.stagnation_pressure * np.power(1 + (gamma - 1) / 2 * np.power(exit_mach, 2),
                                                            -gamma / (gamma - 1))

        ambient_pressure = get_ambient_pressure(height)

        v_exit = get_v_exit(self.exit_area, self.critical_area, self.stagnation_temperature, self.stagnation_pressure,
                            ambient_pressure, gamma)
        if v_exit < 0:
            print('Shock inside, aborting')
            exit()

        if mass_flow == 0:
            return 0
        return mass_flow * v_exit + exit_pressure * self.exit_area - ambient_pressure * self.exit_area

    def get_accel(self, t, height, vel):
        if self.mass_flux(t) > 0:
            mass = self.initial_mass - self.mass_flux(t) * t
        else:
            mass = 0.6*self.initial_mass

        th = self.thrust(t, height)
        self.thrust_data.append(th)
        dg = self.drag(height, vel)
        self.drag_data.append(dg)

        m = mass

        # print(f'thrust: {th}, drag: {dg}, mass: {m}')
        return (th - dg) / m - self.g

    def launch(self, tmin, tmax, steps):
        x = np.linspace(tmin, tmax, steps)
        prev_ts = 0
        for t in x:

            # accel instant
            self.current_accel = self.get_accel(t, self.current_height, self.current_vel)

            dv = self.current_accel * (t - prev_ts)
            self.current_vel += dv

            dh = self.current_vel * (t - prev_ts)
            self.current_height += dh

            if self.current_height < 0:
                self.current_accel = 0
                self.current_vel = 0
                self.current_height = 0

            self.accel_data.append(self.current_accel)
            self.vel_data.append(self.current_vel)
            self.height_data.append(self.current_height)

            if self.current_height > self.top_height:
                self.top_height = self.current_height

            prev_ts = t
