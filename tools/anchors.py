#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'Copy anchors for {ufo}')

# Modify UFO

# The last two consonants, U+191D and U+191E, already have the needed APs.
for codepoint in list(range(0x1900, 0x191C + 1)):
    consonant_name = f'uni{codepoint:X}'
    consonant = font[consonant_name]
    for anchor in consonant.anchors:
        if anchor.name == 'K':

            # consonant + Ukar
            consonant_u_name = f'uni{codepoint:X}{0x1922:X}'
            consonant_u = font[consonant_u_name]
            consonant_u.appendAnchor('K', (anchor.x, anchor.y))

            # consonant + Ra + Ukar
            consonant_ra_u_name = f'uni{codepoint:X}{0x192A:X}{0x1922:X}'
            if consonant_ra_u_name in font:
                consonant_ra_u = font[consonant_ra_u_name]
                consonant_ra_u.appendAnchor('K', (anchor.x, anchor.y))

# One AP did not make it over from the old sources for unknown reasons
omatra = font['uni1928']
omatra.appendAnchor('K', (-150, 1455))

# Not sure what the situation is with the need for these APs
umatra = font['uni1922']
ya = font['uni1929']
wa = font['uni192B']
umatra.appendAnchor('_G', (-150, -15))
ya.appendAnchor('G', (-135, -40))
wa.appendAnchor('G', (-135, -40))

# Save UFO
font.changed()
font.save()
font.close()
