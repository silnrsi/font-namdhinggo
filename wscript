#!/usr/bin/python
# encoding: utf-8
# this is a smith configuration file

# output folders use smith defaults and don't need to be set here

# set the version control system
VCS = 'git'

# set the font name, version, licensing and description
APPNAME="NamdhinggoSIL"
DESC_SHORT = "Font for the Limbu script"
DESC_LONG = """
Namdhinggo SIL is a Unicode font for the Limbu writing system of Nepal.
Font sources are published in the repository and a smith open workflow is
used for building, testing and releasing.
"""
# packaging
DESC_NAME = "NamdhinggoSIL"
DEBPKG = 'fonts-sil-namdhinggo'

# Get version and authorship info from Regular UFO; must be first function call:
getufoinfo('source/NamdhinggoSIL-Regular.ufo')

fontfamily=APPNAME

designspace('source/NamdhinggoSIL.designspace',
            target = "${DS:FILENAME_BASE}.ttf",
            pdf = fret(params="-r -oi"),
            woff = woff()
    )
