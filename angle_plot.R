#!/usr/bin/env Rscript

library(argparse)
library(ggplot2)
library(data.table)

commandline_parser <- ArgumentParser(
        description="draw results for angle analysis") 

commandline_parser$add_argument('-f', '--file',
            type='character', nargs='?', default='dark_field_table.csv')

args <- commandline_parser$parse_args()
dark_field_table <- as.data.table(read.csv(args$f))
setkeyv(dark_field_table, "angle")
#print(dark_field_table)
#print(nrow(dark_field_table))
#print(ncol(dark_field_table))

min_pixel <- 300
max_pixel <- 800

selected_pixels <- dark_field_table[, min_pixel:max_pixel, with=FALSE]
print(selected_pixels)
print(nrow(selected_pixels))
print(ncol(selected_pixels))
average <- selected_pixels[, list(mean=rowMeans(.SD))]
print(average)
print(nrow(average))
print(ncol(average))
