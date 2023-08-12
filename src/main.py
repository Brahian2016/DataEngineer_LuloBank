from utils import *

if __name__ == "__main__":
    series_december_2022 = get_series_for_december_2022()
    if series_december_2022:
        save_to_json(series_december_2022, "../json/series_december_2022.json")
        print("Datos almacenados exitosamente en series_december_2022.json")
    else:
        print("No se pudo obtener la información de la API.")