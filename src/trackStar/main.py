import argparse
from utils.data_cleaning import prepare_coverage_df, prepare_annotation_df
from plotting.custom_plots import annotation_track, coverage_track

def main(args):
	
	coverage = prepare_coverage_df(args.input_files, args.chromosome, args.region_start, args.region_stop)
	transcripts, exons = prepare_annotation_df(args.annotation, args.chromosome, args.region_start, args.region_stop)

	cov_track = coverage_track(coverage, args.chromosome, args.region_start, args.region_stop)
	ann_track = annotation_track(transcripts, exons, args.chromosome, args.region_start, args.region_stop)
	
	final_plot = cov_track / ann_track
	final_plot.save(filename="outputs/plot.png")


def parseArguments():
	parser = argparse.ArgumentParser(prog="main", description='', usage='%(prog)s [options]')
	
	input_args = parser.add_argument_group('Input Arguments')
	input_args.add_argument('-i', '--input', required=True, nargs='+', help='Input alignment files', metavar='', dest='input_files')
	input_args.add_argument('-a', '--annotation', required=True, help='Annotation file', metavar='', dest='annotation')

	region = parser.add_argument_group('Region Arguments')
	region.add_argument('-c', '--chromosome', required=True,  help='The chromosome of the region of interest', metavar='', dest='chromosome')
	region.add_argument('-s', '--start', required=True, type=int, help='The start position of the region of interest', metavar='', dest='region_start')
	region.add_argument('-e', '--stop', required=True, type=int, help='The stop position of the region of interest', metavar='', dest='region_stop')
	return parser.parse_args()

if __name__ == "__main__":
	args = parseArguments()
	main(args)