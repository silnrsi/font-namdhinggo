#!/bin/bash

config=$HOME/script/limb/fonts/namdhinggo_local/latin
latin=$config/instances/stock/GentiumBookPlus-Bold.ufo

pushd $config
cat uppercase_base.txt lowercase_base.txt uppercase_accent.txt lowercase_accent.txt lowercase_extra.txt > import.txt
psfgetglyphnames -a aglfn-nr.csv -i import.txt $latin glyphs.csv
popd

for ufo in NamdhinggoSILMaster-ExtraBold.ufo
do
    # import characters
    psfcopyglyphs --rename rename --unicode usv --force -s $latin -i $config/glyphs.csv -l ${ufo}_import.log $ufo

    # scale characters
    for codepoints in uppercase_accent lowercase_accent uppercase_base lowercase_base lowercase_extra
    do
        psfgetglyphnames -a ${config}/aglfn-nr.csv -i ${config}/${codepoints}.txt $latin ${codepoints}_import.csv
        awk 'FS=","{printf "%s,%s,%s\n", $2, $2, $3}' ${codepoints}_import.csv | tail -n +2 > ${codepoints}.csv
        transform=$(echo $codepoints | cut -d _ -f 1)
        psfmakescaledshifted -i ${codepoints}.csv -t latin$transform -l ${ufo}_${codepoints}.log $ufo
    done
    cd ../..
    ./preflight
    cd -
    psfdeleteglyphs -i $config/delete.txt $ufo
    git add $ufo
    git commit -m "Re-import bold letters"
done
