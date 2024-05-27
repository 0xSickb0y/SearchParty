import sys
from .InitialSetup import initial_setup
from .SearchResults import search_results
from .ValidateArguments import validate_arguments
from .InformationExtractor import information_extractor
from .Utils.CustomExceptions import NoSupportedFiles, NoDataFound


def main(args, parser, colors):
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    try:
        args, file_types, data_filters, tesseract_path = validate_arguments(args, colors)
        supported_files = initial_setup(args, colors, file_types)
        data_found, data_indexes, error_log = information_extractor(args, colors, file_types, data_filters, supported_files, tesseract_path)
        search_results(args, colors, supported_files, data_found, data_indexes, error_log)

    except (ValueError, FileNotFoundError, FileExistsError, PermissionError) as error:
        print(error)
        parser.print_help()
        sys.exit(1)
    except (NoSupportedFiles, NoDataFound) as custom:
        print(custom)
        sys.exit(0)
