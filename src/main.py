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

    else:
        print("No se pudo obtener la información de la API.")
