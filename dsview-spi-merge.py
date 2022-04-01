#!/usr/bin/env python3

#
# DSView SPI Transfer Merge Utility
# (c) MikeM64 - 2022
#

#
# Use this utility to merge two DSView 1:SPI decoder transfer exports
# (csv/txt - both contain identical data) together to allow for
# easier analysis with `diff`
#

#
# Input file format:
# Id,Time[ns],1:SPI: MOSI transfer
# 0,2149586100.00000000000000000000,30 70 F0 00 00 00 00
# ...
#

import argparse

from collections import namedtuple

def parse_arguments():
    parser = argparse.ArgumentParser(description='Merge two DSView SPI exports together for analysis.')
    parser.add_argument('export_files', metavar='file', type=str, nargs=2, \
                        help='The two export files to merge')
    parser.add_argument('-o', '--output-file', type=str, required=True)

    args = parser.parse_args()
    return (args)

def find_mosi_miso_files(files_to_sort):
    miso_file = None
    mosi_file = None

    for filename in files_to_sort:
        with open(filename, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if 'MOSI' in first_line:
                mosi_file = filename
            elif 'MISO' in first_line:
                miso_file = filename

    return (miso_file, mosi_file)

SPITransferRecord = namedtuple('SPITransferRecord', ['transfer_id', 'ns_timestamp', 'data'])

def parse_spi_transfer_line(transfer_line):
    record = SPITransferRecord(*transfer_line.strip().split(','))
    return (record)

def merge_files(mosi_file, miso_file, output_file):
    try:
        output_file_f = open(output_file, 'w', encoding='utf-8')
        mosi_file_f = open(mosi_file, 'r', encoding='utf-8')
        miso_file_f = open(miso_file, 'r', encoding='utf-8')

        # Discard the initial header line
        mosi_line = mosi_file_f.readline()
        miso_line = miso_file_f.readline()

        # Continue parsing from transaction 0 onwards
        mosi_line = mosi_file_f.readline()
        miso_line = miso_file_f.readline()

        output_file_f.write('# Merge of:\n')
        output_file_f.write('# MOSI File:' + mosi_file + '\n')
        output_file_f.write('# MISO File:' + miso_file + '\n')
        output_file_f.write('\n')

        while miso_line and mosi_line:
            mosi_transfer = parse_spi_transfer_line(mosi_line)
            miso_transfer = parse_spi_transfer_line(miso_line)

            output_file_f.write('{:8} - MOSI - {} - {}\n'.format(
                                    mosi_transfer.transfer_id, mosi_transfer.ns_timestamp,
                                    mosi_transfer.data))
            output_file_f.write('{:8} - MISO - {} - {}\n'.format(
                                    miso_transfer.transfer_id, miso_transfer.ns_timestamp,
                                    miso_transfer.data))
            output_file_f.write('\n')

            mosi_line = mosi_file_f.readline()
            miso_line = miso_file_f.readline()
    except Exception as e:
        print('Failed to merge files because: ' + e)
        exit(-1)
    finally:
        output_file_f.close()
        mosi_file_f.close()
        miso_file_f.close()
    print('Finished merging to ' + output_file + '!')

def main():
    args = parse_arguments()

    miso_file, mosi_file = find_mosi_miso_files(args.export_files)

    if not miso_file:
        printf('File with MISO data not found')
        exit(1)

    if not mosi_file:
        printf('File with MOSI data not found')
        exit(1)

    print('Merging MISO from: ' + miso_file)
    print('Merging MOSI from: ' + mosi_file)

    merge_files(mosi_file, miso_file, args.output_file)

if __name__ == '__main__':
    main()
