import csv

risco_ref_path = 'risco_correto.csv'
dadcad_path = 'dadcadcorrigir_risco.csv'
output_path = 'dadcad_risco_ajustado.csv'

#COLUNAS - ARQUIVO REFERÊNCIA
coluna_codigo_referencia = 'Cod'
coluna_risco_referencia =  'Risco'

#COLUNAS - ARQUIVO DADCAD
coluna_codigo_dadcad = 'CodigoCliente'
coluna_risco_dadcad = 'ClassificacaoRisco'

counter = 0

# Step 1: Read the 'risco' file and load client codes and correct risk values into a dictionary.
risco_mapping = {}
with open(risco_ref_path, newline='', encoding='utf-8') as risco_file:
    reader = csv.reader(risco_file, delimiter=';')
    header_risco = next(reader)  # Assume the first row is a header.
    # Assuming the first column contains client codes and the second contains risk values.
    for row in reader:
        if len(row) < 2:
            continue  # Skip rows that do not have enough columns.
        client_code = row[0]
        risk_value = row[1]
        risco_mapping[client_code] = risk_value

# Step 2: Process the large DADCAD file in chunks.
chunk_size = 50000  # Adjust the chunk size depending on your memory requirements.

with open(dadcad_path, newline='', encoding='utf-8') as infile, open(output_filename, 'w', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Read header row from DADCAD file.
    header = next(reader)

    # Identify the column indices for client code and risk.
    # Modify these conditions if your header names differ.
    client_idx = None
    risk_idx = None
    for i, col in enumerate(header):
        # Checking common possibilities for client code column names.
        if col.strip().lower() == coluna_codigo_dadcad:
            client_idx = i
        # Checking for the risk column.
        if col.strip().lower() == coluna_risco_dadcad:
            risk_idx = i

    # Check if the required columns are found.
    if client_idx is None or risk_idx is None:
        raise ValueError(f"Required columns ('{coluna_codigo_dadcad}' and '{coluna_risco_dadcad}') were not found in the dadcad file header.")

    # Write the header to the output file.
    writer.writerow(header)

    # Process the input file in chunks.
    chunk = []
    for row in reader:
        # Ensure row length is at least as long as header.
        if len(row) < len(header):
            # Optionally, you can handle bad rows or fill missing columns.
            row += [''] * (len(header) - len(row))

        # Update the risk column if the client code is found in the risco mapping.
        client_code = row[client_idx]
        if client_code in risco_mapping:
            row[risk_idx] = risco_mapping[client_code]

        chunk.append(row)

        # Write out the chunk when it reaches the defined chunk_size.
        if len(chunk) >= chunk_size:
            writer.writerows(chunk)
            chunk = []
        counter = counter + 1
        print(f"Progress: {counter}", end='\r', flush=True)

    # Write any remaining rows.
    if chunk:
        writer.writerows(chunk)

print(f"File '{output_path}' has been processed and the updated records were saved to '{output_path}'.")


