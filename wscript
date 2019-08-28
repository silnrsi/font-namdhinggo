#!/usr/bin/python
# encoding: utf-8
# this is a smith configuration file

# set some default folders (most are already set by default)
STANDARDS = 'tests/reference'
generated = 'generated/'

# set the version control system
VCS = 'git'

# set the font name, version, licensing and description
APPNAME = "NamdhinggoSIL"
DESC_SHORT = "Unicode font for the Limbu writing system of Nepal"

# Get version and authorship info from Regular UFO
# must be first function call:
getufoinfo('source/NamdhinggoSIL-Regular.ufo')

fontfamily = APPNAME

designspace('source/NamdhinggoSIL.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
                mapfile = generated + '${DS:FILENAME_BASE}.map',
                master = 'source/master.feax',
                make_params = '',
                params = '',
                ),
            script = ['latn', 'limb'],
            pdf = fret(params="-r -oi"),
            woff = woff()
            )
