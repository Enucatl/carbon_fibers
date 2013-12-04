#!/usr/bin/env Rscript

library(argparse)
library(ggplot2)
library(data.table)

commandline_parser <- ArgumentParser(description="draw results for angle analysis") 

commandline_parser$add_argument('-f', '--file',
                                type='character', nargs='?', default='angle_data.csv')
commandline_parser$add_argument('--min_pixel',
                                type='integer', nargs='?', default=400)
commandline_parser$add_argument('--max_pixel',
                                type='integer', nargs='?', default=900)

args <- commandline_parser$parse_args()
angle.table <- data.table(read.csv(args$f), key="angle")

min_pixel <- args$min_pixel
max_pixel <- args$max_pixel

absorption.table <- angle.table[pixel %between% c(min_pixel, max_pixel),
                                list(signal="absorption",
                                     mean=mean(absorption),
                                     sd=sd(absorption)),
                                by=angle]
darkfield.table <- angle.table[pixel %between% c(min_pixel, max_pixel),
                               list(signal="darkfield",
                                    mean=mean(darkfield),
                                    sd=sd(darkfield)),
                                by=angle]

average <- rbind(absorption.table, darkfield.table)

file_name <- "graphs.pdf"
pdf(file_name,
    width=17, height=12)
graph <- ggplot(average,
                aes(x=angle,
                    y=mean,
                    color=signal)) + geom_line(
                aes(group=signal)) + scale_y_continuous(
                name=sprintf("average over pixels %d to %d",
                    min_pixel, max_pixel)) + scale_x_continuous(
                name="angle (degrees)") + geom_ribbon(
                    aes(ymin=mean - sd,
                        ymax=mean + sd,
                        linetype=NA,
                        fill=signal),
                    alpha=0.2)
print(graph)
dev.off()
embed_fonts(file_name)
