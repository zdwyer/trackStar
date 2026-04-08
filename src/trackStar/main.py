import argparse
import pyranges as pr
from utils.data_cleaning import prepare_coverage_df, prepare_annotation_df
from utils.region_processing import validate_region_arguments
from plotting.custom_plots import annotation_track, coverage_track

def main(args):
	
	gtf = pr.read_gtf(args.annotation)

	chromosome, start, stop = validate_region_arguments(args.chromosome, args.start, args.stop, args.region, args.gene, gtf)

	coverage = prepare_coverage_df(args.input_files, chromosome, start, stop)
	transcripts, exons = prepare_annotation_df(gtf, chromosome, start, stop)

	cov_track = coverage_track(coverage, chromosome, start, stop)
	ann_track = annotation_track(transcripts, exons, chromosome, start, stop)
	
	final_plot = cov_track / ann_track
	final_plot.save(filename="outputs/plot.png")

def parseArguments():
	parser = argparse.ArgumentParser(prog="main", description='', usage='%(prog)s [options]')

	input_args = parser.add_argument_group('Input Arguments')
	input_args.add_argument('-i', '--input', required=True, nargs='+', help='Input alignment files', metavar='', dest='input_files')
	input_args.add_argument('-a', '--annotation', required=True, help='Annotation file', metavar='', dest='annotation')

	region = parser.add_argument_group("Region of Interest")
	region.add_argument("--chromosome", type=str, help="Chromosome name")
	region.add_argument("--start", type=int, help="Start position")
	region.add_argument("--stop", type=int, help="Stop position")
	region.add_argument("--region", type=str, help="Region string (e.g. chr1:100-200 or 1:100-200)")
	region.add_argument("--gene", type=str, help="Gene name (e.g. MYB)")
	
	return parser.parse_args()

if __name__ == "__main__":
	args = parseArguments()
	main(args)