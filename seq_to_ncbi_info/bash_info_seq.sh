#!/usr/bin/env bash

place=$1
echo $place
if [  -e info_seq.txt  ]
then
    rm info_seq.txt
else
    echo ''
fi
for VAR in $place/seq_0**
do
    seq=$(echo $VAR | tr -d '.txt')
    NAME=$(cat $VAR | grep $seq)
    NAME_protein=$(cat $VAR | grep 'seq_' | awk -F \t '{print $2}' | tr -d '\\')
    NAME_PROTIEN_INFO=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}')
    NAME_GENE=$( cat $VAR | grep '\<Gene-track_geneid\>' |tr '<' '  ' | tr '>' ' ' | awk '{print $2}')
    echo -e  $seq \t $NAME_protein \t $NAME_PROTIEN_INFO \t "LOC"$NAME_GENE >> info_seq.txt
    wget 'https://www.ncbi.nlm.nih.gov/gene/?term=LOC'$NAME_GENE'&report=gene_table&format=text' -O intro.txt
    cat intro.txt  >> gene_introextro.txt
    cat intro.txt >> $VAR
done

rm intro.txt

