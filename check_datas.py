import csv
from datetime import datetime
import sys

# Lista de formatos candidatos.
CANDIDATE_FORMATS = [
    "%Y-%m-%d",  # 2025-04-15 (ISO format)
    "%d/%m/%Y",  # 15/04/2025 (common European)
    #"%m/%d/%Y",  # 04/15/2025 (common US)
    #"%d-%m-%Y",  # 15-04-2025
    #"%m-%d-%Y",  # 04-15-2025
    #"%Y/%m/%d",  # 2025/04/15
]


csv_file = 'file_input.csv'

coluna_a='testeA'
coluna_b='testeB'
coluna_c='testeC'

def detect_date_format(date_str):
    """
    Tenta reconhecer a string de data fornecida com cada formato candidato.
    Retorna o formato correspondente ou None, se nenhum corresponder.
    """
    for fmt in CANDIDATE_FORMATS:
        try:
            datetime.strptime(date_str, fmt)
            return fmt
        except ValueError:
            continue
    return None


def main(date_column):

    # Dictionarios para armazenar contagem de formatos reconhecidos e um contador para formatos desconhecidos
    format_counts = {}
    unknown_count = 0

    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            if not(date_column in reader.fieldnames):
                print(f'Não encontrei coluna \'{date_column}\' no arquivo {csv_file}')
                sys.exit(1)
            for row in reader:
                date_value = row.get(date_column)
                if date_value is None:
                    continue
                date_value = date_value.strip()
                # Tentar detectar formato de data
                detected_format = detect_date_format(date_value)
                if detected_format:
                    format_counts[detected_format] = format_counts.get(detected_format, 0) + 1
                else:
                    unknown_count += 1
    except FileNotFoundError:
        print(f"Erro: Arquivo '{csv_file}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

    # Print out the summary of detected date formats.
    print("Formatos detectados na coluna '{}':".format(date_column))
    if format_counts:
        for fmt, count in format_counts.items():
            print(f"  Formato: {fmt} -> Contagem: {count}")
    else:
        print("  Nenhum formato de data reconhecido.")

    if unknown_count > 0:
        print(f"\n{unknown_count} Registros não correspondem aos formatos selecionados")



if __name__ == "__main__":
    main(coluna_a)
    main(coluna_b)
    main(coluna_c)