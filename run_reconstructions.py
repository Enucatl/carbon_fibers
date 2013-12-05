#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=C0301

"Run all the reconstructions with the fourier component analysis"

from __future__ import division, print_function

import argparse
import h5py
from subprocess import check_call
import numpy as np
import json

reconstruction_bin = "reconstruction.py"


def scan_name(number):
    """Return the name of the hdf5 file given the scan number

    :number: scan number
    :returns: string with the basename of the hdf5 file

    """
    return "S{0:05d}.hdf5".format(number)

if __name__ == '__main__':
    steps = 21
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file", nargs=1,
                        help="json file with angle/flats/files dict")
    args = parser.parse_args()

    scan_dict = json.load(open(args.file[0]))

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
