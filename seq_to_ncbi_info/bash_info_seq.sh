#!/usr/bin/env bash
# Benodigde variabelen
place=$1
orgninele_seqs=$2
ouptut_folder=$3


function  gen_lenght {
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
    locatie=$(cat $1 | sed -e 's/( &gt; )//g' | sed -e 's/( &lt; )/ /g' | egrep 'from: ' -m1 | awk '{print $(NF-2)","$NF}')
    printf \\t$locatie>>ncbi_table.txt
}

function org_seq {
  # Geeft de orginele sequentie van uit de KEGG-data en schrijft het naar het bestand ncbi_table.txt.
  # Als er geen KEGG-data is geeft hij een foutmelding, dit wordt gecontroleerd bij lengte=$().
    begin=$(cat $1 | grep 'NTSEQ ' -n | awk -F":" '{print $1}')
    eind=$(cat $1 | grep /// -n | awk -F":" '{print $1}')
    lengte=$((eind - begin))

    seq=$(cat $1 |egrep 'NTSEQ' -n$lengte | tail -n$(($lengte)) | head -$(($lengte-1)) | tr -d [0-9]| tr -d - | tr -d ' '| tr -d '\n')
    printf \\t$seq>>ncbi_table.txt
}

function gene_tabels {
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
    gene_length= gen_lenght $VAR
    printf \\t$gene_length>>ncbi_table.txt

    # Op welk chromosoom ligt het gen.
    chromosoom=$(cat $VAR |grep \<GBQualifier_name\>chromosome\<  -n1 | tail -n1 | sed 's/</\t/g'| sed 's/>/\t/g' | awk '{print $3}')
    printf \\t$chromosoom>>ncbi_table.txt

    # De locatie van het gen op het chromosoom in het genoom.
    location= gene_loc $VAR
    # De orginele sequentie van het gen.
    seq= org_seq $VAR

    # Het aantal exonen.
    exonen=$(cat $VAR | grep [0-9]' exons' -m1 | awk '{print $(NF-7)}')
    printf \\t$exonen>>ncbi_table.txt

    # De naam van het eiwit.
    name=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}' | awk '{print $1}')
    printf \\t$name>>ncbi_table.txt
    printf \\n>>ncbi_table.txt
}

function protien_tabels {
    #in deze funtie word alle info voor het ewiit verzamelt.
    #Dit word dan geschreven naar eiwit_tabel.
    #Er word naam groote ec lengte en de sequnetie opgehaald.
    VAR=$1
    NAME_protein=$2
    discript=$3

    if grep -q 'EC' $VAR
    then
        EC=$(cat $VAR | egrep 'EC:' | awk -F '['  '{print $2}'| tr -d ']')
    else
         EC='NONE'
    fi
    lengte=$(cat $VAR | egrep 'AASEQ' | awk '{print $2}')
    seq=$(cat $VAR|egrep '<GBSeq_sequence>' | awk 'NR==1{print $1}' | sed 's/</ </g' | sed 's/>/> /g' | awk '{print $2}')
    echo -e $NAME_protein\\t$discript\\t$EC\\t$lengte\\t$seq>>eiwit_tabel.txt
}

function pathways {
    # in deze funtie worden de pathwas opgehaald als deze bekend zijn voor het eiwit.
    #als er geen beken zijn word er niks naar geschreven.
    #dus ook als het bestand er neit is is dat omdat er geen kegg data is.
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
        lengte=$(( end - begin ))

        echo -e $name'\t'$(cat $1 |egrep 'PATHWAY' -n$lengte| tail -n$(($lengte+1)) | head -n$lengte | sed 's/oaa/ZZ oaa/g' | awk  -F 'ZZ ' '{print $2 "\\t"}')>>pathway_table.txt
    else
        echo
    fi
}

function mrna {
    # HIer word alles over het rna opgehaald wat bekent is.
    #de lengte naam sequentie en dan word het naar een bestand geschreven.
    name=$(cat $1| egrep 'GBSeq_locus>XM_' | tr '>' ' ' | tr '<' ' ' | awk '{print $2}')
    lengte=$(cat $1| egrep '<GBSeq_length>' | tail -n1 | tr '>' ' ' | tr '<' ' ' | awk '{print $2}')
    seq=$(cat $1 | egrep '<GBSeq_sequence>' | tail -n1 | tr '<' ' ' | tr '>' ' ' | awk '{print $2}')
    printf $name\\t$lengte\\t$seq\\n>>mrna_table.txt
}

function org_sequentie {
    #Hier word alles van de orginele mran opgehaald.
    name=$(cat $1| grep seq_0 | sed 's/\[/\t/g'| awk '{print $1}')
    sep=$(cat $orgninele_seqs | grep $name -n1 | tail -n1 | tr -d [0-9]| tr -d '-')
    lengt=$(echo $seq | wc | awk '{print $NF}'| tr -d '\n')
    printf $name\\t$seq\\t$lengt\\n>>org_table.txt


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
    NAME_PROTIEN_INFO=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}')
    NAME_GENE=$( cat $VAR | grep '\<Gene-track_geneid\>' |tr '<' '  ' | tr '>' ' ' | awk '{print $2}')
    MRNA_NAME=$(cat $VAR| egrep 'GBSeq_locus>XM_' | tr '>' ' ' | tr '<' ' ' | awk '{print $2}')
    echo -e  $seq $NAME_protein $NAME_PROTIEN_INFO $NAME_GENE $MRNA_NAME>> info_seq.txt
    wget 'https://www.ncbi.nlm.nih.gov/gene/?term=LOC'$NAME_GENE'&report=gene_table&format=text' -O intro.txt
    cat intro.txt  >> gene_introextro.txt
    cat intro.txt >> $VAR
    echo start
    #Funties voor elk bestand.
    #Voor gen info
    gene_tabels $VAR
    descript=$(cat $VAR | grep seq_ | sed 's/XP/\xx XP/g' | sed 's/\\n/ xx /g'| awk  -F xx '{print $5}'| sed -e 's/'$NAME_protein' //g'|  tr ' ' '_')
    # funtie voor eiwit info.
    protien_tabels $VAR $NAME_protein $descript
    #
    pathways $VAR

    mrna $VAR

    org_sequentie $VAR

    echo done
done

# Verwijdering van alles.
cat mrna_table.txt |sort | uniq >mrna_table_clean.txt
cat eiwit_tabel.txt |sort | uniq >eiwit_table_clean.txt
cat ncbi_table.txt | sort -u -t, -k1,1 | uniq >ncbi_table_clean.txt
cat org_table.txt |sort | uniq >org_table_clean.txt
rm intro.txt mrna_table.txt eiwit_tabel.txt ncbi_table.txt org_table.txt
echo done
