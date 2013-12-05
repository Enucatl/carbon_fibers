#!/usr/bin/env python
# encoding: utf-8

"""Make json data from a list of consecutive scans"""

from __future__ import division, print_function
import argparse
import json
import os

from dpc_reconstruction.io.hdf5 import output_name


def scan_name(number):
    """Return the name of the hdf5 file given the scan number

    :number: scan number
    :returns: string with the basename of the hdf5 file

    """
    return "S{0:05d}.hdf5".format(number)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("file", nargs=1,
                        help="output json file")
    parser.add_argument("--scan_lines", nargs='?',
                        type=int, default=5,
                        help='number of consecutive scan lines')
    parser.add_argument("--flat_lines", nargs='?',
                        type=int, default=5,
                        help='number of consecutive flat lines')
    parser.add_argument("--angle_delta", nargs='?',
                        type=float, default=4.5,
                        help='angular step (degrees)')
    parser.add_argument("--first_scan", nargs='?',
                        type=int, default=10,
                        help='number of first scan')
    parser.add_argument("--n_datasets", nargs='?',
                        type=int, default=21,
                        help='number of datasets')
    parser.add_argument("--base_folder", nargs=1,
                        help='name of the base folder for all the scans')

    args = parser.parse_args()
    offset = args.first_scan
    base_folder = args.base_folder[0]
    number_of_scan_lines = args.scan_lines
    number_of_flats = args.flat_lines
    angle_delta = args.angle_delta
    n_datasets = args.n_datasets
    output_file = args.file[0]

    scan_dict = {}
    for i in range(n_datasets):
        angle = i * angle_delta
        scan_number = offset + i * (number_of_scan_lines + number_of_flats)
        file_names_scans = [os.path.join(
            base_folder, scan_name(scan_number + j))
            for j in range(number_of_scan_lines)]
        flat_names_scans = [os.path.join(base_folder, scan_name(
            number_of_scan_lines + scan_number + j))
            for j in range(number_of_scan_lines)]
        scan_dict[angle] = {}
        scan_dict[angle]["files"] = file_names_scans
        scan_dict[angle]["output_name"] = output_name(
            file_names_scans, "").rstrip("/") + ".hdf5"
        scan_dict[angle]["flats"] = flat_names_scans

    with open(output_file, "w") as outfile:
        json.dump(scan_dict, outfile,
                  sort_keys=True, indent=4, separators=(',', ': '))
