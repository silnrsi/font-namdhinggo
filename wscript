#!/usr/bin/python3
# this is a smith configuration file

# set the font name, version, licensing and description
APPNAME = "NamdhinggoSIL"
FAMILY = APPNAME
DESC_SHORT = "Unicode font for the Limbu writing system of Nepal"

# Get version and authorship info from Regular UFO
# must be first function call:
getufoinfo('source/NamdhinggoSIL-Regular.ufo')
# BUILDLABEL = 'beta1'

# Set up the FTML tests
ftmlTest('tools/ftml-smith.xsl')

fontfamily = APPNAME

generated = 'generated/'

designspace('source/NamdhinggoSIL.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
                mapfile = generated + '${DS:FILENAME_BASE}.map',
                master = 'source/master.feax',
                make_params = '',
                params = '',
                ),
            script = ['latn', 'limb'],
            woff = woff('woff/${DS:FILENAME_BASE}',
                metadata = '../source/${DS:FAMILYNAME_NOSPC}-WOFF-metadata.xml'),
            pdf = fret(params='-oi')
            )
