# SearchParty #

![SearchParty_en-us](https://github.com/0xSickb0y/SearchParty/assets/148525929/f2bdf931-cc06-4837-bbff-fe213aa3dcc6)

## Intro

_**SearchParty**_ é uma ferramenta desenvolvida como parte do projeto [FIAP](http://www.fiap.com.br) Challenge para as turmas de Defesa Cibernética de meio de ano em 2023.

Seu objetivo principal é encontrar dados pessoais e sensíveis no sistema de arquivos.

## Descrição

A ferramenta itera sobre a entrada fornecida, categorizando os arquivos com base em seus tipos MIME. Cada tipo é organizado em uma lista para processamento posterior.

Em seguida, um método de extração é iniciado para cada tipo de arquivo, com cada método representando um membro de uma _Equipe de Busca_.

Os métodos de extração usam expressões regulares e palavras-chave para examinar o texto extraído dos arquivos, procurando correspondências com os tipos de dados suportados.

Durante a execução do programa, os dados são mapeados e, ao término, o usuário recebe um mapeamento compreensivo de sua localização, disponível em formato de banco de dados, arquivos de texto ou saída padrão.

Além disso, a ferramenta oferece recursos práticos de gerenciamento de arquivos, permitindo que os usuários copiem, movam ou excluam arquivos de acordo com os resultados de sua análise.

## Disclaimer

O SearchParty depende da biblioteca libmagic para identificação de tipos de arquivo. Em sistemas Windows, é recomendado usar o módulo [python-magic-bin](https://pypi.org/project/python-magic-bin/), que oferece uma interface para libmagic usando ctypes.

Um arquivo requirements.txt já foi criado para cada sistema:

- Para sistemas baseados em Unix: `requirements_UNIX.txt`
- Para Microsoft Windows: `requirements_WINDOWS.txt`

para reconhecimento óptico de caracteres (OCR), o SearchParty utiliza a engine [Tesseract](https://github.com/tesseract-ocr/tesseract) para análise OCR. Certifique-se de ter o Tesseract instalado e configurado corretamente no seu sistema antes de usar o SearchParty.

Alguns ambientes de terminal podem não suportar o Colorama para formatação de cores. Se encontrar problemas, considere usar o script `SearchParty-NoColors.py`.

## Extensões de arquivo suportadas
- **.txt**: text/plain
- **.csv**: text/csv
- **.bmp**: image/bmp
- **.png**: image/png
- **.gif**: image/gif
- **.tiff**: image/tiff
- **.jpeg**: image/jpeg
- **.webp**: image/webp
- **.docx**: application/vnd.openxmlformats-officedocument.wordprocessingml.document
- **.xlsx**: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- **.pptx**: application/vnd.openxmlformats-officedocument.presentationml.presentation
- **.pdf**: application/pdf
- **.eml**: message/rfc822

## Tipos de dados suportados
- **cpf** (Cadastro de pessoa física)
- **rg** (Registro geral)
- **nit** (Número de identificação do trabalhador)
- **cns** (Cartão nacional de saúde)
- **endereços de e-mail**
- **números de telefone**
- **Grupos étnicos**
- **Informações financeiras**
- **Informações legais**
- **Informações médicas**
- **Preferências políticas**
- **Documentos de veículo**
- **Gênero e orientação sexual**
- **Informações sobre imóveis**
- **Religião e fé**
- **Histórico de viagens**

## Opções
```
  -h, --help            show this help message and exit
  -F $file              scan file
  -D $directory         scan directory
  --find  [ ...]        search for specific values ('John Doe' '47.283.723-0')
  --loot [$name]        save results to a directory (default: $current/loot)
  --database [$sql.db]  save results to a database (default: $hostname.db)
  --data-type $type     data types separated by comma (cpf,rg)
  --file-type $type     file types separated by comma (pdf,docx)
  --copy-files $dst     copy files to another location
  --move-files $dst     move files to another location
  --delete-files        delete files from the file system
```
## Uso

Executando a ferramenta:

    python SearchParty.py [-h] [-F $file] [-D $directory] [--find  [...]] [--loot [$name]] [--database [$sql.db]] [--data-type $type] [--file-type $type] [--copy-files $dst]
                      [--move-files $dst] [--delete-files]
