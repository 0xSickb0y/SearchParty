import os
import time
import psutil
import platform
import datetime
from magic import from_file
from filetype import guess_mime
from .Utils.ColorFormatting import display_info
from .Utils.CustomExceptions import NoSupportedFiles

supported_files = {}

file_patterns = {'txt': 'text/plain',
                 'csv': 'text/csv',
                 'bmp': 'image/bmp',
                 'png': 'image/png',
                 'gif': 'image/gif',
                 'tiff': 'image/tiff',
                 'jpeg': 'image/jpeg',
                 'webp': 'image/webp',
                 'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                 'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                 'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                 'pdf': 'application/pdf',
                 'mail': 'message/rfc822'}


def filter_file_patterns(file_types):
    for ft in list(file_patterns.keys()):
        if ft not in file_types:
            del file_patterns[ft]


def convert_size(size):
    for unit in ['Bytes', 'Kb', 'Mb', 'Gb', 'Tb']:
        if size < 1000.0:
            return f"{size:.2f} {unit}"
        size /= 1000.0


def get_filesystem_size():
    total_size = psutil.disk_usage(os.path.abspath(os.sep)).total
    return convert_size(total_size)


def start_information(args, colors):

    current_user = os.getlogin()
    hostname = platform.node()
    fs_size = get_filesystem_size()
    operating_system = f'{platform.system()} {platform.release()} {platform.machine()}'
    sys_uptime = str(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).split('.')[0]

    print(f"Starting SearchParty with PID {os.getpid()} [{time.strftime('%H:%M:%S %d/%b/%Y')}]")
    print(display_info("System Information", colors))

    sys_info = f"Current User: {current_user}\n" \
               f"Hostname: {hostname}\n" \
               f"Operating System: {operating_system}\n" \
               f"File System Size: {fs_size}\n" \
               f"Uptime: {sys_uptime}\n"

    if args.directory:
        sys_info += f"Working Directories: {', '.join(os.path.abspath(directory) for directory in args.directory)}"

    if args.file:
        sys_info += f"Working Files: {', '.join(os.path.abspath(file_path) for file_path in args.file)}"

    print(sys_info)


def process_file_argument(args):
    for argument in args.file:
        for pattern_name, mime_type in file_patterns.items():
            if from_file(argument, mime=True) == mime_type or guess_mime(argument) == mime_type:
                if pattern_name not in supported_files:
                    supported_files[pattern_name] = []
                supported_files[pattern_name].append(argument)

    if len(supported_files) != 0:
        for value in supported_files.values():
            for file_path in value:
                print(f"File: {os.path.abspath(file_path)} ({convert_size(os.path.getsize(file_path))}) MIME: {guess_mime(file_path) or from_file(file_path, mime=True)}")


def process_directory_argument(args):
    supported_files_size = 0
    for argument in args.directory:
        for path, dirs, files in os.walk(argument):
            for filename in files:
                full_path = os.path.abspath(os.path.join(path, filename))
                supported_files_size += os.path.getsize(full_path)
                for pattern_name, mime_type in file_patterns.items():
                    if from_file(full_path, mime=True) == mime_type or guess_mime(full_path) == mime_type:
                        if pattern_name not in supported_files:
                            supported_files[pattern_name] = []
                        supported_files[pattern_name].append(full_path)

    if len(supported_files) != 0:
        print(f"Directories Have {sum(len(value) for value in supported_files.values())} Supported Items. {convert_size(supported_files_size)}")
        sorted_keys = sorted(supported_files.keys(), key=lambda x: (file_patterns[x], x, len(x)))
        print("\n".join(f"{file_patterns[key]} ({len(supported_files[key])})" for key in sorted_keys))


def process_contents(args, colors):
    print(display_info(f"Enumerating Contents. [{time.strftime('%H:%M:%S %d/%b/%Y')}]", colors))
    if args.directory:
        process_directory_argument(args)
    if args.file:
        process_file_argument(args)
    if not supported_files.keys():
        raise NoSupportedFiles(args, colors)


def initial_setup(args, colors, file_types):
    filter_file_patterns(file_types)
    start_information(args, colors)
    process_contents(args, colors)
    return supported_files
