#! /bin/bash
GENE_NAME=$1
echo $GENE_NAME
folder=$2
echo $2
mkdir $folder
#ls
echo 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='$1'&retmode=xml'
wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='$1'&retmode=xml' -O $1'.txt'
#echo "one"
gene_id=$( grep 'GeneID'  $1.txt | tr '<' ' '| tr ':' ' '| awk '{print $2}')

echo $gene_id
#
echo 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id='$gene_id'&retmode=xml'
wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id='$gene_id'&retmode=xml' -O $1'_gene.txt'
echo "two"
mrna_entry=$(grep mRNA $1_gene.txt -n2| tail -n2 | head -n1 | tr '<' '\t' | tr '>' '\t'| awk 'begin{FS="\t"}{print $3}')
echo $mrna_entry
echo 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id='$mrna_entry'&retmode=xml'
wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id='$mrna_entry'&retmode=xml' -O $1'_mRNA.txt'
echo "tree"

