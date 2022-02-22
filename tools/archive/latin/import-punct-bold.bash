#!/bin/bash

config=$HOME/script/limb/fonts/namdhinggo_local/latin
latin=$config/instances/stock/GentiumBookPlus-Bold.ufo

pushd $config
cat math_purple.txt > import.txt
psfgetglyphnames -a aglfn-nr.csv -i import.txt $latin glyphs.csv
popd

for ufo in NamdhinggoSILMaster-ExtraBold.ufo
do
    # import characters
    psfcopyglyphs --rename rename --unicode usv --force -s $latin -i $config/glyphs.csv -l ${ufo}_import.log $ufo

    # scale characters
    for codepoints in math_purple
    do
        psfgetglyphnames -a ${config}/aglfn-nr.csv -i ${config}/${codepoints}.txt $latin ${codepoints}_import.csv
        awk 'FS=","{printf "%s,%s,%s\n", $2, $2, $3}' ${codepoints}_import.csv | tail -n +2 > ${codepoints}.csv
        transform=$(echo $codepoints | cut -d _ -f 1)
        psfmakescaledshifted -i ${codepoints}.csv -t latin$transform -l ${ufo}_${codepoints}.log $ufo
    done
    cd ../..
    ./preflight
    cd -
    psfdeleteglyphs -i $config/delete_purple.txt $ufo
    psfsetunicodes -i $config/encode_purple.txt $ufo
    git add $ufo
    git commit -m "Make some punctuation bold"
done
