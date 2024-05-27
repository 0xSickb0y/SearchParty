import os
import shutil


def copy_files(args, data_found):

    os.makedirs(args.copy)
    errors = set()
    files_copied = False

    for file_list in data_found.values():
        if file_list:
            for info in file_list:
                try:
                    if args.findme:
                        if not os.path.exists(os.path.join(args.copy, os.path.basename(info['file']))):
                            shutil.copy(info['file'], args.copy)
                    else:
                        if not os.path.exists(os.path.join(args.copy, os.path.basename(info))):
                            shutil.copy(info, args.copy)
                    files_copied = True
                except Exception as error:
                    error_type = type(error).__name__
                    errors.add(error_type)

    copied_message = f'\nDone!' if files_copied else ''

    if errors:
        copied_message += f'Errors were encountered when copying files: {", ".join(errors)}'

    print(f'{copied_message}\n')


def move_files(args, data_found):

    os.makedirs(args.move)
    errors = set()
    files_moved = False

    for file_list in data_found.values():
        if file_list:
            for info in file_list:
                try:
                    if args.findme:
                        if not os.path.exists(os.path.join(args.move, os.path.basename(info['file']))):
                            shutil.move(info['file'], args.move)
                    else:
                        if not os.path.exists(os.path.join(args.move, os.path.basename(info))):
                            shutil.move(info, args.move)
                    files_moved = True
                except Exception as error:
                    error_type = type(error).__name__
                    errors.add(error_type)

    moved_message = f'\nDone!' if files_moved else ''

    if errors:
        moved_message += f'Errors were encountered when moving files: {", ".join(errors)}'

    print(f'{moved_message}\n')


def delete_files(args, data_found):

    errors = set()

    for file_list in data_found.values():
        if file_list:
            for info in file_list:
                try:
                    if args.findme:
                        if os.path.exists(info['file']):
                            os.remove(info['file'])
                    else:
                        if os.path.exists(info):
                            os.remove(info)
                    files_deleted = True
                except Exception as error:
                    error_type = type(error).__name__
                    errors.add(error_type)

    deleted_message = f'\nDone!' if files_deleted else ''

    if errors:
        deleted_message += f'Errors were encountered when deleting files: {", ".join(errors)}'

    print(f'{deleted_message}\n')
