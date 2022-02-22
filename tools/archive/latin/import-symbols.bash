#!/bin/bash

declare -A ufos
ufos[NamdhinggoSILMaster-ExtraBold.ufo]=stock/GentiumBookPlus-Bold.ufo
ufos[NamdhinggoSILMaster-Regular.ufo]=custom/GentiumBookPlus-Regular.ufo

config=$HOME/script/limb/fonts/namdhinggo_local/latin

for ufo in *.ufo
do
    # import characters
    latin=$config/instances/${ufos[$ufo]}
    pushd $config
    cat lowercase_blue.txt > import.txt
    psfgetglyphnames -a aglfn-nr.csv -i import.txt $latin glyphs.csv
    popd

    psfcopyglyphs --rename rename --unicode usv --force -s $latin -i $config/glyphs.csv -l ${ufo}_import.log $ufo

    # scale characters
    for codepoints in lowercase_blue
    do
        psfgetglyphnames -a ${config}/aglfn-nr.csv -i ${config}/${codepoints}.txt $latin ${codepoints}_import.csv
        awk 'FS=","{printf "%s,%s,%s\n", $2, $2, $3}' ${codepoints}_import.csv | tail -n +2 > ${codepoints}.csv
        transform=$(echo $codepoints | cut -d _ -f 1)
        psfmakescaledshifted -i ${codepoints}.csv -t latin$transform -l ${ufo}_${codepoints}.log $ufo
    done

    # cleanup
    psfdeleteglyphs -i $config/delete_blue.txt $ufo
    psfrenameglyphs -i $config/rename_blue.txt $ufo
    psfsetunicodes -i $config/encode_blue.txt $ufo
    cd ../..
    ./preflight
    cd -
    git add $ufo
done
git commit -m "Make some symbols bold"
