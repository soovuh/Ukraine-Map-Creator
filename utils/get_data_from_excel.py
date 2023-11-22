import pandas as pd


def get_data_from_excel(file, label_name, lat_name, lon_name):
    result = []
    data = pd.read_excel(file)
    for index, row in data.iterrows():
        label = row[label_name]
        coords = (row[lat_name], row[lon_name])

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
