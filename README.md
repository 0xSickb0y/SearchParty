# SearchParty #

![SearchParty_pt-br](https://github.com/0xSickb0y/SearchParty/assets/148525929/b237014f-520b-4cdc-b95a-14127ee7f3ff)

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

Para reconhecimento óptico de caracteres (OCR), o SearchParty utiliza a engine [Tesseract](https://github.com/tesseract-ocr/tesseract) para análise OCR. Certifique-se de ter o Tesseract instalado e configurado corretamente no seu sistema antes de usar o SearchParty.

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
- **Informações sobre imóveis e propiedade**
- **Religião e fé**
- **Histórico de viagens**

## Opções
```
  -h, --help            show this help message and exit
  -F $file              escanear arquivo
  -D $directory         escanear diretório
  --find  [ ...]        procurar valores específicos ('John Doe' '47.283.723-0')
  --loot [$name]        salvar resultados em um diretório (default: $current/loot)
  --database [$sql.db]  salvar resultados em um banco de dados (default: $hostname.db)
  --data-type $type     tipos de dados separados por vírgula
  --file-type $type     tipos de arquivos separados por vírgula
  --copy-files $dst     copiar arquivos para outro local
  --move-files $dst     mover arquivos para outro local
  --delete-files        excluir arquivos do sistema de arquivos
```
## Uso

Executando a ferramenta:

    python SearchParty.py [-h] [-F $file] [-D $directory] [--find  [...]] [--loot [$name]] [--database [$sql.db]] [--data-type $type] [--file-type $type] [--copy-files $dst] [--move-files $dst] [--delete-files]

---

Escaneando um diretório:
    
    python SearchParty.py -D /caminho/para/diretório

Este comando irá percorrer o diretório especificado e analisar o conteúdo de todos os arquivos dentro dele. Qualquer dado que corresponda aos padrões de pesquisa predefinidos será extraído e categorizado conforme necessário.

---

Escaneando um arquivo:

    python SearchParty.py -F /caminho/para/myfile.txt

Este comando irá escanear o arquivo específico `myfile.txt` e analisar seu conteúdo. A ferramenta extrairá quaisquer dados que correspondam aos padrões de pesquisa predefinidos encontrados dentro do arquivo.

---

Buscar por valores específicos:

    python SearchParty.py --find 'John Doe' '47.283.723-0'

Este comando buscará por valores específicos ('John Doe' e '47.283.723-0') dentro do conteúdo dos arquivos. Se houver correspondências, a ferramenta irá extrair e categorizar os dados correspondentes.

---

Salvar resultados em arquivos de texto:

    python SearchParty.py --loot /caminho/para/resultados | python SearchParty.py --loot

Este comando irá salvar os resultados da varredura no diretório especificado `/caminho/para/resultados`. Os dados extraídos serão organizados e armazenados em arquivos dentro deste diretório. Se nenhum caminho de destino for fornecido, os resultados serão salvos no diretório atual sob `loot/*.txt`

---

Salvar resultados em um banco de dados:

    python SearchParty.py --database banco_de_dados.db | python SearchParty.py --database

Este comando irá salvar os resultados da varredura em um banco de dados SQLite chamado `banco_de_dados.db`. Cada entrada de dado extraída será armazenada como um registro no banco de dados, permitindo consultas e análises fáceis. Se nenhum caminho de destino for fornecido, os resultados serão salvos no diretório atual sob `$HOSTNAME.db`. É altamente recomendável deixar o nome do banco de dados como o nome do host, isso torna mais fácil identificar qual banco de dados está associado a cada máquina.

---

Filtrando tipos de dados:

    python SearchParty.py --data-type 'Cadastro de pessoa física','Cartão nacional de saúde'

Este comando especificará os tipos de dados a serem pesquisados durante a varredura. Apenas dados que correspondam aos tipos especificados (por exemplo, números de CPF e RG) serão extraídos e categorizados. (Esta opção atualmente funciona apenas para as expressões regulares)

---

Filtrando tipos de arquivo:

    python SearchParty.py --file-type pdf,docx

Este comando especificará os tipos de arquivos a serem incluídos na varredura. Apenas arquivos com as extensões especificadas (por exemplo, PDF e DOCX) serão analisados para extração de dados.

---

Copiando arquivos:

    python SearchParty.py --copy-files /caminho/para/destino

Este comando copiará arquivos contendo dados extraídos para o diretório de destino especificado `/caminho/para/destino`. Os arquivos originais permanecerão inalterados, e cópias contendo dados relevantes serão criadas no diretório de destino.

---

Movendo arquivos:

    python SearchParty.py --move-files /caminho/para/destino

Este comando moverá arquivos contendo dados extraídos para o diretório de destino especificado `/caminho/para/destino`. Os arquivos originais serão excluídos de sua localização atual e movidos para o diretório de destino.

---

Excluindo arquivos:

    python SearchParty.py --delete-files

Este comando excluirá arquivos do sistema de arquivos após extrair dados deles. Tenha cuidado ao usar esta opção, pois ela removerá permanentemente arquivos contendo dados extraídos do sistema de arquivos.

## Outro

Uma Interface Gráfica (GUI) está atualmente em desenvolvimento como uma alternativa à interface de linha de comando (CLI). Esta opção tem como objetivo fornecer uma experiência mais intuitiva e amigável ao usuário, simplificando o processo de escaneamento, análise e gerenciamento de dados.
