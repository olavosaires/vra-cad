# !/usr/bin/env python3
# É para rodar nos 9mi
# [1]-Verificar se todas conta da RECON estão no DADCAD
# [2]-Se faltar conta no DADCAD aponta quais estão faltando
# [3]-Se no DADCAD tiver mais contas do que na RECON, apontar quais são as contas

import csv
import tkinter as tk
from tkinter import ttk

dadcad_path = 'DADCAD.csv'
dadcad_code = 'CodigoCliente'
recon_path = 'RECON.csv'
recon_code = 'cd_cliente'


def read_csv_column(filename, column_name, delimiter=','):
    """
    Reads a CSV file and returns a set of values from the specified column.

    :param filename: Name of the CSV file.
    :param column_name: Column header to extract values from.
    :param delimiter: The delimiter used in the CSV file.
    :return: A set of values from the column.
    """
    values = set()
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                # Only add non-empty values.
                if row.get(column_name):
                    values.add(row[column_name].strip())
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return values


def process_files(progress_bar, output_text, root):
    """
    Processes the CSV files, updating the progress bar and writing output to
    the provided text widget.
    """
    # Clear output text area
    output_text.delete("1.0", tk.END)

    # Reset progress bar to 0%
    progress_bar['value'] = 0
    root.update_idletasks()

    # Step 1: Read RECON file (using ";" as delimiter)
    output_text.insert(tk.END, "Reading RECON file...\n")
    recon_codes = read_csv_column(recon_path, recon_code, delimiter=';')
    progress_bar['value'] = 33
    root.update_idletasks()

    # Step 2: Read DADCAD file (using default comma delimiter)
    output_text.insert(tk.END, "Reading DADCAD file...\n")
    dadcad_codes = read_csv_column(dadcad_path, dadcad_code, delimiter=';')
    progress_bar['value'] = 66
    root.update_idletasks()

    # Step 3: Compare codes from both files.
    output_text.insert(tk.END, "Comparing records...\n")
    missing_in_dadcad = recon_codes - dadcad_codes
    if missing_in_dadcad:
        output_text.insert(tk.END, "The following codes from RECON are missing in DADCAD:\n")
        for code in sorted(missing_in_dadcad):
            output_text.insert(tk.END, f"  - {code}\n")
    else:
        output_text.insert(tk.END, "All codes from RECON are present in DADCAD.\n")

    # Check for extra codes in DADCAD (i.e. if DADCAD has more entries)
    if len(dadcad_codes) > len(recon_codes):
        missing_in_recon = dadcad_codes - recon_codes
        if missing_in_recon:
            output_text.insert(tk.END, f"\nThere are {len(missing_in_recon)} code values from DADCAD not found in RECON:\n")
            for code in sorted(missing_in_recon):
                output_text.insert(tk.END, f"  - {code}\n")
    else:
        output_text.insert(tk.END, "\nNo extra dadcadcode values in DADCAD compared to RECON.\n")

    # Final update of progress bar to 100%
    progress_bar['value'] = 100
    root.update_idletasks()


def main():
    # Create the main window.
    root = tk.Tk()
    root.title("CSV Code Verifier")

    # Create a frame to hold the progress bar and run button.
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Create and pack the progress bar.
    progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=5)

    # Create a text widget to display the output.
    output_text = tk.Text(root, width=80, height=20)
    output_text.pack(padx=10, pady=10)

    # Create and pack the run button.
    run_button = tk.Button(frame, text="Run Verification",
                           command=lambda: process_files(progress_bar, output_text, root))
    run_button.pack(pady=5)

    # Start the Tkinter event loop.
    root.mainloop()


if __name__ == '__main__':
    main()