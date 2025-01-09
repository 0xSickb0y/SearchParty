# SearchParty #

![SearchParty_pt-br](https://github.com/0xSickb0y/SearchParty/assets/148525929/14bd2de4-dcb0-4010-8048-24cf82565666)


## Intro

_**SearchParty**_ é uma ferramenta desenvolvida como parte do projeto [FIAP](http://www.fiap.com.br) Challenge para as turmas de Defesa Cibernética de meio de ano em 2023.

Seu objetivo principal é encontrar dados pessoais e sensíveis no sistema de arquivos.

## Descrição

A ferramenta itera sobre a entrada fornecida, categorizando os arquivos com base em seus tipos MIME. Cada tipo é organizado em uma lista para processamento posterior.

Em seguida, um método de extração é iniciado para cada tipo de arquivo, com cada método representando um membro de uma _Equipe de Busca_.

Os métodos de extração usam expressões regulares e palavras-chave para examinar o texto extraído dos arquivos, procurando correspondências com os tipos de dados suportados.

Após a conclusão, o usuário recebe um mapeamento compreensivo de arquivos contendo PII/dados sensiveis.

Além disso, a ferramenta oferece recursos práticos de gerenciamento de arquivos, permitindo que os usuários copiem, movam ou excluam arquivos de acordo com os resultados.

## Aviso

1. Tipos MIME

    - O SearchParty depende da biblioteca libmagic para identificação de tipos de arquivo.

    - Em sistemas Windows, é recomendado usar o módulo [python-magic-bin](https://pypi.org/project/python-magic-bin/), que fornece uma interface Python para libmagic usando ctypes.

    - Um arquivo _requirements_ já foi criado para ambos os casos:
        
        `requirements_UNIX.txt`
        
        `requirements_WINDOWS.txt`

2. OCR

    - O SearchParty depende da engine [Tesseract](https://github.com/tesseract-ocr/tesseract) para Reconhecimento Óptico de Caracteres.

    - Certifique-se de que o Tesseract está instalado e configurado corretamente no seu sistema antes de utilizar as capacidades de OCR.

    - Para habilitar a funcionalidade OCR, use a opção `-ocr`.

3. Formatação de Cores

    - Certos ambientes de terminal podem não suportar o Colorama para formatação de cores.

    - Você pode desativar essa funcionalidade usando a opção `-dcf`.

4. Operações de Exportação

    - Antes de realizar quaisquer operações de exportação, o SearchParty verifica as permissões nos caminhos de destino: 

        1. O diretório onde o programa está localizado
        2. O diretório _home_ do usuário atual
        3. O diretório _Temp_

    - Certifique-se de que o destino possui permissões de escrita antes de tentar exportar os resultados.

5. Operações de Arquivo

    - Para operações de arquivo, como copiar, mover e excluir, o SearchParty também verifica as permissões dos arquivos de origem e do diretório de destino.

    - Permissões insuficientes podem levar a comportamentos inesperados durante as operações, resultando em erros ou tarefas incompletas.

6. Idiomas

    - SearchParty é projetado para focar em dados específicos do português brasileiro.

    - Uma branch foi criada para usuários que se sentem mais confortáveis usando a ferramenta em inglês (EUA).

    - Se você deseja a versão em inglês, use a branch [en-us](https://github.com/0xSickb0y/SearchParty/tree/en-us).


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
- **.mbox**: message/rfc822


## Tipos de dados suportados

- **Cadastro de pessoa física**
- **Registro geral**
- **Endereços de e-mail**
- **Números de telefone**
- **Grupos étnicos**
- **Informações financeiras**
- **Informações jurídicas**
- **Informações médicas**
- **Preferências políticas**
- **Documentos de veículo**
- **Gênero e orientação sexual**
- **Informações sobre imóveis e propiedade**
- **Religião e fé**
- **Histórico de viagens**

## Opções

```
    -h, --help        show this help message and exit
    -d path           escanear diretório
    -f path           escanear arquivo
    -dcf              desativar a formatação de cores na saída padrão
    -ocr              ativar o reconhecimento óptico de caracteres
    -find  [ ...]     procurar valores específicos
    -save db,csv ...  salvar resultados em [db, csv, txt, json]
    -copy [dst]       copiar arquivos para outro local
    -move [dst]       mover arquivos para outro local
    -delete           excluir arquivos do sistema de arquivos
    -datatype type    filtrar tipo de dados
    -filetype type    filtrar tipo de arquivos
```

## Uso

---

### Escanear um diretório:
    
    python SearchParty.py -d /caminho/para/diretorio

Esse comando percorre o diretório especificado e analisa o conteúdo de todos os arquivos contidos nele. Quaisquer dados que correspondam aos padrões de pesquisa predefinidos serão mapeados adequadamente.

A opção `-d` pode ser usada várias vezes (i.e. escaneie vários diretórios de uma vez).

---

### Escanear um arquivo:

    python SearchParty.py -f /caminho/para/meuarquivo.txt

Esse comando escaneia o arquivo específico `meuarquivo.txt` e analisa seu conteúdo. Quaisquer dados que correspondam aos padrões de pesquisa predefinidos serão mapeados adequadamente.

A opção `-f` pode ser usada várias vezes (i.e. escaneie vários arquivos de uma vez).

---

### Buscar valores específicos:

    python SearchParty.py -find 'João da Silva' '47.283.723-0'

Esse comando busca valores específicos ('João da Silva' e '47.283.723-0') dentro do conteúdo dos arquivos. Se houver correspondências, a ferramenta mapeará os dados correspondentes.

Essa opção é particularmente útil para mapear dados relacionados a um indivíduo específico, identificando informações sensíveis como nomes pessoais, números de identificação ou quaisquer outros padrões de dados predefinidos.

Quanto mais valores você fornecer, mais abrangente se tornará o processo de mapeamento e categorização, permitindo uma análise completa do conteúdo dos dados.

---

### Filtrar tipos de dados:

    python SearchParty.py -datatype cpf,rg

Esse comando especifica os tipos de dados a serem pesquisados durante o scan. Apenas dados que correspondam aos tipos especificados (e.g. números de CPF e RG) serão mapeados. (Essa opção atualmente funciona apenas para as expressões regulares)

Os filtros devem ser separados por vírgulas e não devem ter espaços entre eles.

Filtros: `cpf  rg  email  phone`

---

### Filtrar tipos de arquivos:

    python SearchParty.py -filetype pdf,docx

Esse comando especifica os tipos de arquivos a serem incluídos no scan. Apenas arquivos com as extensões especificadas (e.g. PDF e DOCX) serão analisados para extração de dados.

Os filtros devem ser separados por vírgulas e não devem ter espaços entre eles.

Filtros: `txt  csv  bmp  png  gif  pdf  tiff  jpeg  webp  docx  xlsx  pptx  mail`

---

### Exportando resultados:

    python SearchParty.py -save db,csv,txt,json

Este comando salva os resultados do scan em um formato de arquivo de sua escolha [db, csv, txt, json]

O programa verifica os seguintes diretórios para permissões na ordem listada:

1. O diretório onde o programa está localizado — default.
2. O diretório _home_ do usuário atual($HOME ou %USERPROFILE%)
3. O diretório _Temp_ — Um local de fallback, usado se os caminhos anteriores não estiverem disponíveis.

---

### Copiar arquivos:

    python SearchParty.py -copy /caminho/para/destino

Esse comando copiará arquivos contendo PII/dados sensíveis para o destino especificado `/caminho/para/destino`.

Os arquivos originais permanecerão inalterados, e cópias contendo dados relevantes serão criadas no diretório de destino em `CopiedFiles/`.

---

### Mover arquivos:

    python SearchParty.py -move /caminho/para/destino

Esse comando moverá arquivos contendo PII/dados sensíveis para o destino especificado `/caminho/para/destino`.

Os arquivos originais serão excluídos de sua localização atual e movidos para o diretório de destino em `MovedFiles/`.

---

### Excluir arquivos:

    python SearchParty.py -delete

Esse comando excluirá os arquivos que contêm PII/dados sensíveis.

Exerça cuidado ao usar essa opção, pois ela removerá permanentemente os arquivos do sistema de arquivos.

---

### Desativar formatação de cores:

    python SearchParty.py -dcf

Essa opção desativa a formatação de cores na saída.

Isso pode ser útil em ambientes onde a formatação de cores não é suportada ou preferida.

---

### Habilitar reconhecimento óptico de caracteres:

    python SearchParty.py -ocr

Essa opção ativa o reconhecimento óptico de caracteres (OCR). Essa funcionalidade permite que o programa analise texto dentro de imagens.

O programa tentará localizar automaticamente o executavel Tesseract no seu sistema.

