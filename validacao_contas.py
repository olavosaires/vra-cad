# !/usr/bin/env python3
# É para rodar nos 9mi
# [1]-Verificar se todas conta da RECON estão no DADCAD
# [2]-Se faltar conta no DADCAD aponta quais estão faltando
# [3]-Se no DADCAD tiver mais contas do que na RECON, apontar quais são as contas

import csv
import tkinter as tk
from tkinter import ttk

encoding = 'utf-8'

dadcad_path = 'DADCAD.csv'
dadcad_code = 'CodigoCliente'
dadcad_data = 'DataCadastro'
recon_path = 'RECON.csv'
recon_code = 'cd_cliente'
recon_data = 'dt_criação'

def read_recon_file(filename):
    """
    Reads the RECON CSV file (with delimiter ';') and returns a dictionary
    mapping each 'code' to its corresponding 'dt_criação' date.
    """
    records = {}
    try:
        with open(filename, newline='', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                code = row.get(recon_code, '').strip()
                date = row.get(recon_data, '').strip()
                if code:
                    records[code] = date
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return records


def read_dadcad_file(filename):
    """
    Reads the DADCAD CSV file (using the default comma delimiter) and returns a dictionary
    mapping each 'dadcadcode' to its corresponding 'DataCadastro' date.
    """
    records = {}
    try:
        with open(filename, newline='', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                code = row.get(dadcad_code, '').strip()
                date = row.get(dadcad_data, '').strip()
                if code:
                    records[code] = date
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return records


def process_files(progress_bar, root):
    """
    Processes the CSV files to identify differences between RECON and DADCAD records,
    generates a log CSV file with three columns (codigo, data, direcao), and updates
    the progress bar during processing.
    """
    # Reset progress bar.
    progress_bar['value'] = 0
    root.update_idletasks()

    # Step 1: Read RECON file.
    recon_records = read_recon_file(recon_path)
    progress_bar['value'] = 30
    root.update_idletasks()

    # Step 2: Read DADCAD file.
    dadcad_records = read_dadcad_file(dadcad_path)
    progress_bar['value'] = 60
    root.update_idletasks()

    # Step 3: Identify differences.
    # For records in RECON that are not in DADCAD (direction 'RD')
    missing_in_dadcad = {code: date for code, date in recon_records.items() if code not in dadcad_records}
    # For records in DADCAD that are not in RECON (direction 'DR')
    missing_in_recon = {code: date for code, date in dadcad_records.items() if code not in recon_records}

    progress_bar['value'] = 80
    root.update_idletasks()

    # Step 4: Write the log CSV file with columns: codigo, data, direcao.
    log_filename = "validacao_contas_report.csv"
    try:
        with open(log_filename, "w", newline='', encoding=encoding) as logfile:
            writer = csv.writer(logfile)
            writer.writerow(["codigo", "data", "direcao"])
            # Write missing records from RECON: direction 'RD'
            for code in sorted(missing_in_dadcad):
                writer.writerow([code, missing_in_dadcad[code], "RD"])
            # Write missing records from DADCAD: direction 'DR'
            for code in sorted(missing_in_recon):
                writer.writerow([code, missing_in_recon[code], "DR"])
    except Exception as e:
        print(f"Error writing the log file: {e}")

    progress_bar['value'] = 100
    root.update_idletasks()


def main():
    # Create the main window.
    root = tk.Tk()
    root.title("CSV Log Generator")

    # Create a frame for the progress bar and button.
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Create and pack the progress bar.
    progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=5)

    # Create and pack the "Run Verification" button.
    run_button = tk.Button(frame, text="Run Verification",
                           command=lambda: process_files(progress_bar, root))
    run_button.pack(pady=5)

    # Start the Tkinter main event loop.
    root.mainloop()


if __name__ == '__main__':
    main()