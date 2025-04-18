import csv

input_file_name = 'colunas.csv'
output_file_name = 'output_validacao_vazios.csv'
output_ID_name = 'output_validacao_vazios_ID.csv'

contador = 0;
contador_blankspace = 0;
contador_blank = 0;

blankspace_register = {}
blank_register = {}
client_code_column = 'CodigoCliente'


with open(input_file_name, mode='r', encoding='utf-8') as infile, \
     open(output_file_name, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile, delimiter=';')
    #print(reader.fieldnames)

    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter=';')
    writer.writeheader()

    if not client_code_column in reader.fieldnames:
        print(f'Não encontrei a coluna codigo cliente: {client_code_column}')
        exit(1)


    for row in reader:
        contador += 1
        apontamento = False
        print(f'🔄 guenta aí, to indo: {contador}', end='\r')

        for col in reader.fieldnames:
            if row.get(col).isspace():
                apontamento = True
                contador_blankspace += 1
                blankspace_register = {
                    row.get(client_code_column) : col,
                }
            elif row.get(col) == '':
                contador_blank += 1
                apontamento = True
                blank_register = {
                    row.get(client_code_column) : col,
                }
            else:
                continue
        if apontamento:
            writer.writerow(row)

if blankspace_register or blank_register:
    identifier_fieldnames = ['CodigoCliente', 'ColunaProblema', 'Problema']
    with open(output_ID_name, mode='w', encoding='utf-8', newline='') as out_id:
        writerID = csv.DictWriter(out_id, fieldnames=identifier_fieldnames, delimiter=';')
        writerID.writeheader()

        for client_code, column_name in blank_register.items():
            writerID.writerow({
                'CodigoCliente': client_code,
                'ColunaProblema': column_name,
                'Problema': 'em branco'
            })
        for client_code, column_name in blankspace_register.items():
            writerID.writerow({
                'CodigoCliente': client_code,
                'ColunaProblema': column_name,
                'Problema': 'espaços'
            })

print('\nPronto')
print(f'Blanks:{contador_blank}')
print(f'Blankspaces: {contador_blankspace}')