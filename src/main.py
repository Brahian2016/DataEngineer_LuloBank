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

        # Llamar a la función para realizar las operaciones de agregación
        aggregation_results = aggregate_operations(episodes_df, shows_df)

        # Mostrar los resultados
        print("a. Runtime promedio:", aggregation_results['average_runtime'])
        print("b. Conteo de shows de TV por género:")
        genre_counts = aggregation_results['genre_counts']
        for index, row in genre_counts.iterrows():
            print(row['Genero'], "|", row['cantidad'])
        print("c. Listar los dominios del sitio oficial de los shows:")
        for domain in aggregation_results['unique_domains']:
            print(domain)


    else:
        print("No se pudo obtener la información de la API.")
