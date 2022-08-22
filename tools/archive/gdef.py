#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
ikar = 0x1921
mukphreng = 0x1939
limbu = [ikar, mukphreng]

cgj = 0x034F
vs = range(0xFE00, 0xFE0F+1)
mn = [cgj] + list(vs)

pivot = [
    'eekar_kemphreng-limb',
    'aikar_kemphreng-limb',
    'subya_kemphreng-limb',
    'subwa_kemphreng-limb',
    'subya_akar_kemphreng-limb',
    'subya_ukar_kemphreng-limb',
    'subya_ekar_kemphreng-limb',
    'subya_okar_kemphreng-limb',
    'subya_akar-limb',
    'subya_ukar-limb',
    'subya_ekar-limb',
    'subya_okar-limb',
    'subwa_akar_kemphreng-limb',
    'subwa_ukar_kemphreng-limb',
    'subwa_ekar_kemphreng-limb',
    'subwa_okar_kemphreng-limb',
    'subwa_akar-limb',
    'subwa_ukar-limb',
    'subwa_ekar-limb',
    'subwa_okar-limb',
]

for glyph in font:
    # if glyph.unicode in mn:
    #     glyph.appendAnchor('_none', (0, 0))
    if glyph.name in pivot: # or glyph.unicode in limbu:
        glyph.width = 0
        # glyph.clearAnchors()


# Save UFO
font.changed()
font.save()
font.close()
