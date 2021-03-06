#!/usr/bin/python3
# this is a smith configuration file

# set the font name, version, licensing and description
APPNAME = "NamdhinggoSIL"
FAMILY = APPNAME

# Get version and authorship info from Regular UFO
# must be first function call:
getufoinfo('source/masters/' + FAMILY  + 'Master-Regular.ufo')
# BUILDLABEL = 'beta1'

# Set up the FTML tests
ftmlTest('tools/ftml-smith.xsl')

genout = 'generated/'

designspace('source/' + FAMILY + '.designspace',
            target = process("${DS:FILENAME_BASE}.ttf",
                cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['${DS:FILE}'])
            ),
            instanceparams = '-W',
            opentype = fea(genout + '${DS:FILENAME_BASE}.fea',
                mapfile = genout + '${DS:FILENAME_BASE}.map',
                master = 'source/master.feax',
                make_params = '',
                params = '',
                ),
            version = VERSION,
            woff = woff('woff/${DS:FILENAME_BASE}',
                metadata = f'../source/{FAMILY}-WOFF-metadata.xml'),
            script = ['DFLT'],
            pdf = fret(params='-oi')
            )
