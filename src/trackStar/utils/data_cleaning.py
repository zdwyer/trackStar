import pysam
import numpy as np
import pandas as pd
from pathlib import Path

def prepare_coverage_df(input_files, chromosome, start, stop):

	coverage_list = []

	for bam_file in input_files:
		local_coverage = extract_coverage(bam_file, chromosome, start, stop)
		coverage_list.append(local_coverage)

	coverage_matrix = np.vstack(coverage_list)
	sample_names = [Path(f).stem for f in input_files]

	coverage_df = pd.DataFrame(coverage_matrix.T, columns = sample_names)
	coverage_df['Position'] = np.arange(start, stop)
	final_coverage = coverage_df.melt(id_vars='Position', var_name='Sample', value_name='Coverage')

	return(final_coverage)

def prepare_annotation_df(gtf, chromosome, start, stop):

	target_region = gtf[chromosome, start:stop]

	transcript = target_region [(target_region.Feature == 'transcript')]
	exons = target_region [(target_region.Feature == 'exon')]

	transcript_df = transcript.df.copy()
	exon_df = exons.df.copy()

	transcript_df["tx_id"] = transcript_df["transcript_id"]
	exon_df["tx_id"] = exon_df["transcript_id"]

	transcript_order = {tx: i for i, tx in enumerate(sorted(transcript_df["tx_id"].unique()))}

	transcript_df["y"] = transcript_df["tx_id"].map(transcript_order)
	exon_df["y"] = exon_df["tx_id"].map(transcript_order)

	exon_df["ymin"] = exon_df["y"] - 0.3
	exon_df["ymax"] = exon_df["y"] + 0.3

	return(transcript_df, exon_df)

def extract_coverage(bam_infile, chromosome, start, stop):
	bam = pysam.AlignmentFile(bam_infile)
	coverage = bam.count_coverage('chr%s' % chromosome, start, stop, read_callback='nofilter')
	total_coverage = [sum(base) for base in zip(*coverage)]  
	return total_coverage

def prepare_output_filename(output_dir, output_name, output_format):
	output_dir = Path(output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)
	name = Path(output_name).stem
	output_file = output_dir / f"{name}.{output_format}"
	return(output_file)
