#!/usr/bin/python3

Consonants = list(range(0x1900, 0x191E + 1))
Matras = list(range(0x1920, 0x1928 + 1))
Subjoined = list(range(0x1929, 0x192B + 1))
Finals = list(range(0x1930, 0x1938 + 1))

consonants = list(map(chr, Consonants))
matras = list(map(chr, Matras))
glides = list(map(chr, Subjoined))
finals = list(map(chr, Finals))
k = kemphreng = chr(0x193A)

ukar = matras[2]
