import argparse
import pyranges as pr
from utils.data_cleaning import prepare_coverage_df, prepare_annotation_df, prepare_output_filename
from utils.region_processing import validate_region_arguments
from plotting.custom_plots import annotation_track, coverage_track, finalize_plot

def main(args):
	
	gtf = pr.read_gtf(args.annotation)

	chromosome, start, stop = validate_region_arguments(args.chromosome, args.start, args.stop, args.region, args.gene, gtf)
	start = start - args.extend_start
	stop = stop + args.extend_stop

	if args.plots in ('both', 'coverage-only'):

		label_x_coverage = args.label_x_axis in ('both', 'coverage-only')

		coverage = prepare_coverage_df(args.input_files, chromosome, start, stop)
		cov_track = coverage_track(coverage, chromosome, start, stop, reverse_strand = args.reverse_strand, include_x_label = label_x_coverage)
	
	if args.plots in ('both', 'annotation-only'):
		
		label_x_annotation =  args.label_x_axis in ('both', 'annotation-only')

		transcripts, exons = prepare_annotation_df(gtf, chromosome, start, stop)
		ann_track = annotation_track(transcripts, exons, chromosome, start, stop, reverse_strand = args.reverse_strand, include_x_label = label_x_annotation)
	
	if args.plots == 'both':
		plot = cov_track / ann_track
	elif args.plots == 'coverage-only':
		plot = cov_track
	elif args.plots == 'annotation-only':
		plot = ann_track
	
	output_file = prepare_output_filename(args.output_dir, args.output_name, args.output_format)
	final_plot = finalize_plot(plot, args.width, args.height, args.dpi)
	final_plot.save(filename = str(output_file))

def parseArguments():
	parser = argparse.ArgumentParser(prog="main", description='', usage='%(prog)s [options]')

	input_args = parser.add_argument_group('Input Arguments')
	input_args.add_argument('-i', '--input', required=True, nargs='+', help='Input alignment files', metavar='', dest='input_files')
	input_args.add_argument('-a', '--annotation', required=True, help='Annotation file', metavar='', dest='annotation')

	region = parser.add_argument_group("Region of Interest Arguments")
	region.add_argument("--chromosome", type=str, help="Chromosome name")
	region.add_argument("--start", type=int, help="Start position")
	region.add_argument("--stop", type=int, help="Stop position")
	region.add_argument("--region", type=str, help="Region string (e.g. chr1:100-200 or 1:100-200)")
	region.add_argument("--gene", type=str, help="Gene name (e.g. MYB)")
	region.add_argument("--extend-start", type=int, default = 0, help="Subtract this number of bases from the region start. This operation happens prior to axis inversion when including --reverse-strand.", dest = 'extend_start')
	region.add_argument("--extend-stop", type=int, default = 0, help="Add this number of bases to the region stop. This operation happens prior to axis inversion when including --reverse-strand.", dest = 'extend_stop')
	
	plot = parser.add_argument_group("Plotting Arguments")
	plot.add_argument("--plots", choices = ['both', 'coverage-only', 'annotation-only'], default = 'both', help="Which plots to include.", dest='plots')
	plot.add_argument("--label-x-axis", choices = ['both', 'coverage-only', 'annotation-only', 'neither'], default = 'coverage-only', help="Which plots should have an x-axis label.", dest='label_x_axis')
	plot.add_argument("--reverse-strand", action = 'store_true', help="Reverse strand. Genes on the minus strand will be displayed as left to right.", dest='reverse_strand')

	output = parser.add_argument_group("Output Arguments")
	output.add_argument( "--output-dir", default=".", help="Directory to save the output plot (default: current directory)", dest="output_dir")
	output.add_argument( "--output-name", default="plot", help="Output file name without extension (default: plot)", dest="output_name" )
	output.add_argument( "--output-format", choices=["pdf", "png", "svg"], default="pdf", help="Output file format (default: pdf)", dest="output_format")
	output.add_argument( "--width", type=float, default=4, help="Plot width in inches (default: 4)", dest = 'width')
	output.add_argument( "--height", type=float, default=6, help="Plot height in inches (default: 6)", dest = 'height')
	output.add_argument( "--dpi", type=int, default=300, help="Plot resolution in DPI (default: 300)", dest = 'dpi')

	return parser.parse_args()

if __name__ == "__main__":
	args = parseArguments()
	main(args)