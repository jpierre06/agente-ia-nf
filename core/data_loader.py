from core.csv import get_csv_content
import pandas as pd

def load_dataframes(zip_path: str, files: list[str]) -> dict[str, pd.DataFrame] | str:
    dataframes = {}
    for filename in files:
        df = get_csv_content(zip_path, filename)
        if isinstance(df, str):  # Erro retornado como string
            return f"Erro ao carregar '{filename}': {df}"
        dataframes[filename] = df
    return dataframes
