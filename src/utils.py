import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta


def get_series_by_date(date):
    url = f"http://api.tvmaze.com/schedule/web?date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def get_series_for_december_2022():
    start_date = "2022-12-01"
    end_date = "2022-12-31"

    all_series = []

    current_date = start_date

    while current_date <= end_date:
        series = get_series_by_date(current_date)
        if series:
            all_series.append(series)
        current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    return all_series

def normalized_json(json_list):

    episodes_data = []
    shows_data = []

    for json_data in json_list:
        normalized_data = pd.json_normalize(json_data)

        #Extraer datos de episodios
        episodes_data.append({
            "id": normalized_data["id"].iloc[0],
            "url": normalized_data["url"].iloc[0],
            "name": normalized_data["name"].iloc[0],
            "season": normalized_data["season"].iloc[0]
        })

        # Extraer datos de programas de televisión (si están disponibles)
        shows_data.append({
            "id": normalized_data["_embedded.show.id"].iloc[0],
            "url": normalized_data["_embedded.show.url"].iloc[0],
            "type": normalized_data["_embedded.show.type"].iloc[0],
            "language": normalized_data["_embedded.show.language"].iloc[0],
            "genres": normalized_data["_embedded.show.genres"].iloc[0][0] if normalized_data["_embedded.show.genres"].iloc[0] else None,
            "status": normalized_data["_embedded.show.status"].iloc[0],
            "runtime": normalized_data["_embedded.show.runtime"].iloc[0],
            "averageRuntime": normalized_data["_embedded.show.averageRuntime"].iloc[0],
            "premiered": normalized_data["_embedded.show.premiered"].iloc[0],
            "ended": normalized_data["_embedded.show.ended"].iloc[0],
        })

    episodes_df = pd.DataFrame(episodes_data)
    shows_df = pd.DataFrame(shows_data)

    episodes_df.to_csv('../data/episodes.csv',index = False)
    shows_df.to_csv('../data/shows.csv', index=False)