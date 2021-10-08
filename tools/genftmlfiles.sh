#!/bin/bash

# This script rebuilds the algorithmically-generated ftml files.

set -e

if [ ! -f wscript ]
then
	echo "Must be in the root of the project"
	exit 2
fi

# configure tests
tests="AllChars Diac Matras"
urls='url(../references/NamdhinggoSIL-Regular.ttf)=RefRegular url(../results/NamdhinggoSIL-Regular.ttf)=Regular url(../results/NamdhinggoSIL-Bold.ttf)=Bold'
ufo='source/masters/NamdhinggoSILMaster-Regular.ufo'

# list all the fonts to test
fonts=''
for url in $urls
do
	fonts="$fonts -s '$url'"
done

echo "Rebuilding ftml files..."
for test in $tests
do
	base=${test,,}
	title="\"${test} auto\""
	ftml=tests/${base}.ftml
	log=tests/logs/${base}.log
	eval tools/psfgenftml.py -q -t "$title" --scale 200 --norendercheck -i source/glyph_data.csv --xsl ../tools/ftml.xsl "$fonts" -l $log $ufo $ftml &
done
wait
echo "done."
