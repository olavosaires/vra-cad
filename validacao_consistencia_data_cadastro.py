import csv
from datetime import datetime

input_file_name = 'dadcad_input_file.csv'
output_file_name = 'output_consistencia_data_cadastro.csv'

coluna_cadastro = 'DataCadastro'
coluna_atualizacao_cadastral = 'DataAtualizacaoCadastral'
cod_cliente = 'CodigoCliente'

contador = 0

with open(input_file_name, mode='r', encoding='utf-8', newline='') as infile, \
     open(output_file_name, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile, delimiter=';')

    fieldnames = [cod_cliente, coluna_cadastro, coluna_atualizacao_cadastral]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for row in reader:
        contador += 1
        # Verificar se DataAtualizacaoCadastral é igual ou posterior a dataCadastro
        # Datas precisam estar formatadas em ISO YYYY-MM-DD
        try:
            data_cadastro = datetime.strptime(row.get(coluna_cadastro), "%Y-%m-%d")
            data_atualizacao = datetime.strptime(row.get(coluna_atualizacao_cadastral), "%Y-%m-%d")

            if data_atualizacao < data_cadastro:
                writer.writerow({
                    cod_cliente: row.get(cod_cliente),
                    coluna_cadastro: row.get(coluna_cadastro),
                    coluna_atualizacao_cadastral: row.get(coluna_atualizacao_cadastral)
                })
        except ValueError:
            # Log formato inválido
            print(f"Cliente {row.get(cod_cliente)}: erro ao converter data(s) -> cadastro: {row.get(coluna_cadastro)}, \
            atualizacao: {row.get(coluna_atualizacao_cadastral)}")

        if contador%10000==0:
            print(f"Progress: {contador}", end='\r', flush=True)

print("Validação concluída. Registros com datas inconsistentes foram salvos em: ", output_file_name)