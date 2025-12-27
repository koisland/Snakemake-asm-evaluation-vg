#!/bin/bash

set -euo pipefail

cat /project/logsdon_shared/projects/Keith/Snakemake-asm-evaluation-vg/test/input/all_regions.bed | \
    xargs -I {} bash -c 'path=$(printf "{}" | cut -f 4); bedtools intersect -a "${path}" -b <(printf "{}")'
