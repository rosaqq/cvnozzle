import calculate
import numpy as np
import csv
import sys

mass_range = np.linspace(1000, 10000, 50)
ac_range = np.linspace(0.005, 0.2, 50)
ar_range = np.linspace(1, 7, 50)
best_rocket = {'h': 0.}
#
# with open('data.csv', 'w', newline='') as file:
#     writer = csv.writer(file, delimiter=',')
#     writer.writerow(['mass', 'ac', 'ar', 'top_height', 'time'])
for m in mass_range:
    print(f'\nmass: {m}')
    for ac in ac_range:
        sys.stdout.write(f'\tac: {np.where(np.isclose(ac_range, ac))[0]}/{len(ac_range) - 1} Ar.\r')
        sys.stdout.flush()
        ac = round(ac, 4)
        for ar in ar_range:
            ar = round(ar, 4)
            th = calculate.main(['', ac, ar, m, 0])
            # writer.writerow([m, ac, ar, th, t])
            # print(f'\t\tar: {ar} -> {th, t}')
            if th > best_rocket['h']:
                best_rocket['h'] = th
                best_rocket['m'] = m
                best_rocket['ac'] = ac
                best_rocket['ar'] = ar

print(best_rocket)
