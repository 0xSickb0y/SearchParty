# -*- coding: utf-8 -*-

import os
import time
import argparse
import datetime
from scripts import main

banner = r'''
   _____                      __       ____             __
  / ___/___  ____  ____ _____/ /_     / __ \____  _____/ /___  __
  \__ \/ _ \/ __ `/ ___/ ___/ __ \   / /_/ / __ `/ ___/ __/ / / /
 ___/ /  __/ /_/ / /  / /__/ / / /  / ____/ /_/ / /  / /_/ /_/ /
/____/\___/\__,_/_/   \___/_/ /_/  /_/    \__,_/_/   \__/\__  /
                                                         /___/
v1.0

Ferramenta offline para mapeamento e análise de dados pessoais/sensíveis
https://github.com/0xSickb0y/SearchParty/
'''

parser = argparse.ArgumentParser(
    prog='SearchParty.py',
    description=print(banner),
    allow_abbrev=False,
    epilog='')


def separate_args(arguments):
    return arguments.split(',')


parser.add_argument('-F', metavar="path", dest='file', action='append', help='escanear arquivo')
parser.add_argument('-D', metavar="path", dest='directory', action='append', help='escanear diretório')
parser.add_argument('-sV', metavar='', dest='findme', type=str, nargs='+', help="procurar valores específicos")
parser.add_argument('--data-type', metavar='type', dest='data_filters', type=separate_args, help='filtrar tipo de dados')
parser.add_argument('--file-type', metavar='type', dest='file_filters', type=separate_args, help='filtrar tipo de arquivos')
parser.add_argument('--to-csv', metavar="name", dest='csv', nargs='?', const=os.getcwd(), help='salvar resultados em csv')
parser.add_argument('--to-json', metavar="name", dest='json', nargs='?', const=os.getcwd(), help='salvar resultados em json')
parser.add_argument('--to-text', metavar="name", dest='text', nargs='?', const=os.getcwd(), help='salvar resultados em texto')
parser.add_argument('--to-database', metavar='name', dest='database', nargs='?', const=os.getcwd(), help='salvar resultados em um banco de dados')
parser.add_argument('--copy-files', metavar='dst', dest='copy', nargs='?', const=os.getcwd(), help='copiar arquivos para outro local')
parser.add_argument('--move-files', metavar='dst', dest='move', nargs='?', const=os.getcwd(), help='mover arquivos para outro local')
parser.add_argument('--delete-files', dest='delete', action="store_true", help='excluir arquivos do sistema de arquivos')
parser.add_argument('--no-colors', dest='no_colors', action='store_true', help='desativar a formatação de cores na saída')
parser.add_argument('--enable-ocr', dest='ocr_enabled', action='store_true', help='ativar o reconhecimento óptico de caracteres')

args = parser.parse_args()

start_time = time.time()

if __name__ == '__main__':
    if not args.no_colors:
        main(args, parser, colors=True)
    else:
        main(args, parser, colors=False)

end_time = time.time()

print(f'Tempo total de execução: {datetime.timedelta(seconds=end_time - start_time)}')
