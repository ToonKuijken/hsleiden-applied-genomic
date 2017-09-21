#!/usr/bin/env bash

place=$1
for VAR in $place/seq_0**
do
seq=$(echo $VAR | tr -d '.txt')
NAME=$(cat $VAR | grep $seq)
GENE_CODE=$( cat $VAR | grep '\<Gene-track_geneid\>' |tr '<' '  ' | tr '>' ' ' | awk '{print $2}')
NAME_GENE=$( cat $VAR | egrep "<Gene-ref_locus>" | tr ">" " " | tr "<" " " | awk '{print $2}')
echo "LOC"$GENE_CODE $NAME_GENE >> result.txt
done
cat result.txt | sort | uniq > result_gen.txt
rm result.txt
