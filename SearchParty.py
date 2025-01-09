# -*- coding: utf-8 -*-

import os
import time
import argparse
import datetime
from src import main

version = "v1.1"
branch = "en-us"

banner = rf'''
   _____                      __       ____             __
  / ___/___  ____  ____ _____/ /_     / __ \____  _____/ /___  __
  \__ \/ _ \/ __ `/ ___/ ___/ __ \   / /_/ / __ `/ ___/ __/ / / /
 ___/ /  __/ /_/ / /  / /__/ / / /  / ____/ /_/ / /  / /_/ /_/ /
/____/\___/\__,_/_/   \___/_/ /_/  /_/    \__,_/_/   \__/\__  /
                                                         /___/
{version} {branch}

Offline tool for personal/sensitive data mapping & analytics
https://github.com/0xSickb0y/SearchParty/
'''

parser = argparse.ArgumentParser(
    prog='SearchParty.py',
    description=print(banner),
    allow_abbrev=False,
    epilog=f"For detailed usage, refer to the `Usage` section in: {os.path.dirname(os.path.abspath(__file__))}/README.md")


def separate_args(arguments):
    return arguments.split(',')


parser.add_argument('-d', metavar="path", dest='directory', action='append', help='scan directory')
parser.add_argument('-f', metavar="path", dest='file', action='append', help='scan file')
parser.add_argument('-dcf', dest='no_colors', action='store_true', help='disable color formatting in the output')
parser.add_argument('-ocr', dest='ocr_enabled', action='store_true', help='enable optical character recognition')
parser.add_argument('-find', metavar='', dest='findme', type=str, nargs='+', help="search for specific values")
parser.add_argument('-save', metavar='db,csv ...', dest='save', type=separate_args, help='export results to [db, csv, txt, json]')
parser.add_argument('-copy', metavar='dst', dest='copy', nargs='?', const=os.getcwd(), help='copy files to another location')
parser.add_argument('-move', metavar='dst', dest='move', nargs='?', const=os.getcwd(), help='move files to another location')
parser.add_argument('-delete', dest='delete', action="store_true", help='delete files with positive results')
parser.add_argument('-datatype', metavar='type', dest='data_filters', type=separate_args, help='data type filtering')
parser.add_argument('-filetype', metavar='type', dest='file_filters', type=separate_args, help='file type filtering')

args = parser.parse_args()

start_time = time.time()

if __name__ == '__main__':
    if not args.no_colors:
        main(args, parser, colors=True)
    else:
        main(args, parser, colors=False)

end_time = time.time()

print(f'Elapsed time: {datetime.timedelta(seconds=end_time - start_time)}')
