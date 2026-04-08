from plotnine import ggplot, aes, theme_classic, theme, element_blank, scale_y_continuous, labs, scale_y_reverse, scale_x_reverse, geom_segment, geom_rect, geom_col, facet_grid, coord_cartesian

def coverage_track(df_long, chromosome, start, stop, reverse_strand = False, include_x_label = True):

	if reverse_strand:
		x_coord = coord_cartesian(xlim=(stop, start))
		x_scale = scale_x_reverse(expand=(0, 0))
	else:
		x_coord = coord_cartesian(xlim=(start, stop))
		x_scale = None

	p = (
		ggplot(df_long, aes(x = "Position", y = "Coverage", color = "Sample"))
		+ theme_classic()
		+ theme(
			legend_position = 'none',
			strip_background = element_blank()
		)
		+ facet_grid(
			"Sample"
		)
		+ labs(x = "Genomic Position (%s)" % (chromosome))
		+ x_coord
		+ x_scale
		+ scale_y_continuous(expand = (0,0))
		+ geom_col(width = 1)
	)

	if not include_x_label:
		p = (
			p
			+ labs(x = None)
			+ theme(
				axis_title_x = element_blank(),
				axis_text_x = element_blank(),
				axis_ticks_x = element_blank()
			)
		)

	return p

def annotation_track(transcript_df, exon_df, chromosome, start, stop, reverse_strand = False, include_x_label = False):

	if reverse_strand:
		x_coord = coord_cartesian(xlim=(stop, start))
		x_scale = scale_x_reverse(expand=(0, 0))
	else:
		x_coord = coord_cartesian(xlim=(start, stop))
		x_scale = None

	p =  (
		ggplot()
		+ theme_classic()
		+ theme(
			axis_text_y = element_blank(),
			axis_ticks_y = element_blank(),
			axis_title_y = element_blank(),
			axis_line_y = element_blank()
		)
		+ labs(x = "Genomic Position (%s)" % (chromosome))
		+ x_coord
		+ x_scale
		+ scale_y_reverse()
		+ geom_segment(
			data = transcript_df, 
			mapping = aes(x = "Start", xend = "End", y = 'y', yend = 'y'),
			size = 0.8
		)
		+ geom_rect(
			data = exon_df, 
			mapping = aes(xmin = "Start", xmax = "End", ymin = "ymin", ymax = "ymax")
		)
	)

	if not include_x_label:
		p = (
			p
			+ labs(x = None)
			+ theme(
				axis_title_x = element_blank(),
				axis_text_x = element_blank(),
				axis_ticks_x = element_blank(),
				axis_line_x = element_blank()
			)
		)

	return p

def finalize_plot(p, width, height, dpi):
	final = (
		p
		+ theme(
			figure_size=(width, height),
			dpi = dpi
		)
	)
	return(final)