## Uso

Executando a ferramenta:

    python SearchParty.py [-h] [-F $arquivo] [-D $diretório] [--find  [...]] [--loot [$nome]] [--database [$sql.db]] [--data-type $tipo] [--file-type $tipo] [--copy-files $dst] [--move-files $dst] [--delete-files]

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