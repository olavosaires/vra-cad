#!/usr/bin/env python3
"""
This script reads a CSV file and inspects a specified date column to determine the date formats used.
It compares each date string against several candidate format strings using datetime.strptime.
If a candidate format successfully parses the date, that format is recorded.
At the end, the script prints a summary of the detected date formats along with the occurrence counts.
If any date cannot be parsed with the candidate formats, it will be reported as unknown.

Usage:
    python detect_date_formats.py <csv_file> <date_column>
Example:
    python detect_date_formats.py sample.csv date
"""

import csv
from datetime import datetime
import sys

# Define a list of candidate date formats.
# Feel free to extend this list with other common date formats as needed.
CANDIDATE_FORMATS = [
    "%Y-%m-%d",  # 2025-04-15 (ISO format)
    "%d/%m/%Y",  # 15/04/2025 (common European)
    "%m/%d/%Y",  # 04/15/2025 (common US)
    "%d-%m-%Y",  # 15-04-2025
    "%m-%d-%Y",  # 04-15-2025
    "%Y/%m/%d",  # 2025/04/15
    # If you have date-time values, you may add formats such as:
    "%Y-%m-%d %H:%M:%S",  # 2025-04-15 13:45:30
    "%d/%m/%Y %H:%M:%S",  # 15/04/2025 13:45:30
    "%m/%d/%Y %H:%M:%S",  # 04/15/2025 13:45:30
]


def detect_date_format(date_str):
    """
    Attempt to parse the provided date string with each candidate format.
    Return the format string that works or None if none match.
    """
    for fmt in CANDIDATE_FORMATS:
        try:
            datetime.strptime(date_str, fmt)
            return fmt
        except ValueError:
            continue
    return None


def main():

    csv_file = 'file_input.csv'
    date_column = 'column_name'

    # Dictionaries to hold counts of recognized formats and a counter for unknown formats.
    format_counts = {}
    unknown_count = 0

    try:
        with open(csv_file, newline="", encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                # Get the value from the designated column.
                date_value = row.get(date_column)
                if date_value is None:
                    continue
                date_value = date_value.strip()
                # Try to detect the date format.
                detected_format = detect_date_format(date_value)
                if detected_format:
                    format_counts[detected_format] = format_counts.get(detected_format, 0) + 1
                else:
                    unknown_count += 1
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Print out the summary of detected date formats.
    print("Detected date formats in column '{}':".format(date_column))
    if format_counts:
        for fmt, count in format_counts.items():
            print(f"  Format: {fmt} -> Count: {count}")
    else:
        print("  No recognized date formats found.")

    if unknown_count > 0:
        print(f"\nThere were {unknown_count} entries that did not match any candidate format.")


if __name__ == "__main__":
    main()
