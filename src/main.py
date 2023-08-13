from utils import *

if __name__ == "__main__":
    series_december_2022 = get_series_for_december_2022()
    if series_december_2022:
        save_to_json(series_december_2022, "../json/series_december_2022.json")
        episodes_df, shows_df = normalized_json(series_december_2022)
        print("Datos almacenados exitosamente en series_december_2022.json")

        # Limpiar data
        clean_data(episodes_df, shows_df)
        episodes_df, shows_df = clean_data(episodes_df, shows_df)

        episodes_df.to_csv('../data/episodes_clean.csv', index=False)
        shows_df.to_csv('../data/shows_clean.csv', index=False)

        # Guardar en parquet
        save_dataframes_to_parquet(episodes_df, shows_df)

        # Llamar a la función para leer Parquet y almacenar en la base de datos
        read_parquet_and_store_in_database()

        # Hacer una consulta a la db
        #query_database('shows')

    else:
        print("No se pudo obtener la información de la API.")
