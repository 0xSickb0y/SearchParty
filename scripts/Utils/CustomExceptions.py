# -*- coding: utf-8 -*-

import os
from .ColorFormatting import display_negative


class NoSupportedFiles(Exception):
    def __init__(self, args=None, colors=None):
        self.colors = colors
        self.directories = args.directory if args and args.directory else []
        self.files = args.file if args and args.file else []

    def __str__(self):
        message = ""
        if self.directories:
            message = f"No supported files were encountered at: {', '.join(os.path.abspath(directory) for directory in self.directories)}"
        if self.files:
            message = f"Files: {', '.join(os.path.abspath(file_path) for file_path in self.files)} are not supported"
        return display_negative(message, self.colors)


class NoDataFound(Exception):
    def __init__(self, args=None, colors=None):
        self.directories = args.directory if args and args.directory else []
        self.files = args.file if args and args.file else []
        self.colors = colors

    def __str__(self):
        if self.directories:
            message = f"No data were found at: {', '.join(os.path.abspath(directory) for directory in self.directories)}"
        if self.files:
            message = f"No data were found at: {', '.join(os.path.abspath(file_path) for file_path in self.files)}"
        return display_negative(message, self.colors)
