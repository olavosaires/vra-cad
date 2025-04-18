import csv

input_file_name = 'colunas.csv'
output_file_name = 'output_validacao_vazios.csv'

colunas_mandatorias = ['col2','col3','col4']


contador = 0;

with open(input_file_name, mode='r', encoding='utf-8') as infile, \
     open(output_file_name, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile, delimiter=';')
    print(reader.fieldnames)

    write_fieldnames = reader.fieldnames

    writer = csv.DictWriter(outfile, fieldnames=write_fieldnames, delimiter=';')

    for row in reader:
        contador += 1
        for col in colunas_mandatorias:
            if row.get(col) == '':
                writer.writerow(row)
                break
        print(f'🔄 indo: {contador}', end='\r', flush=True)

print('Pronto')