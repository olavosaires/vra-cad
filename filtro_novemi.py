import csv
import threading
import tkinter as tk
from tkinter import ttk

# Global variables for progress tracking and output feedback.
total_lines = 0
current_line = 0
matching_count = 0
processing_done = False

input_path = 'dummy_data.csv'
output_path = 'DADCAD.csv'
code_column = 'code'


def count_lines(filepath):
    """Count the total number of lines in the file (including the header)."""
    count = 0
    with open(filepath, 'rb') as f:
        for _ in f:
            count += 1
    return count


def process_csv(input_file, output_file, threshold=9000000):
    """
    Process the CSV file row by row and write rows to the output if their 'code' value is
    greater than or equal to the threshold. Updates the current_line and matching_count globals.
    """
    global total_lines, current_line, matching_count, processing_done

    # Count the lines in the file; subtract one for the header.
    total_lines = count_lines(input_file)
    if total_lines > 0:
        total_lines -= 1  # Exclude header from processing count

    with open(input_file, mode='r', newline='') as infile, \
            open(output_file, mode='w', newline='') as outfile:

        reader = csv.DictReader(infile, delimiter=';')
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter=';')
        writer.writeheader()  # write header row

        # Process each row one at a time.
        for row in reader:
            current_line += 1  # Update processed row count
            try:
                if int(row[code_column]) >= threshold:
                    writer.writerow(row)
                    matching_count += 1  # Increment matching rows counter
            except (ValueError, KeyError):
                # If conversion fails or key is missing, skip the row.
                continue

    processing_done = True


def start_processing():
    """Start processing the CSV in a background thread to avoid UI freezing."""
    thread = threading.Thread(target=process_csv, args=(input_path, output_path), daemon=True)
    thread.start()


def update_progress():
    """Update the progress bar and output feedback label periodically."""
    if total_lines > 0:
        progress_percent = (current_line / total_lines) * 100
        progress_bar['value'] = progress_percent
        feedback_label.config(text=f"Processed {current_line} of {total_lines} rows - Matching rows: {matching_count}")

    if not processing_done:
        root.after(100, update_progress)
    else:
        progress_bar['value'] = 100
        status_label.config(text="Processing complete!")
        feedback_label.config(text=f"Final count: {current_line} rows processed, {matching_count} matching rows.")


# Set up the Tkinter UI.
root = tk.Tk()
root.title("CSV Processing with Output Feedback")

# Progress bar widget.
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

# Label to show main status messages.
status_label = tk.Label(root, text="Ready")
status_label.pack(pady=5)

# Label for detailed output feedback.
feedback_label = tk.Label(root, text="")
feedback_label.pack(pady=5)


# Button to start the CSV processing.
def on_start():
    status_label.config(text="Processing...")
    start_processing()
    update_progress()


start_button = tk.Button(root, text="Start Processing", command=on_start)
start_button.pack(pady=10)

root.mainloop()