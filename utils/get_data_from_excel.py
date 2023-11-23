import pandas as pd
import numpy as np


def get_data_from_excel(file, label_name, lat_name, lon_name, unique_labels):
    data = pd.read_excel(file)
    result = []
    unique_labels_list = []

    for index, row in data.iterrows():
        label = row[label_name]
        try:
            coords = (float(row[lat_name]), float(row[lon_name]))
        except Exception as e:
            print(f'Error: {e}')
            continue
        if label == np.nan or np.nan in coords:
            continue
        if unique_labels:
            if label in unique_labels_list:
                continue
            else:
                unique_labels_list.append(label)
        result.append(
            {
                "label": label,
                "coords": coords,
            }
        )
    return result


def get_headers_from_excel(file):
    df = pd.read_excel(file)
    headers = df.columns.tolist()
    return headers
