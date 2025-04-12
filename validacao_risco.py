import csv

file_path = "DADCAD.csv"
dadcad_code = "CodigoCliente"
dadcad_risco = "ClassificacaoRisco"

output_file_path = "validacao_risc_report.csv"

def main():
    matching_rows = []

    # Open the input file for reading with UTF-8 encoding and ';' delimiter
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')

        # Read the header row
        header = next(reader)

        # Find the indices of the relevant columns using our variable names
        try:
            code_index = header.index(dadcad_code)
            risco_index = header.index(dadcad_risco)
        except ValueError:
            print("Required columns not found in the CSV file.")
            return

        # Process each row and check if the dadcad_risco column has a '-' value
        for row in reader:
            if row[risco_index] == "-":
                matching_rows.append([row[code_index], row[risco_index]])

    # Output the filtered data to the new CSV file if any matching rows were found
    if matching_rows:
        with open(output_file_path, mode='w', encoding='utf-8', newline='') as out_file:
            writer = csv.writer(out_file, delimiter=';')
            # Write the header using our defined column names
            writer.writerow([dadcad_code, dadcad_risco])
            # Write the matching rows
            writer.writerows(matching_rows)
        print(f"Found {len(matching_rows)} matching records. Data written to '{output_file_path}'.")
    else:
        print("No matching records found with '-' in the ClassificacaoRisco column.")


if __name__ == "__main__":
    main()