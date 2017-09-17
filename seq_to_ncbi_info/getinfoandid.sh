#! /bin/bash
GENE_NAME=$1
SEQ_NAME=$3
echo $GENE_NAME
echo $SEQ_NAME

folder=$2
#echo $2
mkdir $folder

#echo 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='$1'&retmode=xml'
wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='$1'&retmode=xml' -O $3'.txt'
gene_id=$( grep 'GeneID'  $3.txt | tr '<' ' '| tr ':' ' '| awk '{print $2}')

#echo $gene_id

#echo 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id='$gene_id'&retmode=xml'
wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id='$gene_id'&retmode=xml' -O $3'_gene.txt'

mrna_entry=$(grep mRNA $3_gene.txt -n2| tail -n2 | head -n1 | tr '<' '\t' | tr '>' '\t'| awk 'begin{FS="\t"}{print $3}')
#echo $mrna_entry
#echo 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id='$mrna_entry'&retmode=xml'
wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id='$mrna_entry'&retmode=xml' -O $3'_mRNA.txt'
#echo $gene_id

#wget 'http://www.genome.jp/dbget-bin/www_bget?oaa:'$gene_id -O html.txt
#cat html.txt | grep pathway | sed 's/\/kegg-bin\/show_pathway\?/ZZ/g' >> pathway.txt
#echo  \n\n >>pathway.txt


echo 'done'



