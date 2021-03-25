import matplotlib
import matplotlib.pyplot as plt
import sys

from flow import *
from rocket import Rocket

plt_count = 0


def main(args):
    matplotlib.use('tkagg')

    if len(args) < 4:
        args = ['', 0.1562, 1.3673, 6000]

    # Problem inputs
    stagnation_pressure = 7e6
    stagnation_temperature = 2500

    # a / a* -> ex / crit
    critical_area = float(args[1])
    a_ratio = float(args[2])

    initial_mass = float(args[3])

    # params for height plot calculation
    tmin = 0
    tmax = 200
    steps = 200

    def plot(data, label):
        global plt_count
        plt.figure(plt_count)
        plt.plot(np.linspace(tmin, tmax, steps), data, label=label)
        plt.legend()
        plt_count += 1

    rocket = Rocket(stagnation_pressure, stagnation_temperature, critical_area, a_ratio, initial_mass)
    rocket.launch(tmin, tmax, steps)

    # plot(rocket.accel_data, 'accel')
    # plot(rocket.vel_data, 'vel')
    # plot(rocket.height_data, 'height')
    # plot(rocket.thrust_data, 'thrust')
    # plot(rocket.drag_data, 'drag')
    # plt.show()

    return rocket.top_height


if __name__ == '__main__':
    print(main(sys.argv))
