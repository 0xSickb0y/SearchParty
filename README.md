# SearchParty #

![SearchParty_en-us](https://github.com/0xSickb0y/SearchParty/assets/148525929/e4613b05-6066-42d2-8083-6c124bd1b49d)

## Intro ##
 _**SearchParty**_ is a tool developed as part of the [FIAP](https://www.fiap.com.br) Challenge project for the mid-year Cyber-Defense classes on 2023.

Its primary purpose is to find personal and sensitive data within the file system.

## Description

The tool iterates over the provided input, categorizing files based on their MIME types. Each type is organized into a list for further processing.

Subsequently, an extraction method is initiated for each file type, with each method representing a member of a _Search Party_.

The extraction methods use regular expressions and keywords to examine the text extracted from the files, searching for matches with the supported data types.

Upon completion, the user receives a comprehensive mapping of files containing PII/Sensitive data.

Additionally, the tool provides practical file management features, enabling users to copy, move, or delete files according to their findings.

## Disclaimer

1. MIME types

    - SearchParty relies on the libmagic library for file type identification.

    - On Windows systems, it is recommended to use the [python-magic-bin](https://pypi.org/project/python-magic-bin/) module, which provides a Python interface to libmagic using ctypes.

    - A _requirements_ file has already been created for both cases:
        
        `requirements_UNIX.txt`
        
        `requirements_WINDOWS.txt`

2. OCR

    - SearchParty relies on the [Tesseract](https://github.com/tesseract-ocr/tesseract) engine for Optical Character Recognition.

    - Make sure you have Tesseract installed and properly configured on your system before utilizing OCR capabilities.

    - To enable OCR functionality, use the `--enable-ocr` option.

3. Color Formatting

    - Certain terminal environments may not support Colorama for color formatting.

    - you can disable it by using the `--no-colors` option.

4. Export Operations

    - Before performing any export operations, SearchParty checks for permissions in the destination paths.

    - Ensure that the destination has write permissions before trying to export results.

5. File Operations

    - For file operations such as copying, moving, and deleting, SearchParty also verifies the permissions of the source files and the destination directory. 

    - Insufficient permissions may lead to unexpected behavior during operations, resulting in potential errors or incomplete tasks.

6. Languages

    - SearchParty is designed to focus on data specific to Brazilian Portuguese.

    - This branch was created for users who feel more confortable using the tool in English (US).

    - If you want the version in Portuguese, use the [pt-br](https://github.com/0xSickb0y/SearchParty/tree/pt-br) branch.

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
- **.mbox**: message/rfc822

## Supported Data Types

- **CPF** (Social Security Number)
- **RG** (General Registration)
- **NIT** (Employee ID)
- **CNS** (National Health Card)
- **Email Dddresses**
- **Phone Numbers**
- **Ethnic Groups**
- **Financial Information**
- **Legal Information**
- **Medical Records**
- **Political Preferences**
- **Vehicle Documents**
- **Gender Orientation**
- **Property Information**
- **Religion and Faith**
- **Travel History**

## Available Output Formats

- **csv**
- **json**
- **text**
- **stdout**
- **database**

## Options

```
  -h, --help            show this help message and exit
  -F path               scan file
  -D path               scan directory
  -sV  [ ...]           search for specific values
  --data-type type      data type filtering
  --file-type type      file type filtering
  --to-csv [name]       save results to csv
  --to-json [name]      save results to json
  --to-text [name]      save results to text
  --to-database [name]  save results to a database
  --copy-files [dst]    copy files to another location
  --move-files [dst]    move files to another location
  --delete-files        delete files from the file system
  --no-colors           disable color formatting in the output
  --enable-ocr          enable optical character recognition
```

## Usage

---

### Scanning a directory:
    
    python SearchParty.py -D /path/to/directory

This command will scan through the specified directory and analyze the content of all files within it. Any data matching the predefined search patterns will mapped accordingly.

The `-D` option can be used multiple times (i.e. scan multiple directories at once)

---

### Scanning a file:

    python SearchParty.py -F /path/to/myfile.txt

This command will scan the specific file `myfile.txt` and analyze its content. Any data matching the predefined search patterns will mapped accordingly.

The `-F` option can be used multiple times (i.e. scan multiple files at once)

---

### Search for specific values:

    python SearchParty.py -sV 'John Doe' '47.283.723-0'

This command will search for specific values ('John Doe' and '47.283.723-0') within the content of files. If any matches are found, the tool will map the corresponding data.

This option is particularly useful for mapping data related to a specific individual, identifying sensitive information such as personal names, identification numbers, or any other predefined data patterns.

The more values you provide, the more comprehensive the mapping and categorization process becomes, allowing for a thorough analysis of the data content.

---

### Filtering data types:

    python SearchParty.py --data-type cpf,rg


This command will specify the data types to search for during the scan. Only data matching the specified types (e.g., CPF and RG numbers) will be mapped. (This option currently works only for the regular expressions)

The filters must be separated by commas and should not have any spaces in between.

Filters: `cpf  rg  email  phone  nit  cns`

---

### Filtering file types:

    python SearchParty.py --file-type pdf,docx

This command will specify the types of files to include in the scan. Only files with the specified extensions (e.g., PDF and DOCX) will be analyzed for data extraction.

The filters must be separated by commas and should not have any spaces in between.

Filters: `txt  csv  bmp  png  gif  pdf  tiff  jpeg  webp  docx  xlsx  pptx  mail`

---

### Save results to a csv file:

    python SearchParty.py --to-csv | python SearchParty.py --to-csv /path/to/results.csv | python SearchParty.py --to-csv /path/to/results

This command will save the scan results in comma separated values. You can specify a destination folder, a destination file, or leave it empty.

Leaving the option as the default value will save the results to `HOSTNAME.csv` under the current directory.

If you provide a destination file, the scan results will be saved directly to that file.

If you specify a destination folder, the results file will be located under that directory as: `HOSTNAME.csv`.

This option is useful for exporting results in a format that can be easily opened and manipulated in spreadsheet software.

---

### Save results to a json file:

    python SearchParty.py --to-json | python SearchParty.py --to-json /path/to/results.json | python SearchParty.py --to-json /path/to/results

This command will save the scan results in json. You can specify a destination folder, a destination file, or leave it empty.

Leaving the option as the default value will save the results to `HOSTNAME.json` under the current directory.

If you provide a destination file, the scan results will be saved directly to that file.

If you specify a destination folder, the results file will be located under that directory as: `HOSTNAME.json`.

This option is useful for exporting results in a structured format that can be easily processed and analyzed programmatically.

---

### Save results to a text file:

    python SearchParty.py --to-text | python SearchParty.py --to-text /path/to/results.txt | python SearchParty.py --to-text /path/to/results

This command will save the scan results in raw text. You can specify a destination folder, a destination file, or leave it empty.

Leaving the option as the default value will save the results to `HOSTNAME.txt` under the current directory.

If you provide a destination file, the scan results will be saved directly to that file.

If you specify a destination folder, the results file will be located under that directory as: `HOSTNAME.txt`.

This option allows for saving results in a simple, human-readable format, which can be easily viewed and edited using any text editor.

---

### Save results to a database:

    python SearchParty.py --to-database | python SearchParty.py --to-database /path/to/results.db | python SearchParty.py --to-database /path/to/results

This command will save the scan results in sqlite database. You can specify a destination folder, a destination file, or leave it empty.

Leaving the option as the default value will save the results to `HOSTNAME.db` under the current directory.

If you provide a destination file, the scan results will be saved directly to that file.

If you specify a destination folder, the results file will be located under that directory as: `HOSTNAME.db`.

This option is particularly useful for storing results in a structured and scalable manner, allowing for efficient data management and analysis using database management systems.

If you're using SearchParty on multiple hosts, it's highly recommended to leave the database name as the default value. This makes it easier to identify which database is associated with each machine.

---

### Copying files:

    python SearchParty.py --copy-files /path/to/destination

This command will copy files containing PII/Sensitive data to the specified destination `/path/to/destination`.

The original files will remain unchanged, and copies containing relevant data will be created in the destination directory under `CopiedFiles/`.

---

### Moving files:

    python SearchParty.py --move-files /path/to/destination


This command will move files containing PII/Sensitive data to the specified destination `/path/to/destination`.

The original files will be deleted from their current location and moved to the destination directory under `MovedFiles/`.

---

### Deleting files:

    python SearchParty.py --delete-files

This command will delete the files that contain PII/Sensitive data.

Exercise caution when using this option, as it will permanently remove the files from the file system.

---

### Disabling color formatting:

    python SearchParty.py --no-colors

    
Use this option to disable color formatting in the output.

This can be useful in environments where color formatting is not supported or preferred.

---

### Enabling optical character recognition:

    python SearchParty.py --enable-ocr

This option activates optical character recognition (OCR). This functionality allows the program to analyze text within images.

SearchParty will automatically attempt to locate the Tesseract binary on your system, ensure that it is installed and properly configured for OCR to work effectively.

---

## Outro

A Graphical User Interface (GUI) is currently under development as an  alternative to the command-line interface (CLI). This option aims to provide a more intuitive and user-friendly experience, simplifying the process of scanning, analyzing, and managing data for users unfamiliar with the command-line.
