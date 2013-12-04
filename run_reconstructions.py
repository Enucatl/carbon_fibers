#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=C0301

"Run all the reconstructions with the fourier component analysis"

from __future__ import division, print_function

import argparse
import os
import h5py
from subprocess import check_call
import numpy as np

from dpc_reconstruction.io.hdf5 import output_name

base_folder = "/afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.11.27/S00000-00999"  # noqa
reconstruction_bin = "reconstruction.py"


def scan_name(number):
    """Return the name of the hdf5 file given the scan number

    :number: scan number
    :returns: string with the basename of the hdf5 file

    """
    return "S{0:05d}.hdf5".format(number)

offset = 16
number_of_scan_lines = 5
number_of_flats = 5
angle_delta = 4.5
steps = 21
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--test",
                    action="store_true",
                    help="test with a single dataset")
args = parser.parse_args()
if args.test:
    n_datasets = 1
else:
    n_datasets = 21

scan_dict = {}
for i in range(n_datasets):
    angle = i * angle_delta
    scan_number = offset + i * (number_of_scan_lines + number_of_flats)
    file_names_scans = [os.path.join(base_folder, scan_name(scan_number + j))
                        for j in range(number_of_scan_lines)]
    flat_names_scans = [os.path.join(base_folder, scan_name(
        number_of_scan_lines + scan_number + j))
        for j in range(number_of_scan_lines)]
    scan_dict[angle] = {}
    scan_dict[angle]["files"] = file_names_scans
    scan_dict[angle]["output_name"] = output_name(
        file_names_scans, "").rstrip("/") + ".hdf5"
    scan_dict[angle]["flats"] = flat_names_scans

output_table = "angle_data.csv"
with open(output_table, "w") as output_file:
    print("angle,pixel,absorption,darkfield", file=output_file)
    for angle, scan in scan_dict.iteritems():
        command = "{0} ".format(reconstruction_bin)
        command += " ".join(scan['files'])
        command += " --flat " + " ".join(scan['flats'])
        command += " -o "
        command += " -j 6 "
        command += " --steps {0} ".format(steps)
        print(command)
        check_call(command, shell=True)
        h5_file = h5py.File(scan['output_name'], "r")
        dataset = h5_file['postprocessing']['Stacker']
        along_2 = np.average(dataset, axis=2)
        along_0 = np.average(along_2, axis=0)
        for i, pixel_values in enumerate(along_0):
            line = '{angle},{pixel},{absorption},{darkfield}'.format(
                angle=angle,
                pixel=i + 1,
                absorption=pixel_values[0],
                darkfield=pixel_values[2])
            print(line, file=output_file)
