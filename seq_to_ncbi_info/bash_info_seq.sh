#!/bin/bash
place=$1
echo $place
echo 'helpppppp'
for VAR in $place/seq_0**
do
seq=$(echo $VAR | tr -d '.txt')
NAME=$(cat $VAR | grep $seq)
NAME_protein=$(cat $VAR | grep 'seq_' | awk -F \t '{print $2}' | tr -d '\\')
NAME_PROTIEN_INFO=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}')
NAME_GENE=$( cat $VAR | grep '\<Gene-track_geneid\>' |tr '<' '  ' | tr '>' ' ' | awk '{print $2}')
echo $seq $NAME_protein $NAME_PROTIEN_INFO  "LOC"$NAME_GENE
# echo 'done'
done
