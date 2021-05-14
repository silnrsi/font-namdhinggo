#!/usr/bin/python3
# this is a smith configuration file

# set the font name, version, licensing and description
APPNAME = "NamdhinggoSIL"
FAMILY = APPNAME

# Get version and authorship info from Regular UFO
# must be first function call:
getufoinfo('source/' + FAMILY  + '-Regular.ufo')
# BUILDLABEL = 'beta1'

# Set up the FTML tests
ftmlTest('tools/ftml-smith.xsl')

genout = 'generated/'

designspace('source/' + FAMILY + '.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            opentype = fea(genout + '${DS:FILENAME_BASE}.fea',
                mapfile = genout + '${DS:FILENAME_BASE}.map',
                master = 'source/master.feax',
                make_params = '',
                params = '',
                ),
            script = ['DFLT'],
            woff = woff('woff/${DS:FILENAME_BASE}',
                metadata = '../source/${DS:FAMILYNAME_NOSPC}-WOFF-metadata.xml'),
            version = VERSION,
            pdf = fret(params='-oi')
            )
