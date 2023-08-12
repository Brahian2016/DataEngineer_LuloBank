import requests
import pandas
import numpy
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
            all_series.extend(series)
        current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    return all_series