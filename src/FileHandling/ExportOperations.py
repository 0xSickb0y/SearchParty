# -*- coding: utf-8 -*-

import os
import csv
import json
import time
import sqlite3


def get_timestamp_filename(dst_path, extension):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return os.path.abspath(f"{dst_path}/SearchParty-Resultados-{timestamp}{extension}")


def export_to_csv(args, dst_path, data_found):
    filename = get_timestamp_filename(dst_path, '.csv')

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['tipo de dado', 'arquivos'])

        for data_type, file_list in data_found.items():
            if file_list:
                for info in file_list:
                    if args.findme:
                        csv_writer.writerow([data_type, info['file']])
                    else:
                        csv_writer.writerow([data_type, info])


def export_to_json(args, dst_path, data_found):
    filename = get_timestamp_filename(dst_path, '.json')

    with open(filename, 'w') as json_file:
        json_data = {}
        for table_name, file_list in data_found.items():
            json_data[table_name] = []
            for info in file_list:
                if args.findme:
                    json_data[table_name].append(info['file'])
                else:
                    json_data[table_name].append(info)
        json.dump(json_data, json_file, indent=4)


def export_to_text(args, dst_path, data_found):
    filename = get_timestamp_filename(dst_path, '.txt')

    with open(filename, 'w') as output_file:
        for data_type, file_list in data_found.items():
            if file_list:
                print(f'\n<{data_type}>\n\n', file=output_file)
                if args.findme:
                    for info in file_list:
                        print(info['file'], file=output_file)
                else:
                    for info in file_list:
                        print(info, file=output_file)


def export_to_database(args, dst_path, data_found):
    filename = get_timestamp_filename(dst_path, '.db')

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    for table_name, file_list in data_found.items():
        if file_list:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}" (arquivos TEXT)''')
            for info in file_list:
                if args.findme:
                    cursor.execute(f'''INSERT INTO "{table_name}" (arquivos) VALUES (?)''', (info['file'],))
                else:
                    cursor.execute(f'''INSERT INTO "{table_name}" (arquivos) VALUES (?)''', (info,))
    conn.commit()
    conn.close()
