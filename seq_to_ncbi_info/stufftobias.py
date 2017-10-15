import subprocess

lijst = []
for i in range(1,46):
    if int(i) < 10:
        i = '00' + str(i)
        lijst.append(i)
    else:
        i = '0' + str(i)
        lijst.append(i)

for x in lijst:
    #print("cat seq_00" + str(x) +".txt | sed 's/EC:/\nEC:/g' | egrep 'EC:' | tr ']' ' '")
    subprocess.call("cat seq_" + str(x) +".txt | sed 's/EC:/\\nEC:/g' | egrep 'EC:' | tr ']' ' ' >> eiwit_ec", shell=True)
for x in lijst:    
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'AASEQ' | awk '{print $2}' >> eiwit_aalengte", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep '<GBSeq_sequence>' | awk 'NR==1{print $1}' | sed 's/</ </g' | sed 's/>/> /g' | awk '{print $2}' >> eiwit_aaseq", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'NTSEQ' | awk '{print $2}' >> eiwit_ntlengte", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep '<GBSeq_sequence>' | awk 'NR==2{print $1}' | sed 's/</ </g' | sed 's/>/> /g' | awk '{print $2}' >> eiwit_ntseq", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'GBSeq_locus>XM_' | tr '>' ' ' | tr '<' ' ' | awk '{print $2}' >> mRNA_id", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep '<GBSeq_sequence>' | tail -n1 | tr '<' ' ' | tr '>' ' ' | awk '{print $2}' >> mRNA_seq", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep '<GBSeq_length>' | tail -n1 | tr '>' ' ' | tr '<' ' ' | awk '{print $2}' >> mRNA_lengte", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'value>GeneID' | uniq | sed 's/D:/D: /g' | sed 's/<\// <\//' | awk '{print $2}' >> gen_id", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'NAME' | awk '{print $2}' >> gen_naam", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'from: ' | awk '{print $NF-$(NF-2)}' >> gen_lengte", shell=True)
for x in lijst:
    subprocess.call("bash gen_locatie.sh" + x, shell=True)
    print('hoi')
for x in lijst:
    subprocess.call("cat seq_" + str(x) + ".txt | egrep 'oaa[0-9][0-9][0-9][0-9][0-9] ' | sed 's/PATHWAY//g' | awk '{print $1 "'\t'"}' | tr '\n' ' ' >> pathway_id", shell=True)
for x in lijst:
    subprocess.call("cat seq_" + str(x) +".txt | egrep 'oaa[0-9][0-9][0-9][0-9][0-9] ' | sed 's/PATHWAY//g' | awk '{$1=""; print $0 "'\t'"}' | tr '\n' ' ' >> pathway_naam", shell=True)