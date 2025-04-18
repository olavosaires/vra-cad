import csv

input_file_name = 'colunas.csv'
output_file_name = 'output_validacao_vazios.csv'

contador = 0;

with open(input_file_name, mode='r', encoding='utf-8') as infile, \
     open(output_file_name, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile, delimiter=';')
    print(reader.fieldnames)

    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter=';')

    for row in reader:
        contador += 1
        for col in reader.fieldnames:
            if row.get(col) == '':
                writer.writerow(row)
                break
        print(f'🔄 guenta aí, to indo: {contador}', end='\r', flush=True)

print('Pronto')