import csv
import random

with open('chameleon.csv') as csvfile, open('chameleon.dir', 'w') as dirfile:
    reader = csv.reader(csvfile)

    for (col1, col2) in enumerate(reader, start=1):
        x = random.random()
        if col2[0] == col2[1]:
            continue
        if x > 0.6:
            dirfile.write(f'{col2[0]},{col2[1]}\n')
        elif x > 0.2:
            dirfile.write(f'{col2[1]},{col2[0]}\n')
        else:
            dirfile.write(f'{col2[1]},{col2[0]}\n')
            dirfile.write(f'{col2[0]},{col2[1]}\n')