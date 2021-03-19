#!/usr/bin/python3

from ranges import *
import sys


with open(sys.argv[1], 'w') as output:

    output.write('Consonants with vowels or Kemphreng\n')
    for c in consonants:
        clusters = list()
        for m in matras + [k]:
            cluster = c + m
            clusters.append(cluster)
        line = ' '.join(clusters)
        output.write(line + '\n')

    output.write('Consonants with vowels and kemphreng\n')
    for c in consonants:
        clusters = list()
        for m in matras:
            cluster = c + m + k
            clusters.append(cluster)
        line = ' '.join(clusters)
        output.write(line + '\n')

    output.write('Consonants with glide + Ukar + Kemphreng\n')
    for c in consonants:
        clusters = list()
        for g in glides:
            cluster = c + g + ukar + k
            clusters.append(cluster)
        line = ' '.join(clusters)
        output.write(line + '\n')

    output.write('Consonants with Vowels + (Kemphreng) + small final\n')
    for c in consonants:
        clusters = list()
        for m in matras:
            for f in finals:
                cluster = c + m + f + c + m + k + f
                clusters.append(cluster)
        line = ' '.join(clusters)
        output.write(line + '\n')
