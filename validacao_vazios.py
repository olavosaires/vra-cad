import csv

input_file_name = 'colunas.csv'
output_file_name = 'output_validacao_vazios.csv'

contador = 0;
contador_blankspace = 0;

blankspace_register = {}
client_code_column = 'CodigoCliente'


with open(input_file_name, mode='r', encoding='utf-8') as infile, \
     open(output_file_name, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile, delimiter=';')
    print(reader.fieldnames)

    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter=';')

    for row in reader:
        contador += 1
        apontamento = False
        for col in reader.fieldnames:
            if row.get(col).isspace():
                apontamento = True
                contador_blankspace += 1
                blankspace_register = {
                    row.get(client_code_column) : col,
                }
            elif row.get(col) == '':
                apontamento = True
                break
            else:
                continue
        if apontamento:
            writer.writerow(row)


        print(f'🔄 guenta aí, to indo: {contador}', end='\r', flush=True)

print('Pronto')
print(f'Blanks: {contador_blankspace}')