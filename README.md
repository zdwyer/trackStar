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

#### Plotting Arguments

------------------------------------------------------------------------

##### `--plots` 

  Specify which tracks to include in the final output.

  * `both` (*default*) - show coverage and annotation tracks stacked vertically

  * `coverage-only` - show only the coverage track

  * `annotation-only` - show only the annotation tarck

    ```bash
    --plots {both, coverage-only, annotation-only}
    ```

------------------------------------------------------------------------

##### `--label-x-axis` 

  Control which tracks display the x-axis (label, ticks, and values).

  * `both` - both tracks include x-axis labels, ticks, and values

  * `coverage-only` (*default*) - only the coverage track includes x-axis labels, ticks, and values

  * `annotation-only` - only the annotation track includes x-axis labels, ticks, and values

    ```bash
    --label-x-axis {both, coverage-only, annotation-only}
    ```

------------------------------------------------------------------------

##### `--reverse-strand`

	Reverse the x-axis so genomic coordinates are displayed right-to-left.

  * Useful for visualizing genes on the minus strand in a more intuitive orientation (5' → 3')

  * Applies to both **coverage** and **annotation** tracks

  * Axis reversal occurs after any region extension (`--extend-start`, `--extend-stop`)

	```bash
	--reverse-strand
	```

------------------------------------------------------------------------

##### `--extend-start` and `--extend-stop` 

  Expand the plotted region upstream or downstream:

  * `--extend-start` - subtracts bases from the start coordinate

  * `--extend-stop` - adds bases to the stop coordinate

    ```bash
    --extend-start 1000
    --extend-stop 1000
    ```

    These adjustments are applied **before** strand reversal.

------------------------------------------------------------------------

#### Output Control

------------------------------------------------------------------------

##### `--output-dir` 

  Controls the directory in which to save result.

  * Default: current directory (`.`)

  * Creates directory if it does not exist

      ``` bash
      --output-dir output/plots
      ```

------------------------------------------------------------------------

##### `output-name`

  Controls the output plot's filename (Default: plot).

  * Do not include the extension in the filename.

    ``` bash
    --output-name myplot
    ```

------------------------------------------------------------------------

##### `output-format`

  Controls the output plot's format (Default: pdf).

  * Options: pdf, png, svg

    ``` bash
    --output-format {pdf, png, svg}
    ```
------------------------------------------------------------------------

##### `width`

  Controls the output plot width in inches (Default: 4).

------------------------------------------------------------------------

##### `height`

  Controls the output plot height in inches (Default: 6).

------------------------------------------------------------------------

##### `dpi`

  Controls the output plot dots per inch (Default: 300).

------------------------------------------------------------------------

## Example Commands

### Using coordinates
```bash
python main.py --input sample.bam --annotation annotation.gtf --chromosome VII --start 364079 --stop 366105
```

### Using region string
```bash
python main.py --input sample.bam --annotation annotation.gtf --region VII:364079-366105
```

### Using gene name
```bash
python main.py --input sample.bam --annotation annotation.gtf --gene RPL7A
```