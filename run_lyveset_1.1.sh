#! /bin/bash
#Author: Logan Fink
#Usage: script to select a reference genome for input to lyve-SET and run lyve-SET
#Permission to copy and modify is granted without warranty of any kind
#Last revised 03/12/18

run_quit=false
while getopts :q opt; do
    case $opt in
        q)run_quit=true ;;
    esac
done

shift "$(( OPTIND-1 ))"

##### Create the snp_counts directory #####
python /home/staphb/scripts/pairwise_matrix_dist*.py ./roary/core_gene_alignment.aln
ref=$(head -1 ./snp_counts/avg_snp_differences_ordered | cut -d ' ' -f 1)

##### Create lyveset directory. If it exists, delete it and create it #####
rm -rf lyveset 2>/dev/null
set_manage.pl --create lyveset

cp ./spades_assembly_trim/*$ref*/contigs.fasta lyveset/reference/$ref.fasta
cp ./clean/*.fastq.gz lyveset/reads/
launch_set.pl lyveset -ref lyveset/reference/$ref.fasta --allowedFlanking 5 --min_alt_frac 0.95 --min_coverage 20 --numcpus 8

if $run_quit; then
    sudo shutdown -h now
fi
