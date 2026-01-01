#!/bin/bash

set -euo pipefail

function intersect() {
    path=$1
    chrom=$2
    st=$3
    end=$4
    asm_name=$(basename "${path}" _hifi_misassemblies.bed);
    bedtools intersect -a "${path}" -b <(printf "${chrom}\t${st}\t${end}\n") | \
        awk -v OFS="\t" -v ANAME="${asm_name}" -v ST="${st}" -v ED="${end}" '{ $1=ANAME"_"$1":"ST"-"ED; $2=$2-ST; $3=$3-ST; print}'
}

export -f intersect
cat /project/logsdon_shared/projects/Keith/Snakemake-asm-evaluation-vg/test/input/all_regions.bed | \
    xargs -I {} bash -c 'intersect $(printf "{}" | cut -f 4) $(printf "{}" | cut -f 1) $(printf "{}" | cut -f 2) $(printf "{}" | cut -f 3)'
