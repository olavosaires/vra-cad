import csv

risco_ref_path = 'risco.csv'
dadcad_path = 'dadcad.csv'
output_path = 'dadcad_risco_ajustado.csv'

#COLUNAS - ARQUIVO REFERÊNCIA
coluna_codigo_referencia = 'cliente_col'
coluna_risco_referencia =  'risco_col'

#COLUNAS - ARQUIVO DADCAD
coluna_codigo_dadcad = 'cliente_col_dadcad'
coluna_risco_dadcad = 'risco_col_dadcad'

counter = 0

# Step 1: Build the risk mapping from risco.csv.
# Adjust the column names if needed.
risk_mapping = {}
with open(risco_ref_path, mode='r', encoding='utf-8') as risco_file:
    risk_reader = csv.DictReader(risco_file)
    for risk_row in risk_reader:
        client_code = risk_row[coluna_codigo_referencia]
        risk_value = risk_row[coluna_risco_referencia]
        risk_mapping[client_code] = risk_value

# Step 2: Stream through dadcad.csv one row at a time and write out to a temporary file.
with open(dadcad_path, mode='r', encoding='utf-8') as infile, \
     open(output_path, mode='w', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        client_code = row[coluna_codigo_dadcad]
        # Update risk only if there's a discrepancy.
        if client_code in risk_mapping and row[coluna_risco_dadcad] != risk_mapping[client_code]:
            row[coluna_risco_dadcad] = risk_mapping[client_code]
        writer.writerow(row)
        counter = counter + 1
        print(f"Progress: {counter}", end='\r', flush=True)

print(f"dadcad atualizado salvo em {output_path}")

