import csv

from validacao_tpcliente import dadcad_path

risco_ref_path = 'risco.csv'
dacad_path = 'dadcad.csv'
output_path = 'dadcad_risco_ajustado.csv'

risk_mapping = {}
with open(risco_ref_path, mode='r', newline='', encoding='utf-8') as risco_file:
    reader = csv.DictReader(risco_file, delimiter=';')
    for row in reader:
        client_code = row['client_code']
        risk_value = row['risk']
        risk_mapping[client_code] = risk_value


updated_rows = []
with open(dadcad_path, mode='r+', newline='', encoding='utf-8') as dadcad_file:
    reader = csv.DictReader(dadcad_file, delimiter=';')
    fieldnames = reader.fieldnames
    for row in reader:
        client_code = row['client_code']
        if client_code in risk_mapping:
            row['risk'] = risk_mapping[client_code]
        updated_rows.append(row)


with open(output_path, mode='w', newline='', encoding='utf-8') as updated_file:
    writer = csv.DictWriter(updated_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"risco ajustado e salvo em {output_path}")
