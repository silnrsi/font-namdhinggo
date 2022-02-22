#!/bin/bash

config=$HOME/script/limb/fonts/namdhinggo_local/latin

pushd $config
cat ftml.txt > import.txt
psfgetglyphnames -a aglfn-nr.csv -i import.txt instances/GentiumBookPlus-Regular.ufo glyphs.csv
popd

for ufo in *.ufo
do
    # import characters
    psfcopyglyphs --rename rename --unicode usv --force -s $config/instances/GentiumBookPlus-Regular.ufo -i $config/glyphs.csv -l ${ufo}_import.log $ufo
    git add $ufo
    git commit -m "Adding characters for FTML tests in $ufo"
done
