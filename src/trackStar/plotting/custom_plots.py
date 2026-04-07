from plotnine import ggplot, aes, theme_classic, theme, element_blank, xlim, scale_y_continuous, labs, scale_y_reverse, geom_segment, geom_rect, geom_col, facet_grid

def coverage_track(df_long, chromosome, start, stop):
	return (
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
		+ xlim(start, stop)
		+ scale_y_continuous(expand = (0,0))
		+ geom_col(width = 1)
	)

def annotation_track(transcript_df, exon_df, chromosome, start, stop):

	return (
		ggplot()
		+ theme_classic()
		+ theme(
			axis_text = element_blank(),
			axis_ticks = element_blank(),
			axis_title = element_blank(),
			axis_line = element_blank()
		)
		+ xlim(start, stop)
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