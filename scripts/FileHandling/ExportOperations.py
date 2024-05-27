# -*- coding: utf-8 -*-

import csv
import json
import sqlite3


def export_to_csv(args, data_found):
    with open(args.csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['tipo de dado', 'arquivos'])

        for data_type, file_list in data_found.items():
            if file_list:
                for info in file_list:
                    if args.findme:
                        csv_writer.writerow([data_type, info['file']])
                    else:
                        csv_writer.writerow([data_type, info])


def export_to_json(args, data_found):
    with open(args.json, 'w') as json_file:
        json_data = {}
        for table_name, file_list in data_found.items():
            json_data[table_name] = []
            for info in file_list:
                if args.findme:
                    json_data[table_name].append(info['file'])
                else:
                    json_data[table_name].append(info)
        json.dump(json_data, json_file, indent=4)


def export_to_text(args, data_found):
    with open(args.text, 'w') as output_file:
        for data_type, file_list in data_found.items():
            if file_list:
                print(f'\n<{data_type}>\n\n', file=output_file)
                if args.findme:
                    for info in file_list:
                        print(info['file'], file=output_file)
                else:
                    for info in file_list:
                        print(info, file=output_file)


def export_to_database(args, data_found):
    conn = sqlite3.connect(args.database)
    cursor = conn.cursor()
    for table_name, file_list in data_found.items():
        if file_list:
            cursor.execute(f'''CREATE TABLE "{table_name}" (arquivos TEXT)''')
            for info in file_list:
                if args.findme:
                    cursor.execute(f'''INSERT INTO "{table_name}" (arquivos) VALUES (?)''', (info['file'],))
                else:
                    cursor.execute(f'''INSERT INTO "{table_name}" (arquivos) VALUES (?)''', (info,))
    conn.commit()
    conn.close()
