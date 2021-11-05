import os
import sys
import re


def find_csv_file(input_folder):
    file_list = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    if len(file_list) == 0:
        print(f'Error: No .txt files found in {input_folder}')
        sys.exit()
    elif len(file_list) > 1:
        print(f'Error: Multiple .csv files found in {input_folder}')
    else:
        return f'{input_folder}/{file_list[0]}'


def find_text_file(input_folder):
    file_list = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    if len(file_list) == 0:
        print(f'Error: No .txt files found in {input_folder}')
        sys.exit()
    elif len(file_list) > 1:
        print(f'Error: Multiple .txt files found in {input_folder}')
    else:
        return f'{input_folder}/{file_list[0]}'


def find_header(file_path):
    # Specify the first few characters of the row containing the variable names
    header_line_start = '# STN'
    with open(file_path, 'r') as f:
        skip_lines = 0
        for line in f:
            print(line)
            if line.startswith(header_line_start):
                headers = re.sub('[# \n]', '', line)
            if line.startswith('#'):
                skip_lines += 1
            else:
                break
    try:
        return headers.split(','), skip_lines
    except NameError:
        print(f'Error: cannot find headers! '
              f'No line starts with {header_line_start}')
        sys.exit()


def check_length(df):
    if len(df) != 8760:
        print(f'Error, missing data. Expected 8760 data points, got {len(df)}')
        sys.exit()


def calculate_profile_fraction(Teff, G2A_TST, G2A_RER, G2A_TOP):
    """
    Calculates the profile fraction for each hour.
    If the effective temperature Teff is lower than the reference temperature
    G2A_TST, the fraction equals (G2A_TST - Teff) * G2A_RER + G2A_TOP
    Otherwise, fraction equals G2A_TOP
    """
    if Teff < G2A_TST:
        fraction = (G2A_TST - Teff) * G2A_RER + G2A_TOP
    else:
        fraction = G2A_TOP

    return fraction
