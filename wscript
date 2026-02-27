#!/usr/bin/python3
# this is a smith configuration file

# command line options
opts = preprocess_args(
    {'opt' : '-r'}, # only build the regular font
    )

# override the default folders
DOCDIR = ['documentation', 'web']
TESTDIR = ['tests', '../font-namdhinggo-private/tests']

# set the font name, version, licensing and description
APPNAME = "Namdhinggo"
FAMILY = APPNAME

# Get version and authorship info from Regular UFO
# must be first function call:
getufoinfo('source/masters/' + FAMILY  + '-Regular.ufo')
# BUILDLABEL = 'beta1'

TEXTSIZE = 16

# Set up the FTML tests
ftmlTest('tools/ftml-smith.xsl')

genout = 'generated/'

#for dspace in ('Upright',):
cmds = [
    cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['${source}']),
    cmd('gftools fix-nonhinting -q --no-backup ${DEP} ${TGT}'),
    ]

# for dspace in ('Upright', 'Oblique'):
for dspace in ('Upright',):
    designspace('source/' + FAMILY + dspace + '.designspace',
            target = process("${DS:FILENAME_BASE}.ttf", *cmds),
            instances = ['Namdhinggo Regular'] if '-r' in opts else None,
            opentype = fea(genout + '${DS:FILENAME_BASE}.fea',
                mapfile = genout + '${DS:FILENAME_BASE}.map',
                master = 'source/master.feax',
                make_params = '',
                params = '',
                ),
            version = VERSION,
            woff = woff('web/${DS:FILENAME_BASE}',
                metadata = f'../source/{FAMILY}-WOFF-metadata.xml'),
            script = ['limb', 'DFLT'],
            pdf = fret(params='-oi')
            )
