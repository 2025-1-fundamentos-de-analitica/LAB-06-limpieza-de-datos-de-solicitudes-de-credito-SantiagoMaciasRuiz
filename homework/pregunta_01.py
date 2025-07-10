"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os
import pandas as pd


def clean_text(column):
    return column.str.lower().str.replace("-", " ").str.replace("_", " ").str.strip()


def dates(date_series):
    dates = pd.to_datetime(date_series, dayfirst=True, errors="coerce")
    dates = dates.fillna(
        pd.to_datetime(date_series, format="%Y/%m/%d", errors="coerce")
    )
    return dates


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    input_path = "files/input/solicitudes_de_credito.csv"
    output_path = "files/output/solicitudes_de_credito.csv"

    df = pd.read_csv(input_path, sep=";", index_col=0)

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    df["sexo"] = df["sexo"].str.lower()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()
    df["barrio"] = df["barrio"].str.lower().str.replace("_", " ").str.replace("-", " ")
    columns = [
        "idea_negocio",
        "línea_credito",
    ]
    for column in columns:
        df[column] = clean_text(df[column])

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.strip()
        .str.replace("$", "")
        .str.replace(",", "")
        .str.replace(".00", "")
        .astype(int)
    )
    df["fecha_de_beneficio"] = dates(df["fecha_de_beneficio"])

    df.drop_duplicates(inplace=True)

    if os.path.exists(output_path):
        os.remove(output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=";")

    print(df["sexo"].value_counts())
    print(df["barrio"].value_counts())


pregunta_01()
