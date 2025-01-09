# -*- coding: utf-8 -*-

import os
import platform
import tempfile
from .Utils.ColorFormatting import display_alert
from .Utils.CustomExceptions import WordlistNotFound

data_filters = ['cpf', 'rg', 'email', 'phone']
file_types = ['txt', 'csv', 'bmp', 'png', 'gif', 'pdf', 'tiff', 'jpeg', 'webp', 'docx', 'xlsx', 'pptx', 'mail']
valid_save_types = ['csv', 'json', 'txt', 'db']

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def validate_wordlist_path(args, colors):
    wordlist_path = os.path.join(script_dir, "wordlists/")
    if not os.path.exists(wordlist_path):
        raise WordlistNotFound(script_dir, colors)

def validate_directory_and_file_args(args, colors):
    if not (args.directory or args.file):
        raise ValueError(display_alert("Error: Either -d or -f option must be provided", colors=colors))

    if args.directory and args.file:
        raise ValueError(display_alert("Error: Both -d and -f options cannot be provided simultaneously", colors=colors))


def validate_file_operations(args, colors):
    if args.copy and (args.move or args.delete):
        raise ValueError(display_alert("Error: -copy and (-move, -delete) cannot be provided simultaneously", colors=colors))
    if args.move and (args.copy or args.delete):
        raise ValueError(display_alert("Error: -move and (-copy, -delete) cannot be provided simultaneously", colors=colors))
    if args.delete and (args.copy or args.move):
        raise ValueError(display_alert("Error: -delete and (-copy, -move) cannot be provided simultaneously", colors=colors))
    if args.delete and args.save:
        raise ValueError(display_alert("Error: -delete and -save cannot be provided simultaneously", colors=colors))
    if args.move and args.save:
        raise ValueError(display_alert("Error: -move and -save cannot be provided simultaneously", colors=colors))


def validate_findme_and_datatype_args(args, colors):
    if args.findme and args.data_filters:
        raise ValueError(display_alert("Error: Both -find and -datatype options cannot be provided simultaneously", colors=colors))


def validate_files(args, colors):
    if args.file:
        args.file = validate_paths(args.file, colors, is_dir=False)


def validate_directories(args, colors):
    if args.directory:
        args.directory = validate_paths(args.directory, colors, is_dir=True)


def validate_paths(paths, colors, is_dir):
    validated_paths = []
    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(display_alert(f"Error: {'Directory' if is_dir else 'File'} {path} does not exist", colors=colors))
        if not os.access(path, os.R_OK):
            raise PermissionError(display_alert(f"Error: Cannot read {path}", colors=colors))
        if is_dir and os.path.isfile(path):
            raise ValueError(display_alert(f"Error: Provided path {path} is a file", colors=colors))
        if not is_dir and os.path.isdir(path):
            raise ValueError(display_alert(f"Error: Provided path {path} is a directory", colors=colors))
        validated_paths.append(path)
    return validated_paths


def validate_ocr(args, colors):
    global file_types

    if args.ocr_enabled:
        if platform.system().lower() in ["linux", "linux2", "darwin"]:
            cmd = os.popen("which tesseract").read().strip()
            if not cmd:
                raise FileNotFoundError(display_alert("Unable to locate the Tesseract OCR executable", colors=colors))
            tesseract_path = cmd
        elif platform.system().lower() in ['win32', 'cygwin', 'windows']:
            default_path = os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'Tesseract-OCR\\tesseract.exe')
            if os.path.exists(default_path):
                tesseract_path = default_path
            else:
                cmd = 'powershell -Command "(Get-Command -Name tesseract | Select-Object -ExpandProperty Path) -or (where.exe tesseract)"'
                path = os.popen(cmd).read().strip()
                if not path:
                    raise FileNotFoundError(display_alert("Unable to locate the Tesseract OCR executable", colors=colors))
                tesseract_path = path
        return tesseract_path
    else:
        for file_type in ('bmp', 'png', 'gif', 'tiff', 'jpeg', 'webp'):
            if file_type in file_types:
                file_types.remove(file_type)
        return None


def validate_datatype_args(args, colors):
    global data_filters
    if args.data_filters:
        args.data_filters = set(args.data_filters)
        for dt in args.data_filters:
            if dt not in data_filters:
                raise ValueError(display_alert(f"Error: Invalid data type(s) provided {dt}", colors=colors))
        filtered_types = []
        for value in data_filters:
            if value in args.data_filters:
                filtered_types.append(value)
        data_filters = filtered_types


def validate_filetype_args(args, colors):
    global file_types
    if args.file_filters:
        args.file_filters = set(args.file_filters)
        for ft in args.file_filters:
            if ft not in file_types:
                raise ValueError(display_alert(f"Error: Invalid file type provided: {ft}", colors=colors))
            if ft in ['bmp', 'png', 'gif', 'tiff', 'jpeg', 'webp'] and not args.ocr_enabled:
                raise ValueError(display_alert(f"Error: File type {ft} cannot be used without OCR capabilities", colors=colors))
        filtered_types = []
        for value in file_types:
            if value in args.file_filters:
                filtered_types.append(value)
        file_types = filtered_types


def validate_save(args, colors):
    paths_to_check = [os.getcwd(), os.environ['HOME'], tempfile.gettempdir()]
    if args.save:
        save_types = args.save
        writable_path = False
        for path in paths_to_check:
            if os.access(path, os.W_OK):
                writable_path = True
                full_path = os.path.abspath(path)
                args.save = {"path": full_path, "types": save_types}
                break
        
        if not writable_path:
            raise PermissionError(display_alert(f"Insufficient permissions to save results on paths: {paths_to_check}", colors=colors))

        for st in save_types:
            if st not in valid_save_types:
                raise ValueError(display_alert(f"Error: Invalid export option {st}. Must be one of: {', '.join(valid_save_types)}", colors=colors))

def validate_copy(args, colors):
    if args.copy:
        current = os.getcwd()
        default = os.path.abspath(f'{args.copy}/CopiedFiles/')

        if os.path.isfile(args.copy):
            raise ValueError(display_alert(f"Error: Destination path {args.copy} is a file", colors=colors))

        elif args.copy == current:
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))
                args.copy = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        elif not os.path.isabs(args.copy):
            default = f"{current}/{default}"
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))
                args.copy = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        else:
            parent_dir = os.path.dirname(os.path.abspath(args.copy))
            if os.path.exists(default):
                raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))

            elif os.path.exists(args.copy) and not os.access(args.copy, os.W_OK):
                raise PermissionError(display_alert(f"Error: Cannot write to {args.copy}", colors=colors))

            elif os.path.exists(args.copy) and not os.access(parent_dir, os.W_OK):
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))

            else:
                args.copy = default


def validate_move(args, colors):
    if args.move:
        current = os.getcwd()
        default = os.path.abspath(f'{args.move}/MovedFiles/')

        if os.path.isfile(args.move):
            raise ValueError(display_alert(f"Error: Destination path {args.move} is a file", colors=colors))

        elif args.move == current:
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))
                args.move = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        elif not os.path.isabs(args.move):
            default = f"{current}/{default}"
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))
                args.move = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        else:
            parent_dir = os.path.dirname(os.path.abspath(args.move))
            if os.path.exists(default):
                raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))

            elif os.path.exists(args.move) and not os.access(args.move, os.W_OK):
                raise PermissionError(display_alert(f"Error: Cannot write to {args.move}", colors=colors))

            elif os.path.exists(args.move) and not os.access(parent_dir, os.W_OK):
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))

            else:
                args.move = default

def validate_arguments(args, colors):

    validate_findme_and_datatype_args(args, colors)
    validate_directory_and_file_args(args, colors)
    validate_file_operations(args, colors)
    validate_datatype_args(args, colors)
    validate_filetype_args(args, colors)
    validate_wordlist_path(args, colors)
    validate_directories(args, colors)
    validate_files(args, colors)
    validate_save(args, colors)
    validate_move(args, colors)
    validate_copy(args, colors)

    tesseract_path = validate_ocr(args, colors)

    return args, file_types, data_filters, tesseract_path
