#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=C0301

"Run all the reconstructions with the fourier component analysis"

from __future__ import division, print_function

import argparse
import h5py
from subprocess import check_call
import numpy as np
import os
import re

import logging
import logging.config
from dpc_reconstruction.logger_config import config_dictionary
log = logging.getLogger()

reconstruction_bin = "flats_every.py"
from dpc_reconstruction.io.hdf5 import output_name


def extract_date(string):
    """Get date inside string

    :string: @todo
    :returns: @todo

    """
    match = re.search(r"(\d\d\d\d\.\d\d\.\d\d)", string)
    return match.group(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("files", nargs='+',
                        help="files with the scans")
    parser.add_argument("--steps", nargs='?',
                        type=int, default=21,
                        help="phase steps")
    parser.add_argument("--flats_every", nargs='?',
                        type=int, default=5,
                        help="flats every n scans")
    parser.add_argument("--n_flats", nargs='?',
                        type=int, default=5,
                        help="flats to average")
    parser.add_argument("--angle_delta", nargs='?',
                        type=float, default=4.5,
                        help="angular step")
    parser.add_argument("--verbose", "-v",
                        action="store_true",
                        help="print debug info.")
    args = parser.parse_args()
    if args.verbose:
        config_dictionary['handlers']['default']['level'] = 'DEBUG'
        config_dictionary['loggers']['']['level'] = 'DEBUG'
    logging.config.dictConfig(config_dictionary)

    # determine the length of each block
    files = args.files
    n = len(files) // (args.flats_every + args.n_flats)

    # built the command for the reconstruction program
    command = "{0} ".format(reconstruction_bin)
    command += " ".join(args.files)
    command += " -o "
    if args.verbose:
        command += " -v "
    command += " -j 7 "
    command += " --flats_every {0} ".format(args.flats_every)
    command += " --n_flats {0} ".format(args.n_flats)
    command += " --steps {0} ".format(args.steps)
    log.debug(command)
    check_call(command, shell=True)

    # open the hdf5 file with the reconstruction
    input_file_name = os.path.dirname(
        output_name(files, "MergeFlatsEvery")) + ".hdf5"
    h5_file = h5py.File(input_file_name, "r")
    big_dataset = h5_file['postprocessing']['MergeFlatsEvery']
    datasets = np.dsplit(big_dataset, n)
    output_file_name = extract_date(input_file_name) + ".csv"
    angle_delta = args.angle_delta

    # write the absorption and dark field of each pixel to the csv output
    # file
    with open(output_file_name, "w") as output_file:
        print("angle,pixel,absorption,darkfield",
              file=output_file)
        for i, dataset in enumerate(datasets):
            angle = i * angle_delta
            along_2 = np.average(dataset, axis=2)
            along_0 = np.average(along_2, axis=0)
            for i, pixel_values in enumerate(along_0):
                line = '{angle},{pixel},{absorption},{darkfield}'.format(
                    angle=angle,
                    pixel=i + 1,
                    absorption=pixel_values[0],
                    darkfield=pixel_values[2])
                print(line, file=output_file)
