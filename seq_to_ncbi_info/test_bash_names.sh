rm name_andseq.txt

for VAR in all_seq_info/seq_0**

do
SEQ=$(grep \<GBSeq_sequence $VAR -m1| sed 's/\</\ @/g'| sed 's/\>/@  /g'| awk -F@ '{print $4}')
NAME=$(grep \<GBInterval_accession $VAR  -m1| sed 's/\</\ @/g'| sed 's/\>/@  /g'| awk -F@ '{print $4}')
echo \>$NAME'Z'$SEQ >> name_andseq.txt

done