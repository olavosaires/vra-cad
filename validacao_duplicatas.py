import csv

# CONFIG
input_file = 'dadcad.csv'
output_file = 'output_validacao_duplicados'
column_name = 'CodigoCliente' #Codigo do cliente feverificado

def encontrar_duplicados(input_file, output_file, column_name):
    seen = set()
    duplicates = set()

    # First pass: collect duplicates
    with open(input_file, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        contador = 0
        for row in reader:
            code = row[column_name]
            if code in seen:
                duplicates.add(code)
            else:
                seen.add(code)

            contador += 1
            if contador % 1000 == 0:
                print(f"🔄 buscando duplicados: {contador}", end='\r', flush=True)

    if not duplicates:
        print("Nenhum duplicado encontrado.")
        return

    # Second pass: extract rows with duplicate codes
    with open(input_file, 'r', encoding='utf-8') as csvfile, \
            open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter=';')
        writer.writeheader()

        contador = 0
        for row in reader:
            if row[column_name] in duplicates:
                writer.writerow(row)
            contador += 1
            print(f'✍️ escrevendo duplicados: {contador}', end='\r', flush=True)

    print(f"Duplicates written to: {output_file}")

if __name__ == '__main__':
    encontrar_duplicados(input_file, output_file, column_name)