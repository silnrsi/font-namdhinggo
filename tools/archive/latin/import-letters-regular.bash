#!/bin/bash

config=$HOME/script/limb/fonts/namdhinggo_local/latin

pushd $config
cat uppercase_base.txt lowercase_base.txt uppercase_accent.txt lowercase_accent.txt lowercase_extra.txt > import.txt
psfgetglyphnames -a aglfn-nr.csv -i import.txt instances/GentiumBookPlus-Regular.ufo glyphs.csv
popd

for ufo in *.ufo
do
    # import characters
    psfcopyglyphs --rename rename --unicode usv --force -s $config/instances/GentiumBookPlus-Regular.ufo -i $config/glyphs.csv -l ${ufo}_import.log $ufo
    git add $ufo
    git commit -m "Replacing Latin and adding glyphs in $ufo"

    # scale characters
    for codepoints in uppercase_accent lowercase_accent uppercase_base lowercase_base lowercase_extra
    do
        psfgetglyphnames -a ${config}/aglfn-nr.csv -i ${config}/${codepoints}.txt $config/instances/GentiumBookPlus-Regular.ufo ${codepoints}_import.csv
        awk 'FS=","{printf "%s,%s,%s\n", $2, $2, $3}' ${codepoints}_import.csv | tail -n +2 > ${codepoints}.csv
        transform=$(echo $codepoints | cut -d _ -f 1)
        psfmakescaledshifted -i ${codepoints}.csv -t latin$transform -l ${ufo}_${codepoints}.log $ufo
    done
    cd ../..
    ./preflight
    cd -
    git add $ufo
    git commit -m "Transformed Latin glyphs in $ufo"
done
