import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
import sqlite3


from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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

        # Extraer datos de episodios
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

    episodes_df.to_csv('../data/episodes.csv', index=False)
    shows_df.to_csv('../data/shows.csv', index=False)

    episodes_profiling = profiling(episodes_df)
    shows_profiling = profiling(shows_df)

    episodes_profiling.to_csv('../profiling/episodes_profiling.csv', index=False)
    shows_profiling.to_csv('../profiling/shows_profiling.csv', index=False)

    generate_pdf_report(episodes_profiling, '../profiling/episodes_profiling.pdf')
    generate_pdf_report(shows_profiling, '../profiling/shows_profiling.pdf')

    return(episodes_df,shows_df)


def generate_pdf_report(df, filename):
    doc = SimpleDocTemplate(filename, pagesize=landscape(letter))

    # Convert DataFrame to list of lists
    data = [df.columns.tolist()] + df.values.tolist()

    # Create table with data
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Build document and save to file
    doc.build([table])

def profiling(df):
    profiling = {
        'column_name': [],
        'data_type': [],
        'unique_values': [],
        'missing_values': [],
        'mean': [],
        'min': [],
        'max': [],
    }

    for column in df.columns:
        profiling['column_name'].append(column)
        profiling['data_type'].append(df[column].dtype)
        profiling['unique_values'].append(df[column].nunique())
        profiling['missing_values'].append(df[column].isnull().sum())

        if pd.api.types.is_numeric_dtype(df[column]):
            profiling['mean'].append(df[column].mean())
            profiling['min'].append(df[column].min())
            profiling['max'].append(df[column].max())
        else:
            profiling['mean'].append(None)
            profiling['min'].append(None)
            profiling['max'].append(None)

    profiling_df = pd.DataFrame(profiling)
    return profiling_df



def clean_data(episodes_df, shows_df):
    # Tratar valores faltantes en 'averageRuntime'
    average_runtime_mean = shows_df['averageRuntime'].mean()
    shows_df['averageRuntime'].fillna(average_runtime_mean, inplace=True)

    # Eliminar filas duplicadas
    episodes_df.drop_duplicates(inplace=True)

    return episodes_df, shows_df


def save_dataframes_to_parquet(episodes_df, shows_df):
    # Almacenar los DataFrames en archivos Parquet con compresión Snappy
    episodes_table = pa.Table.from_pandas(episodes_df)
    pq.write_table(episodes_table, '../data/episodes.parquet', compression='snappy')

    shows_table = pa.Table.from_pandas(shows_df)
    pq.write_table(shows_table, '../data/shows.parquet', compression='snappy')


def create_database_schema(connection):
    cursor = connection.cursor()

    # Crear la tabla 'episodes'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY,
            url TEXT,
            name TEXT,
            season INTEGER
        )
    ''')

    # Crear la tabla 'shows'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY,
            url TEXT,
            type TEXT,
            language TEXT,
            genres TEXT,
            status TEXT,
            runtime INTEGER,
            averageRuntime INTEGER,
            premiered TEXT,
            ended TEXT
        )
    ''')

    connection.commit()

# Conectar a la base de datos
conn = sqlite3.connect('tv_series.db')
create_database_schema(conn)

def read_parquet_and_store_in_database():
    episodes_table = pq.read_table('../data/episodes.parquet')
    episodes_df = episodes_table.to_pandas()

    shows_table = pq.read_table('../data/shows.parquet')
    shows_df = shows_table.to_pandas()

    # Conectar a la base de datos
    conn = sqlite3.connect('../db/tv_series.db')

    # Almacenar datos en la tabla 'episodes'
    episodes_df.to_sql('episodes', conn, if_exists='replace', index=False)

    # Almacenar datos en la tabla 'shows'
    shows_df.to_sql('shows', conn, if_exists='replace', index=False)

    conn.close()

def query_database(table_name):
    # Conectarse a la base de datos
    db_name = '../db/tv_series.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Ejecutar una consulta
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Imprimir los resultados
    for row in rows:
        print(row)

    # Cerrar la conexión
    conn.close()


