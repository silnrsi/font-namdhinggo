#!/bin/bash

config=$HOME/script/limb/fonts/namdhinggo_local/latin

pushd $config
cat digits.txt > import.txt
psfgetglyphnames -a aglfn-nr.csv -i import.txt instances/GentiumPlus-Bold.ufo glyphs.csv
popd

for ufo in NamdhinggoSILMaster-ExtraBold.ufo
do
    # import characters
    psfcopyglyphs --rename rename --unicode usv --force -s $config/instances/GentiumPlus-Bold.ufo -i $config/glyphs.csv -l ${ufo}_import.log $ufo
    git add $ufo
    git commit -m "Replacing Latin digits in $ufo"
done
