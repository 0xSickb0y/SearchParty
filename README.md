# SearchParty #

![SearchParty_en-us](https://github.com/0xSickb0y/SearchParty/assets/148525929/f2bdf931-cc06-4837-bbff-fe213aa3dcc6)

## Intro ##
 _**SearchParty**_ is a tool developed as part of the [FIAP](https://www.fiap.com.br) Challenge project for the 2023 mid-year Cyber-Defense classes.

Its primary purpose is to find personal and sensitive data within the file system.

## Description

The tool iterates over the provided input, categorizing files based on their MIME types. Each type is organized into a list for further processing.

Subsequently, an extraction method is initiated for each file type, with each method representing a member of a _Search Party_.

The extraction methods use regular expressions and keywords to examine the text extracted from the files, searching for matches with the supported data types.

During program execution, the data is mapped, and upon completion, the user receives a comprehensive mapping of its location, available in database format, text files, or standard output.

Additionally, the tool provides practical file management features, enabling users to copy, move, or delete files according to their analysis findings.

## Disclaimer

SearchParty relies on the libmagic library for file type identification. On Windows systems, it is recommended to use the [python-magic-bin](https://pypi.org/project/python-magic-bin/) module, which provides a Python interface to libmagic using ctypes.

A requirements file has already been created for both cases:

- For Unix-based systems: `requirements_UNIX.txt`
- For MS-Windows: `requirements_WINDOWS.txt`

SearchParty utilizes the [Tesseract](https://github.com/tesseract-ocr/tesseract) engine for OCR analysis. Ensure that you have Tesseract installed and configured correctly on your system before using SearchParty.

Please be aware that some terminal environments may not support Colorama for color formatting. If you encounter issues, use the script `SearchParty-NoColors.py`.

##  Supported File Extensions
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

## Supported Data Types
- **cpf** (Cadastro de pessoa física)
- **rg** (Registro geral)
- **nit** (Número de identificação do trabalhador)
- **cns** (Cartão nacional de saúde)
- **email addresses**
- **phone numbers**
- **Ethnic groups**
- **Financial information**
- **Legal information**
- **Medical information**
- **Political preferences**
- **Vehicle documents**
- **Gender and sexual orientation**
- **Property information**
- **Religion and faith**
- **Travel history**

## Options
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

## Usage

Running the tool:

    python SearchParty.py [-h] [-F $file] [-D $directory] [--find  [...]] [--loot [$name]] [--database [$sql.db]] [--data-type $type] [--file-type $type] [--copy-files $dst] [--move-files $dst] [--delete-files]

---

Scanning a directory:
    
    python SearchParty.py -D /path/to/directory

This command will scan through the specified directory and analyze the content of all files within it. Any data matching the predefined search patterns will be extracted and categorized accordingly.

---

Scanning a file:

    python SearchParty.py -F /path/to/myfile.txt

This command will scan the specific file `myfile.txt` and analyze its content. The tool will extract any data matching the predefined search patterns found within the file.

---

Search for specific values:

    python SearchParty.py --find 'John Doe' '47.283.723-0'

This command will search for specific values ('John Doe' and '47.283.723-0') within the content of files. If any matches are found, the tool will extract and categorize the corresponding data.

---

Save results to text files:

    python SearchParty.py --loot /path/to/results | python SearchParty.py --loot

This command will save the results of the scan to the specified directory `/path/to/results`. The extracted data will be organized and stored in files within this directory, if no destination path is provided, the results will be saved in the current directory under `loot/*.txt`

---

Save results to a database:

    python SearchParty.py --database my_database.db | python SearchParty.py --database

This command will save the results of the scan to a SQLite database named `my_database.db`. Each extracted data entry will be stored as a record in the database, allowing for easy querying and analysis. If no destination path is provided, the results will be saved in the current directory under `$HOSTNAME.db`. It is highly recommended to leave the database name as the hostname, as this makes it easier to identify which database is associated with each machine.

---

Filtering data types:

    python SearchParty.py --data-type 'Cadastro de pessoa física','Cartão nacional de saúde'


This command will specify the data types to search for during the scan. Only data matching the specified types (e.g., CPF and RG numbers) will be extracted and categorized. (This option currently works only for the regular expressions)

---

Filtering file types:

    python SearchParty.py --file-type pdf,docx

This command will specify the types of files to include in the scan. Only files with the specified extensions (e.g., PDF and DOCX) will be analyzed for data extraction.

---

Copying files:

    python SearchParty.py --copy-files /path/to/destination

This command will copy files containing extracted data to the specified destination directory `/path/to/destination`. The original files will remain unchanged, and copies containing relevant data will be created in the destination directory.

---

Moving files:

    python SearchParty.py --move-files /path/to/destination


This command will move files containing extracted data to the specified destination directory `/path/to/destination`. The original files will be deleted from their current location and moved to the destination directory.

---

Deleting files:

    python SearchParty.py --delete-files

This command will delete files from the file system after extracting data from them. Exercise caution when using this option, as it will permanently remove files containing extracted data from the file system.


## Outro

A Graphical User Interface (GUI) is currently under development as an  alternative to the command-line interface (CLI). This option aims to provide a more intuitive and user-friendly experience, simplifying the process of scanning, analyzing, and managing data
