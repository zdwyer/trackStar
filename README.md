# trackStar

trackStar is a command-line tool to visualize sequencing coverage alongside genomic annotations for a user-defined region.

## Installation

### Requirements

-   Python 3.8+
-   Required Python packages:
    -   `pysam`
    -   `numpy`
    -   `pandas`
    -   `pyranges`
    -   `plotnine`

Install dependencies using pip:

``` bash
pip install pysam numpy pandas pyranges plotnine
```

## Usage

Run the main script with:

``` bash
python main.py \
  -i sample1.bam sample2.bam \
  -a annotation.gtf \
  -c VII \
  -s 364079 \
  -e 366105
```

### Arguments

#### Input Arguments

-   `-i, --input`\
    One or more BAM files

-   `-a, --annotation`\
    GTF annotation file

#### Region Arguments

-   `-c, --chromosome`\
    Chromosome (e.g., `VII`)

-   `-s, --start`\
    Start position (integer)

-   `-e, --stop`\
    Stop position (integer)