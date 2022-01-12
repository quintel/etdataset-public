'''
Aggegrates a curve based on all irradiation curves in a subfolder ('offshore')
of the countries 'input' data folder.
'''

import sys
from pathlib import Path

import pandas as pd
import numpy as np

from process_irradiation_data import normalize, export_data_to_csv

# FIT_FACTOR = 0.002593461 # NL2015
FIT_FACTOR = 0.002340651  # NL2019

def processed_curve(csv_file):
    curve = pd.read_csv(csv_file, header=None, squeeze=True)

    # Schrikkeljaar
    if curve.size == 8784: curve.drop(curve.tail(24).index, inplace=True)

    print(csv_file.stem)
    print('-   FLH: ', curve.sum() * FIT_FACTOR)

    missing = curve.isna().sum()
    if missing > 180:
        print(f"\033[93m-   Skipping: {missing} datapoints missing\033[0m")
        return np.zeros(8760)

    return normalize(curve)


def create_curve(country, year):
    # Aggregating and normailising the curve
    curves = Path(__file__).resolve().parents[2] / 'data' / country / str(year) / 'input' / 'offshore'
    nl_curve = normalize(sum((processed_curve(csv_file) for csv_file in curves.glob('*.csv'))))
    export_data_to_csv(nl_curve, 'output/solar_pv_offshore_weighted', 'nl', str(year), header=False)


if __name__ == '__main__':
    year = sys.argv[1]
    country = sys.argv[2]

    create_curve(country, year)
