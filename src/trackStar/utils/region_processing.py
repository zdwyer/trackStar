def validate_region_arguments(chromosome_param, start_param, stop_param, region, gene, gtf):
	"""
	Validate mutually exclusive region arguments and resolve them into coordinates.

	Exactly one of the following input modes must be provided:
		1. chromosome_param, start_param, stop_param
		2. region (string of form "chromosome:start-stop")
		3. gene (looked up in GTF)

	Args:
		chromosome_param (str | None): Chromosome name.
		start_param (int | None): Start coordinate.
		stop_param (int | None): Stop coordinate.
		region (str | None): Genomic region string (e.g. "chr1:100-200" or "1:100-200).
		gene (str | None): Gene identifier or gene name.
		gtf (pyranges.PyRanges): GTF annotation as a PyRanges object.

	Returns:
		tuple[str, int, int]: A tuple containing (chromosome, start, stop).

	Raises:
		ValueError: If multiple or no input modes are provided.
		ValueError: If start is greater than or equal to stop.
		ValueError: If region or gene parsing fails.
	"""

	coords_provided = all([chromosome_param is not None, start_param is not None, stop_param is not None])	
	
	if sum([coords_provided, region is not None, gene is not None]) != 1:
		raise ValueError("Error with command line arguments. Provide either --chromosome/--start/--stop OR --region OR --gene")

	if coords_provided:
		chromosome = chromosome_param
		start = start_param
		stop = stop_param
	elif region:
		chromosome, start, stop = process_region(region)
	else:
		chromosome, start, stop = process_gene(gene, gtf)

	if start >= stop:
		raise ValueError("Region start must be less than stop. Values provided - Start: %d; Stop: %d" % (start, stop))

	return(chromosome, start, stop)

def process_region(region):
	"""
	Parse a genomic region string into coordinates.

	The region must follow the format:
		chromosome:start-stop

	Args:
		region (str): Region string (e.g. "chr1:100-200" or "1:100-200").

	Returns:
		tuple[str, int, int]: A tuple containing (chromosome, start, stop).

	Raises:
		ValueError: If the region string does not match the expected format.
	"""

	import re
	
	pattern = r"^[^:]+:\d+-\d+$"

	if not re.match(pattern, region):
		raise ValueError("Invalid --region format. Expected format: chromosome:start-stop (e.g. chr1:100-200 or 1:100-200)")
	
	chromosome, coords = region.split(":")

	start, stop = map(int, coords.split("-"))


	return(chromosome, start, stop)

def process_gene(gene, gtf):
    
	"""
	Resolve a gene name or ID to genomic coordinates using a GTF.

	The function searches for rows where Feature == "gene" and matches
	either gene_id or gene_name.

	Args:
		gene (str): Gene identifier or gene name.
		gtf (pyranges.PyRanges): GTF annotation as a PyRanges object.

	Returns:
		tuple[str, int, int]: A tuple containing (chromosome, start, stop).

	Raises:
		ValueError: If no matching gene is found.
		ValueError: If multiple matching genes are found.
    """
	
	target = gtf.subset(lambda df: (df.Feature == "gene") & ((df.gene_id == gene) | (df.gene_name == gene)))

	if len(target) > 1:
		raise ValueError("Multiple genes found with the name: %s" % (gene))
	elif len(target) == 0:
		raise ValueError("No genes found with the name: %s" % (gene))

	row = target.df.iloc[0]
	return(row['Chromosome'], row['Start'], row['End'])