#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: ts=4 sw=4 et ai si

"""
A simple tool to find duplicate file files
"""

import argparse
import sys, os

from collections import defaultdict

from hashlib import sha1

def main(args):
    """
    entry point
    """
    parser = argparse.ArgumentParser(description="Find and delete duplicate files.")
    parser.add_argument('-d', '--delete', action="store_true", help='delete duplicates')
    parser.add_argument('directory', nargs='*', default=['.'], help='directory to go through')
    args = parser.parse_args()

    data = defaultdict(list)

    for dirname in args.directory:
        for path, _, files in os.walk(dirname):
            for name in files:
                fname = os.path.join(path, name)
                with open(fname, 'rb') as handle:
                    data[sha1(handle.read()).digest()].append(fname)

    for files in [sorted(v) for v in data.values() if len(v) > 1]:
        print('%d duplicate(s) of %s' % (len(files) - 1, files[-1]))
        if args.delete:
            for fname in files[:-1]:
                try:
                    os.remove(fname)
                    print (' ', fname, '(deleted)')
                except OSError as e:
                    print ("Error: %s - %s." % (e.filename, e.strerror))
        else:
            for fname in files[:-1]:
                print (' ', fname)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
