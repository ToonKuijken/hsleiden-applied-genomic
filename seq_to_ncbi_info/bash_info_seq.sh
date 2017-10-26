#!/usr/bin/env bash
# Benodigde variabelen
place=$1
original_seqs=$2
ouptut_folder=$3


function  gene_length {
# Functie voor het berekenen van de lengte van het gen.
# Na het berekenen worden de gegevens naar het bestand ncbi_table.txt geschreven.
    if [ $(cat $1 | egrep 'from: ' -m1 | wc| awk '{print $2}') == 9 ]
        then
           gene_length=$(cat $1 |egrep 'from: ' -m1 | awk '{print $NF-$(NF-2)}')
            printf \\t$gene_length>>ncbi_table.txt
    else
        if [[ $(cat $1 | egrep 'from: ' -m1) == *"( &gt; )"* ]] || [[ $(cat $1 | egrep 'from: ' -m1) == *"( &lt; )"* ]]
            then
               gene_length=$(cat $1 | sed -e 's/( &gt; )//g' | sed -e 's/( &lt; )/ /g' | egrep 'from: ' -m1 |awk '{print $NF-$(NF-2)}')
               printf \\t$gene_length>>ncbi_table.txt
        else
        gene_length=$(cat $1 | egrep 'from: ' -m1 | awk '{print $(NF-2)-$NF}')
         printf \\t$gene_length>>ncbi_table.txt
        fi
    fi
}

function gene_loc {
  # Geeft de locatie van de genen vanuit de KEGG-data en schrijft het naar het bestand ncbi_table.txt.
    location=$(cat $1 | sed -e 's/( &gt; )//g' | sed -e 's/( &lt; )/ /g' | egrep 'from: ' -m1 | awk '{print $(NF-2)","$NF}')
    printf \\t$location>>ncbi_table.txt
}

function org_seq {
     # Geeft de orginele sequentie van uit de KEGG-data en schrijft het naar het bestand ncbi_table.txt.
     # Als er geen KEGG-data is geeft hij een foutmelding, dit wordt gecontroleerd bij lengte=$().
    begin=$(cat $1 | grep 'NTSEQ ' -n | awk -F":" '{print $1}')
    end=$(cat $1 | grep /// -n | awk -F":" '{print $1}')
    length=$((end - begin))

    seq=$(cat $1 |egrep 'NTSEQ' -n$length | tail -n$(($length)) | head -$(($length-1)) | tr -d [0-9]| tr -d - | tr -d ' '| tr -d '\n')
    printf \\t$seq>>ncbi_table.txt
}

function gene_tables {
  # Hier wordt alles over het gen verkregen.
    VAR=$1
    ncbi_table_name=$(cat $VAR | egrep 'value>GeneID' | uniq | sed 's/D:/D: /g' | sed 's/<\// <\//' | awk '{print $2}' )
    printf $ncbi_table_name>>ncbi_table.txt

    # De naam van het gen.
    if grep -q 'NAME' $VAR
    then
        ncbi_gene_name=$(cat $VAR | egrep 'NAME' | awk '{print $2}')
    else
        ncbi_gene_name='NONE'
    fi
    printf \\t$ncbi_gene_name>> ncbi_table.txt

    # De lengte van het gen.
    gene_length= gene_length $VAR
    printf \\t$gene_length>>ncbi_table.txt

    # Op welk chromosoom ligt het gen.
    chromosome=$(cat $VAR |grep \<GBQualifier_name\>chromosome\<  -n1 | tail -n1 | sed 's/</\t/g'| sed 's/>/\t/g' | awk '{print $3}')
    printf \\t$chromosome>>ncbi_table.txt

    # De locatie van het gen op het chromosoom in het genoom.
    location= gene_loc $VAR
    # De orginele sequentie van het gen.
    seq= org_seq $VAR

    # Het aantal exonen.
    exons=$(cat $VAR | grep [0-9]' exons' -m1 | awk '{print $(NF-7)}')
    printf \\t$exons>>ncbi_table.txt

    # De naam van het eiwit.
    name=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}' | awk '{print $1}')
    printf \\t$name>>ncbi_table.txt
    printf \\n>>ncbi_table.txt
}

function protein_tables {
     # In deze functie wordt alle informatie van het eiwit verzamelt.
    # Dit wordt dan geschreven naar eiwit_tabel.
    # De naam, grootte, EC-nummer, lengte en de sequentie worde hier opgehaald.
    VAR=$1
    NAME_protein=$2
    discript=$3

    if grep -q 'EC' $VAR
    then
        EC=$(cat $VAR | egrep 'EC:' | awk -F '['  '{print $2}'| tr -d ']')
    else
         EC='NONE'
    fi
    length=$(cat $VAR | egrep 'AASEQ' | awk '{print $2}')
    seq=$(cat $VAR|egrep '<GBSeq_sequence>' | awk 'NR==1{print $1}' | sed 's/</ </g' | sed 's/>/> /g' | awk '{print $2}')
    echo -e $NAME_protein\\t$discript\\t$EC\\t$length\\t$seq>>eiwit_tabel.txt
}

function pathways {
    # In deze functie worden de pathways waar het eiwit inzit opgehaald als deze bekend zijn.
    # Als er geen kegg data aanwezig is wordt er niks weg geschreven.
    voor='oaa'
    name=$voor$(cat $VAR | grep 'seq_' | awk -F \t '{print $2}' | tr -d '\\')
    if grep -q 'PATHWAY' $1
    then
        begin=$(cat $1 | grep 'PATHWAY ' -n | awk -F":" '{print $1}')

        if grep -q 'MODULE' $1
        then
            end=$(cat $1 | grep MODULE -n | awk -F":" '{print $1}')
        else
            end=$(cat $1 | grep BRITE -n | awk -F":" '{print $1}')
        fi
        length=$(( end - begin ))

        echo -e $name'\t'$(cat $1 |egrep 'PATHWAY' -n$length| tail -n$(($length+1)) | head -n$length | sed 's/oaa/ZZ oaa/g' | awk  -F 'ZZ ' '{print $2 "\\t"}')>>pathway_table.txt
    else
        echo
    fi
}

function mrna {
     # Hier wordt alles over het mRNA opgehaald wat bekent is.
    # De lengte, naam en sequentie worden naar een bestand geschreven.
    name=$(cat $1| egrep 'GBSeq_locus>XM_' | tr '>' ' ' | tr '<' ' ' | awk '{print $2}')
    length=$(cat $1| egrep '<GBSeq_length>' | tail -n1 | tr '>' ' ' | tr '<' ' ' | awk '{print $2}')
    seq=$(cat $1 | egrep '<GBSeq_sequence>' | tail -n1 | tr '<' ' ' | tr '>' ' ' | awk '{print $2}')
    printf $name\\t$length\\t$seq\\n>>mrna_table.txt
}

function org_sequence {
    # Hier wordt alles van de orginele mRNA opgehaald.
   name=$(cat $1| grep seq_0 | sed 's/\[/\t/g'| awk '{print $1}')
    sep=$(cat $original_seqs | grep $name -n1 | tail -n1 | tr -d [0-9]| tr -d '-')
    length=$(echo $seq | wc | awk '{print $NF}'| tr -d '\n')
    printf $name\\t$seq\\t$length\\n>>org_table.txt


}

# Controle of het bestand met info_seq.txt al bestaat.
if [  -e info_seq.txt  ]
then
    rm info_seq.txt
else
    echo ''
fi

for VAR in $place/seq_0**
do
    # Alles wat er per sequentie wordt gedaan
    seq=$(echo $VAR | tr -d '.txt')
    NAME=$(cat $VAR | grep $seq)
    NAME_protein=$(cat $VAR | grep 'seq_' | awk -F \t '{print $2}' | tr -d '\\')
    NAME_PROTEIN_INFO=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}')
    NAME_GENE=$( cat $VAR | grep '\<Gene-track_geneid\>' |tr '<' '  ' | tr '>' ' ' | awk '{print $2}')
    MRNA_NAME=$(cat $VAR| egrep 'GBSeq_locus>XM_' | tr '>' ' ' | tr '<' ' ' | awk '{print $2}')
    echo -e  $seq $NAME_protein $NAME_PROTEIN_INFO $NAME_GENE $MRNA_NAME>> info_seq.txt
    wget 'https://www.ncbi.nlm.nih.gov/gene/?term=LOC'$NAME_GENE'&report=gene_table&format=text' -O intro.txt
    cat intro.txt  >> gene_introextro.txt
    cat intro.txt >> $VAR
    echo start
    # Funties voor elk bestand:
    # Voor elk gen met bijbehorende informatie.
    gene_tables $VAR
    discription=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}'| sed -e 's/'$NAME_protein' //g'|  tr ' ' '_')
    # Funtie voor elk eiwit met bijbehorende informatie.    protein_tables $VAR $NAME_protein $discription
    # Functie voor elk gevonden pathway met bijbehorende informatie
    pathways $VAR

    mrna $VAR

    org_sequence $VAR

    echo done
done

# Verwijdering van alles.
cat mrna_table.txt |sort | uniq >mrna_table_clean.txt
cat eiwit_tabel.txt |sort | uniq >eiwit_table_clean.txt
cat ncbi_table.txt | sort -u -t, -k1,1 | uniq >ncbi_table_clean.txt
# Teslotte verwijdering van alles.cat org_table.txt |sort | uniq >org_table_clean.txt
rm intro.txt mrna_table.txt eiwit_tabel.txt ncbi_table.txt org_table.txt
echo done
