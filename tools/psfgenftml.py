#!/usr/bin/python3
'generate ftml tests from glyph_data.csv and UFO'
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018,2021 SIL International  (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Bob Hallissy'

import re
from silfont.core import execute
import silfont.ftml_builder as FB
from palaso.unicode.ucd import get_ucd

argspec = [
    ('ifont', {'help': 'Input UFO'}, {'type': 'infont'}),
    ('output', {'help': 'Output file ftml in XML format', 'nargs': '?'}, {'type': 'outfile', 'def': '_out.ftml'}),
    ('-i','--input', {'help': 'Glyph info csv file'}, {'type': 'incsv', 'def': 'glyph_data.csv'}),
    ('-f','--fontcode', {'help': 'letter to filter for glyph_data'},{}),
    ('-l','--log', {'help': 'Set log file name'}, {'type': 'outfile', 'def': '_ftml.log'}),
    ('--langs', {'help':'List of bcp47 language tags', 'default': None}, {}),
    ('--rtl', {'help': 'enable right-to-left features', 'action': 'store_true'}, {}),
    ('--norendercheck', {'help': 'do not include the RenderingUnknown check', 'action': 'store_true'}, {}),
    ('-t', '--test', {'help': 'name of the test to generate', 'default': None}, {}),
    ('-s','--fontsrc', {'help': 'font source: "url()" or "local()" optionally followed by "=label"', 'action': 'append'}, {}),
    ('--scale', {'help': 'percentage to scale rendered text (default 100)'}, {}),
    ('--ap', {'help': 'regular expression describing APs to examine', 'default': '.'}, {}),
    ('-w', '--width', {'help': 'total width of all <string> column (default automatic)'}, {}),
    ('--xsl', {'help': 'XSL stylesheet to use'}, {}),
]


def doit(args):
    logger = args.logger

    # Read input csv
    builder = FB.FTMLBuilder(logger, incsv=args.input, fontcode=args.fontcode, font=args.ifont, ap=args.ap,
                             rtlenable=args.rtl, langs=args.langs)

    # Override default base (25CC) for displaying combining marks:
    builder.diacBase = 0x1901   # ka

    # Specify block of primary script
    block = range(0x1900, 0x194F+1)

    # Useful ranges of codepoints
    uids = sorted(builder.uids())
    consonants = [uid for uid in uids if builder.char(uid).general == 'Lo' and uid in block]
    matras = [uid for uid in uids if 'VOWEL SIGN' in get_ucd(uid, 'na')]
    glides = [uid for uid in uids if 'SUBJOINED' in get_ucd(uid, 'na')]
    finals = [uid for uid in uids if 'LIMBU SMALL' in get_ucd(uid, 'na')]
    digits = [uid for uid in uids if builder.char(uid).general == 'Nd' and uid in block]

    k = 0x193A  # Kemphreng
    ukar = matras[2]

    # Initialize FTML document:
    # Default name for test: AllChars or something based on the csvdata file:
    test = args.test or 'AllChars (NG)'
    widths = None
    if args.width:
        try:
            width, units = re.match(r'(\d+)(.*)$', args.width).groups()
            if len(args.fontsrc):
                width = int(round(int(width)/len(args.fontsrc)))
            widths = {'string': f'{width}{units}'}
            logger.log(f'width: {args.width} --> {widths["string"]}', 'I')
        except:
            logger.log(f'Unable to parse width argument "{args.width}"', 'W')
    # split labels from fontsource parameter
    fontsrc = []
    labels = []
    for sl in args.fontsrc:
        try:
            s, l = sl.split('=',1)
            fontsrc.append(s)
            labels.append(l)
        except ValueError:
            fontsrc.append(sl)
            labels.append(None)
    ftml = FB.FTML(test, logger, rendercheck=not args.norendercheck, fontscale=args.scale,
                   widths=widths, xslfn=args.xsl, fontsrc=fontsrc, fontlabel=labels, defaultrtl=args.rtl)

    if test.lower().startswith("allchars"):
        # all chars that should be in the font:
        ftml.startTestGroup('Encoded characters')
        for uid in uids:
            if uid < 32: continue
            c = builder.char(uid)
            # iterate over all permutations of feature settings that might affect this character:
            for featlist in builder.permuteFeatures(uids = (uid,)):
                ftml.setFeatures(featlist)
                builder.render((uid,), ftml)
                # Don't close test -- collect consecutive encoded chars in a single row
            ftml.clearFeatures()
            for langID in sorted(c.langs):
                ftml.setLang(langID)
                builder.render((uid,), ftml)
            ftml.clearLang()

        # Add unencoded specials and ligatures -- i.e., things with a sequence of USVs in the glyph_data:
        ftml.startTestGroup('Specials & ligatures from glyph_data')
        for basename in builder.specials():
            special = builder.special(basename)
            # iterate over all permutations of feature settings that might affect this special
            for featlist in builder.permuteFeatures(uids = special.uids):
                ftml.setFeatures(featlist)
                builder.render(special.uids, ftml)
                # close test so each special is on its own row:
                ftml.closeTest()
            ftml.clearFeatures()
            if len(special.langs):
                for langID in sorted(special.langs):
                    ftml.setLang(langID)
                    builder.render(special.uids, ftml)
                    ftml.closeTest()
                ftml.clearLang()

        # Characters used to create SILE test data
        ftml.startTestGroup('Proof')
        for uid in consonants:
            builder.render((uid,), ftml)
        ftml.closeTest()
        for uid in matras:
            builder.render((uid,), ftml)
        ftml.closeTest()
        for uid in glides:
            builder.render((uid,), ftml)
        ftml.closeTest()
        for uid in digits:
            builder.render((uid,), ftml)
        ftml.closeTest()

    if test.lower().startswith("diac"):
        # Diac attachment:

        # Representative base and diac chars:
        repDiac = list(filter(lambda x: x in builder.uids(), (0x193A, 0x1939, 0x193B)))
        repBase = list(filter(lambda x: x in builder.uids(), (0x1901, 0x1900, 0x191D, 0x191E)))

        ftml.startTestGroup('Representative diacritics on all bases that take diacritics')
        for uid in uids:
            # ignore bases outside of the primary script:
            if uid not in block: continue
            c = builder.char(uid)
            # Always process Lo, but others only if that take marks:
            if c.general == 'Lo' or c.isBase:
                for diac in repDiac:
                    for featlist in builder.permuteFeatures(uids = (uid,diac)):
                        ftml.setFeatures(featlist)
                        # Don't automatically separate connecting or mirrored forms into separate lines:
                        builder.render((uid,diac), ftml, addBreaks = False)
                    ftml.clearFeatures()
                ftml.closeTest()

        ftml.startTestGroup('All diacritics on representative bases')
        for uid in uids:
            # ignore marks outside of the primary script:
            if uid not in block: continue
            c = builder.char(uid)
            if c.general == 'Mn':
                for base in repBase:
                    for featlist in builder.permuteFeatures(uids = (uid,base)):
                        ftml.setFeatures(featlist)
                        builder.render((base,uid), ftml, keyUID = uid, addBreaks = False)
                    ftml.clearFeatures()
                ftml.closeTest()

    if test.lower().startswith("matras"):
        # Combinations with matras:

        ftml.startTestGroup('Consonants with vowels or Kemphreng')
        for c in consonants:
            for m in matras + [k]:
                builder.render((c,m), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonants with vowels and kemphreng')
        for c in consonants:
            for m in matras:
                builder.render((c,m,k), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonants with glide + Ukar + Kemphreng')
        for c in consonants:
            for g in glides:
                builder.render((c,g,ukar,k), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonants with Vowels + (Kemphreng) + small final')
        for c in consonants:
            for m in matras:
                for f in finals:
                    builder.render((c,m,f,c,m,k,f), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

    # Write the output ftml file
    ftml.writeFile(args.output)


def cmd() : execute("UFO",doit,argspec)
if __name__ == "__main__": cmd()
