#!/usr/bin/env python3

import os
import time
import argparse
import datetime
from scripts import main

banner = r'''
   _____                      __       ____             __
  / ___/___  ____  ____ _____/ /_     / __ \____  _____/ /___  __
  \__ \/ _ \/ __ `/ ___/ ___/ __ \   / /_/ / __ `/ ___/ __/ / / /
 ___/ /  __/ /_/ / /  / /__/ / / /  / ____/ /_/ / /  / /_/ /_/ /
/____/\___/\__,_/_/   \___/_/ /_/  /_/    \__,_/_/   \__/\__  /
                                                         /___/
v1.0

Offline tool for personal/sensitive data mapping & analytics
https://github.com/0xSickb0y/SearchParty/
'''

parser = argparse.ArgumentParser(
    prog='SearchParty.py',
    description=print(banner),
    allow_abbrev=False,
    epilog='')


def separate_args(arguments):
    return arguments.split(',')


parser.add_argument('-F', metavar="path", dest='file', action='append', help='scan file')
parser.add_argument('-D', metavar="path", dest='directory', action='append', help='scan directory')
parser.add_argument('-sV', metavar='', dest='findme', type=str, nargs='+', help="search for specific values")
parser.add_argument('--data-type', metavar='type', dest='data_filters', type=separate_args, help='data type filtering')
parser.add_argument('--file-type', metavar='type', dest='file_filters', type=separate_args, help='file type filtering')
parser.add_argument('--to-csv', metavar="name", dest='csv', nargs='?', const=os.getcwd(), help='save results to csv')
parser.add_argument('--to-json', metavar="name", dest='json', nargs='?', const=os.getcwd(), help='save results to json')
parser.add_argument('--to-text', metavar="name", dest='text', nargs='?', const=os.getcwd(), help='save results to text')
parser.add_argument('--to-database', metavar='name', dest='database', nargs='?', const=os.getcwd(), help='save results to a database')
parser.add_argument('--copy-files', metavar='dst', dest='copy', nargs='?', const=os.getcwd(), help='copy files to another location')
parser.add_argument('--move-files', metavar='dst', dest='move', nargs='?', const=os.getcwd(), help='move files to another location')
parser.add_argument('--delete-files', dest='delete', action="store_true", help='delete files from the file system')
parser.add_argument('--no-colors', dest='no_colors', action='store_true', help='disable color formatting in the output')
parser.add_argument('--enable-ocr', dest='ocr_enabled', action='store_true', help='enable optical character recognition')

args = parser.parse_args()

start_time = time.time()

if __name__ == '__main__':
    if not args.no_colors:
        main(args, parser, colors=True)
    else:
        main(args, parser, colors=False)

end_time = time.time()

print(f'Elapsed time: {datetime.timedelta(seconds=end_time - start_time)}')
