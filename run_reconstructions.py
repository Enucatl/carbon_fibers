#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=C0301

"Run all the reconstructions with the fourier component analysis"

from __future__ import division, print_function

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

scan_dict = {}
for i in range(21):
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

output_table = "dark_field_table.csv"
with open(output_table, "w") as output_file:
    output_file.write("angle,")
    output_file.write(",".join([str(x) for x in range(1, 1025)]))
    output_file.write("\n")
    for angle, scan in scan_dict.iteritems():
        command = "{0} ".format(reconstruction_bin)
        command += " ".join(scan['files'])
        command += " --flat " + " ".join(scan['flats'])
        command += " -o "
        command += " --steps {0} ".format(steps)
        print(command)
        check_call(command, shell=True)
        print(scan['output_name'])
        dark_field_file = h5py.File(scan['output_name'], "r")
        dark_field_dataset = dark_field_file[
            'postprocessing']['Stacker'][..., 2]
        average_along_2 = np.average(dark_field_dataset, axis=2)
        average_along_0 = np.average(average_along_2, axis=0)
        as_string = ",".join(["{0}".format(
            x) for x in average_along_0])
        line = "{0},{1}\n".format(
            angle, as_string)
        output_file.write(line)
