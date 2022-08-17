---
title: Namdhinggo - Character Set Support
fontversion: 3.001
---

Namdhinggo supports the Limbu script, the double danda from Devanagari, and a basic set of Latin characters.
Inclusion of a basic Latin repertoire is provided as a convenience, e.g., for use in menus or for displaying markup in text files.
These fonts are not intended for extensive Latin script use.

## Supported characters

The following character ranges are supported by this font:

Unicode block | Namdhinggo support
------------- | ------------------
C0 Controls and Basic Latin|U+0020..U+007E
C1 Controls and Latin-1 Supplement|U+00A0..U+00FF
Devanagari|U+0965 DEVANAGARI DOUBLE DANDA
Limbu (complete)|U+1900..U+194F
General Punctuation|U+2009, 200B, U+2013, U+2014, U+2018, U+2019, U+201C, U+201D, U+2020..U+2022, U+2026, U+2039, U+203A, U+2060
Geometric Shapes|U+25CC

The Devanagari "bit" is set in this font to prevent unwarranted font switching when U+0965 DEVANAGARI DOUBLE DANDA is used.
However, U+0965 is the only character from the Devanagari block in this font.
