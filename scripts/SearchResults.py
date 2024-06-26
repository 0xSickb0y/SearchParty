# -*- coding: utf-8 -*-

import time
from .Utils.ColorFormatting import *
from .FileHandling.FileOperations import copy_files, move_files, delete_files
from .FileHandling.ExportOperations import export_to_csv, export_to_json, export_to_text, export_to_database


def result_stats(args, colors, supported_files, data_found, data_indexes, error_log):
    results_info = f"{display_positive('Análise de dados:', colors)}\n"
    results_info += ''.join([f"\n{key + ':': <30} {value} entradas" for key, value in data_indexes.items() if value != 0]) + '\n'
    results_info += f"{display_positive('Análise de arquivos:', colors)}\n"

    if not (args.findme or args.file):
        results_info += ''.join([f"\n{key + ':': <31}{len(value)} arquivos" for key, value in data_found.items() if value != 0]) + '\n'

    results_info += ''.join([f"\n{str(key).upper() + ':': <7}{len(supported_files[key])} arquivos" for key in supported_files.keys()])

    if sum(error['count'] for error in error_log.values()) != 0:
        results_info += "\n\n"
        results_info += display_negative(f"Erros foram encontrados ao ler {sum(error['count'] for error in error_log.values())} arquivos: ", colors)
        results_info += ''.join([f"\n{str(key).upper()+':': <6}{error['count']}" for key, error in error_log.items()])

    results_info += "\n"
    results_info += display_positive(f"Processo de busca finalizado [{time.strftime('%H:%M:%S %d/%b/%Y')}]", colors)
    return results_info


def results_information(args, colors, data_found):

    if args.findme and (args.directory or args.file):
        arguments_not_found = []
        arguments_found = [argument for argument in args.findme if len(data_found[argument]) != 0]
        for argument in args.findme:
            if argument in arguments_found:
                files_with_keywords = sum(1 for info in data_found[argument] if "keywords" in info)
                print(display_positive(f"{argument} foi encontrado em {len(data_found[argument])} arquivos {f'{files_with_keywords} contém PII/dados sensiveis' if files_with_keywords else ''}\n", colors))
                for info in data_found[argument]:
                    print(info['file'])
                if files_with_keywords:
                    for info in [info for info in data_found[argument] if 'keywords' in info]:
                        print(display_positive(f"Palavras-chave encontradas em  {display_style(info['file'], colors)}\n", colors))
                        for key in (key for key in info['keywords'] if info['keywords'].get(key) and len(info['keywords'].get(key)) != 0):
                            print(f"{key}")
            else:
                arguments_not_found.append(argument)
        if arguments_not_found:
            print()
            for argument in arguments_not_found:
                print(display_negative(f"Nenhuma entrada para {argument} em {', '.join(directory for directory in args.directory) or ', '.join(file_path for file_path in args.file)}", colors))
    else:
        if args.directory:
            for data_type, file_list in data_found.items():
                if file_list:
                    print(display_positive(f"Arquivos contendo {data_type}:\n", colors))
                    for info in file_list:
                        print(info)
        elif args.file:
            for file_path in args.file:
                contains_data = False
                for data_type, file_list in data_found.items():
                    if file_path in file_list:
                        if not contains_data:
                            print(display_positive(f"{file_path} contém:\n", colors))
                            contains_data = True
                        print(data_type)
                if not contains_data:
                    print(display_negative(f"Nenhum dado foi encontrado em: {file_path}", colors))


def export_output(args, colors, supported_files, data_found, data_indexes, error_log):
    print(f'{result_stats(args, colors, supported_files, data_found, data_indexes, error_log)}\n')
    export_option = []
    if args.csv:
        export_to_csv(args, data_found)
        export_option.append(args.csv)
    if args.json:
        export_to_json(args, data_found)
        export_option.append(args.json)
    if args.text:
        export_to_text(args, data_found)
        export_option.append(args.text)
    if args.database:
        export_to_database(args, data_found)
        export_option.append(args.database)
    print(f"Salvando resultados em {display_style(', '.join(export_option), colors)}\n")


def console_output(args, colors, supported_files, data_found, data_indexes, error_log):
    print("\n" + display_alert("Nenhum arquivo de saída especificado, mostrando os resultados no terminal", colors))
    time.sleep(5)
    results_information(args, colors, data_found)
    print(f'{result_stats(args, colors, supported_files, data_found, data_indexes, error_log)}\n')
    if args.copy:
        print(display_info(f"Copiando arquivos para {display_style(os.path.abspath(args.copy), colors)}", colors))
        copy_files(args, data_found)
    if args.move:
        print(display_info(f"Movendo arquivos para {display_style(os.path.abspath(args.move), colors)}", colors))
        move_files(args, data_found)
    if args.delete:
        print(display_info("Deletando arquivos", colors))
        delete_files(args, data_found)


def search_results(args, colors, supported_files, data_found, data_indexes, error_log):
    if args.csv or args.json or args.text or args.database:
        export_output(args, colors, supported_files, data_found, data_indexes, error_log)
    else:
        console_output(args, colors, supported_files, data_found, data_indexes, error_log)
