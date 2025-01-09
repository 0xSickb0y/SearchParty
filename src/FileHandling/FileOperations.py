# -*- coding: utf-8 -*-

import os
import shutil

def copy_files(args, data_found):
    os.makedirs(args.copy, exist_ok=True)

    processed_files = set()

    for file_list in data_found.values():
        if file_list:
            for info in file_list:
                file_path = info['file'] if args.findme else info

                if file_path in processed_files:
                    continue

                processed_files.add(file_path)

                if not os.access(file_path, os.R_OK):
                    print(f"Insufficient permissions to copy file: {file_path}")
                else:
                    dest_path = os.path.join(args.copy, os.path.basename(file_path))

                    if not os.path.exists(dest_path):
                        shutil.copy(file_path, args.copy)
                    else:
                        print(f"File already exists in destination: {dest_path}")
    
    print(f"\nCopied {len(processed_files)} files")


def move_files(args, data_found):
    os.makedirs(args.move, exist_ok=True)

    processed_files = set()

    for file_list in data_found.values():
        if file_list:
            for info in file_list:
                file_path = info['file'] if args.findme else info

                if file_path in processed_files:
                    continue

                processed_files.add(file_path)

                if not os.access(file_path, os.W_OK):
                    print(f"Insufficient permissions to move file: {file_path}")
                else:
                    dest_path = os.path.join(args.move, os.path.basename(file_path))

                    if not os.path.exists(dest_path):
                        shutil.move(file_path, args.move)
                    else:
                        print(f"File already exists at destination: {dest_path}")

    print(f"\nMoved {len(processed_files)} files")

def delete_files(args, data_found):
    processed_files = set()

    for file_list in data_found.values():
        if file_list:
            for info in file_list:
                file_path = info['file'] if args.findme else info

                if file_path in processed_files:
                    continue

                processed_files.add(file_path)

                if not os.access(file_path, os.W_OK):
                    print(f"Insufficient permissions to delete file: {file_path}")
                else:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    else:
                        print(f"Failed to delete: {file_path} (not found)")

    print(f"\nDeleted {len(processed_files)} files")