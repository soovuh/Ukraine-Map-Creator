import pandas as pd


def get_data_from_excel(file, label_name, lat_name, lon_name, unique_labels):
    data = pd.read_excel(file)
    result = []
    unique_labels_list = []

    for index, row in data.iterrows():
        label = row[label_name]
        coords = (row[lat_name], row[lon_name])
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
