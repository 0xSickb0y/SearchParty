import os
import platform
from .Utils.ColorFormatting import display_alert

data_filters = ['cpf', 'rg', 'email', 'phone', 'nit', 'cns']
file_types = ['txt', 'csv', 'bmp', 'png', 'gif', 'pdf', 'tiff', 'jpeg', 'webp', 'docx', 'xlsx', 'pptx', 'mail']


def validate_directory_and_file_args(args, colors):
    if not (args.directory or args.file):
        raise ValueError(display_alert("Error: Either -D or -F option must be provided", colors=colors))

    if args.directory and args.file:
        raise ValueError(display_alert("Error: Both -D and -F options cannot be provided simultaneously", colors=colors))


def validate_file_operations(args, colors):
    if args.copy and (args.move or args.delete):
        raise ValueError(display_alert("Error: --copy-files and (--move-files, --delete-files) cannot be provided simultaneously", colors=colors))
    if args.move and (args.copy or args.delete):
        raise ValueError(display_alert("Error: --move-files and (--copy-files, --delete-files) cannot be provided simultaneously", colors=colors))
    if args.delete and (args.copy or args.move):
        raise ValueError(display_alert("Error: --delete-files and (--copy-files, --move-files) cannot be provided simultaneously", colors=colors))
    if args.delete and (args.text or args.database):
        raise ValueError(display_alert("Error: --delete-files and (--to-text, --to-database) cannot be provided simultaneously", colors=colors))
    if args.move and (args.text or args.database):
        raise ValueError(display_alert("Error: --move-files and (--to-text, --to-database) cannot be provided simultaneously", colors=colors))


def validate_findme_and_datatype_args(args, colors):
    if args.findme and args.data_filters:
        raise ValueError(display_alert("Error: Both -sV and --data-type options cannot be provided simultaneously", colors=colors))


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
                raise ValueError(display_alert(f"Error: Invalid file type(s) provided {ft}", colors=colors))
        filtered_types = []
        for value in file_types:
            if value in args.file_filters:
                filtered_types.append(value)
        file_types = filtered_types


def validate_csv(args, colors):
    if args.csv:
        current = os.getcwd()
        default = f"{args.csv}/{platform.node()}.csv"

        if args.csv == current:
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.csv = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        elif os.path.isdir(args.csv):
            if os.access(args.csv, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.csv = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {args.csv}", colors=colors))

        elif not os.path.isabs(args.csv):
            default = f"{current}/{args.csv}"
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.csv = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        else:
            parent_dir = os.path.split(args.csv)[0]
            if os.access(parent_dir, os.W_OK):
                if os.path.exists(args.csv):
                    raise ValueError(display_alert(f"Error: {args.csv} already exists", colors=colors))
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))


def validate_json(args, colors):
    if args.json:
        current = os.getcwd()
        default = f"{args.json}/{platform.node()}.json"

        if args.json == current:
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.json = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        elif os.path.isdir(args.json):
            if os.access(args.json, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.json = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {args.json}", colors=colors))

        elif not os.path.isabs(args.json):
            default = f"{current}/{args.json}"
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.json = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        else:
            parent_dir = os.path.split(args.json)[0]
            if os.access(parent_dir, os.W_OK):
                if os.path.exists(args.json):
                    raise ValueError(display_alert(f"Error: {args.json} already exists", colors=colors))
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))


def validate_text(args, colors):
    if args.text:
        current = os.getcwd()
        default = f"{args.text}/{platform.node()}.txt"

        if args.text == current:
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.text = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        elif os.path.isdir(args.text):
            if os.access(args.text, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.text = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {args.text}", colors=colors))

        elif not os.path.isabs(args.text):
            default = f"{current}/{args.text}"
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.text = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        else:
            parent_dir = os.path.split(args.text)[0]
            if os.access(parent_dir, os.W_OK):
                if os.path.exists(args.text):
                    raise ValueError(display_alert(f"Error: {args.text} already exists", colors=colors))
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))


def validate_database(args, colors):
    if args.database:
        current = os.getcwd()
        default = f"{args.database}/{platform.node()}.db"

        if args.database == current:
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.database = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        elif os.path.isdir(args.database):
            if os.access(args.database, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.database = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {args.database}", colors=colors))

        elif not os.path.isabs(args.database):
            default = f"{current}/{args.database}"
            if os.access(current, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: {default} already exists", colors=colors))
                args.database = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {current}", colors=colors))

        else:
            parent_dir = os.path.split(args.database)[0]
            if os.access(parent_dir, os.W_OK):
                if os.path.exists(args.database):
                    raise ValueError(display_alert(f"Error: {args.database} already exists", colors=colors))
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))


def validate_copy(args, colors):
    if args.copy:
        current = os.getcwd()
        default = f'{args.copy}/CopiedFiles/'

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
            parent_dir = os.path.split(args.copy)[0]
            if os.access(parent_dir, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))
                args.copy = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))


def validate_move(args, colors):
    if args.move:
        current = os.getcwd()
        default = f'{args.move}/MovedFiles/'

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
            parent_dir = os.path.split(args.move)[0]
            if os.access(parent_dir, os.W_OK):
                if os.path.exists(default):
                    raise ValueError(display_alert(f"Error: Destination path {default} already exists", colors=colors))
                args.move = default
            else:
                raise PermissionError(display_alert(f"Error: Cannot write to {parent_dir}", colors=colors))


def validate_arguments(args, colors):

    validate_findme_and_datatype_args(args, colors)
    validate_directory_and_file_args(args, colors)
    validate_file_operations(args, colors)
    validate_datatype_args(args, colors)
    validate_filetype_args(args, colors)
    validate_directories(args, colors)
    validate_database(args, colors)
    validate_files(args, colors)
    validate_move(args, colors)
    validate_csv(args, colors)
    validate_text(args, colors)
    validate_json(args, colors)
    validate_copy(args, colors)

    tesseract_path = validate_ocr(args, colors)

    return args, file_types, data_filters, tesseract_path
