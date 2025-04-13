import csv
import sys

dadcad_path = 'DADCAD.csv'
dadcad_codigo_col = 'CodigoCliente'
dadcad_tipopessoa_col = 'TipoPessoa'

recon_path = 'RECON.csv'
recon_tpcliente_col = 'TPCliente'
recon_codigo_col = 'cd_cliente'
recon_master_col = 'Codigo_Master'

encoding = 'utf-8'


# TODO: não dá erro se não encontra a coluna, simplesmente da uma saída como se não houvesse discrepancia

def load_dadcad(file_path):
    """
    Loads DADCAD.csv into a dictionary keyed by CodigoCliente.
    """
    dadcad_dict = {}
    try:
        with open(file_path, mode='r', encoding=encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                codigo = row.get(dadcad_codigo_col, "").strip()
                if codigo:
                    dadcad_dict[codigo] = row
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return dadcad_dict


def process_files(recon_file_path, dadcad_file_path, report_file_path):
    """
    Processes the RECON file, computes derived TPCliente values, finds the corresponding record
    in DADCAD (using CodigoCliente), and writes mismatches (or blank/'-' TipoPessoa) to the report.
    """
    # First, load the DADCAD file into a dictionary for quick lookup.
    dadcad_dict = load_dadcad(dadcad_file_path)

    report_rows = []

    try:
        with open(recon_file_path, mode='r', encoding=encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                # Get the raw TPCliente value from RECON and strip any extra whitespace.
                recon_tp = row.get(recon_tpcliente_col, "").strip()
                derived_tp = None
                key_value = None  # will hold the customer key for join

                if recon_tp in ("PF", "PJ"):
                    derived_tp = recon_tp
                    # For PF/PJ, we look for the key in the column "Cd_cliente"
                    key_value = row.get(recon_codigo_col, "").strip()
                    # In case Cd_cliente is not found, check for Cd_Cliente
                    if not key_value:
                        key_value = row.get(recon_codigo_col, "").strip()
                elif recon_tp == "GESTORA":
                    # For GESTORA, compare Cd_Cliente and Código_Master to determine derived_tp.
                    cd_cliente = row.get(recon_codigo_col, "").strip()
                    codigo_master = row.get(recon_master_col, "").strip()
                    derived_tp = "PJF" if cd_cliente == codigo_master else "FI"
                    # Use Cd_Cliente as the key for joining
                    key_value = cd_cliente
                else:
                    # If TPCliente is not one of the expected values, skip the row.
                    continue

                if not key_value:
                    # If there is no customer code, skip this row.
                    continue

                # Find the corresponding row in the DADCAD file using the customer key.
                dadcad_row = dadcad_dict.get(key_value)
                if dadcad_row is None:
                    # Optionally, you could log a warning if no matching customer is found.
                    continue

                # Retrieve the TipoPessoa value from DADCAD.
                dadcad_tp = dadcad_row.get(dadcad_tipopessoa_col, "").strip()

                # Check if TipoPessoa does not match our derived TPCliente value, or if it is blank or "-"
                if dadcad_tp != derived_tp or dadcad_tp in ("", "-"):
                    if dadcad_tp == 'PJNF' and recon_tp == 'PJ':
                        continue
                    else:
                        report_rows.append({
                            "CodigoCliente": dadcad_row.get(dadcad_codigo_col, "").strip(),
                            "TipoPessoa_dadcad": dadcad_tp,
                            "TPCliente_recon": derived_tp
                        })
    except Exception as e:
        print(f"Error processing {recon_file_path}: {e}")

    # Write the output report if discrepancies were found.
    try:
        if report_rows:
            with open(report_file_path, mode='w', encoding=encoding, newline='') as report_file:
                fieldnames = ["CodigoCliente", "TipoPessoa_dadcad", "TPCliente_recon"]
                writer = csv.DictWriter(report_file, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for row in report_rows:
                    writer.writerow(row)
            print(f"Report written to {report_file_path}")
        else:
            print("No discrepancies found.")
    except Exception as e:
        print(f"Error writing report file {report_file_path}: {e}")


if __name__ == "__main__":
    output_report_file = "validacao_tpcliente_report.csv"

    process_files(recon_path, dadcad_path, output_report_file)
