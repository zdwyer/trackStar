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
  --input sample1.bam sample2.bam \
  --annotation annotation.gtf \
  --chromosome VII \
  --start 364079 \
  --stop 366105
```

### Arguments

#### Input Arguments

-   `-i, --input`\
    One or more BAM files

-   `-a, --annotation`\
    GTF annotation file

#### Region Specification

You must provide **exactly one** of the following methods to define a region:

##### 1. Genomic Coordinates

Provide chromosome, start, and stop directly:

```bash
--chromosome VII --start 364079 --stop 366105
```

- `-c, --chromosome`  
  Chromosome (e.g., `VII` or `chr1` or `1`)

- `-s, --start`  
  Start position (integer)

- `-e, --stop`  
  Stop position (integer)

##### 2. Region String

Provide a single region string in the format:

```bash
--region VII:364079-366105
```

- `-r, --region`  
  Region formatted as `chromosome:start-stop`  
  (e.g., `chr1:100-200` or `1:100-200` or `VII:364079-366105`)

##### 3. Gene Name or ID

Provide a gene identifier, which will be looked up in the GTF:

```bash
--gene RPL7A
```

- `-g, --gene`  
  Gene name or gene ID (must exist in the annotation file)

#### Notes

- These three options are **mutually exclusive** — you must provide exactly one.
- If multiple genes match the provided name/ID, the program will return an error.
- If no matching gene is found, the program will also return an error.

## Example Commands

### Using coordinates
```bash
python main.py --input sample.bam --annotation annotation.gtf --chromosome VII --start 364079 --end 366105
```

### Using region string
```bash
python main.py --input sample.bam --annotation annotation.gtf --region VII:364079-366105
```

### Using gene name
```bash
python main.py --input sample.bam --annotation annotation.gtf --gene RPL7A
```