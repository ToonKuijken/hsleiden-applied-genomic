#!/usr/bin/env bash
GENE_NAME=$1
SEQ_NAME=$3

folder=$2
if [  -d $folder  ]
then
    echo ''
else
    mkdir $folder
fi

wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='$1'&retmode=xml ' -O $3'.txt'
gene_id=$( grep 'GeneID'  $3.txt | tr '<' ' '| tr ':' ' '| awk '{print $2}')

wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id='$gene_id'&retmode=xml ' -O $3'_gene.txt'

mrna_entry=$(grep mRNA $3_gene.txt -n2| tail -n2 | head -n1 | tr '<' '\t' | tr '>' '\t'| awk 'begin{FS="\t"}{print $3}')

wget 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id='$mrna_entry'&retmode=xml ' -O $3'_mRNA.txt'
