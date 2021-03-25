import matplotlib
import matplotlib.pyplot as plt

from flow import *
from rocket import Rocket

plt_count = 0


def main(args=None):
    matplotlib.use('tkagg')

    if args is None:
        args = ['', 0.1562, 1.3673, 6000]

    tmin = 0
    tmax = 200
    steps = 200

    # Problem inputs

    # a / a* -> ex / crit
    critical_area = float(args[1])
    a_ratio = float(args[2])

    stagnation_pressure = 7e6
    stagnation_temperature = 2500
    initial_mass = float(args[3])

    def plot(data, label):
        global plt_count
        plt.figure(plt_count)
        plt.plot(np.linspace(tmin, tmax, steps), data, label=label)
        plt.legend()
        plt_count += 1

    rocket = Rocket(stagnation_pressure, stagnation_temperature, critical_area, a_ratio, initial_mass)
    rocket.launch(tmin, tmax, steps)

    plot(rocket.accel_data, 'accel')
    plot(rocket.vel_data, 'vel')
    plot(rocket.height_data, 'height')
    plot(rocket.thrust_data, 'thrust')
    plot(rocket.drag_data, 'drag')
    plt.show()

    # print(f'top height: {top_height}, reached at t = {x[height_data.index(top_height)]}')
    return rocket.top_height


if __name__ == '__main__':
    # print(main(sys.argv))
    print(main())
