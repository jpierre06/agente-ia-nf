import pandas as pd
from pathlib import Path
#import core.zip_processor as zp
import unicodedata
import re
import io

HEADS_DIR = Path("./data/csv/heads")
ITEMS_DIR = Path("./data/csv/items")

def get_info_df(df: pd.DataFrame) -> str:
    """Retorna informações básicas do DataFrame."""
    buffer = io.StringIO()
    df.info(buf=buffer)

    info_str = buffer.getvalue()

    # Quebrar por linhas
    lines_str = info_str.split('\n')

    # Extrair as linhas das colunas (começam geralmente na 5ª linha até a penúltima)
    lines_columns = lines_str[5:-3]  # pode variar dependendo do pandas

    # Parse manual das colunas
    data_info = []
    for lines in lines_columns:
        line_parts = lines.strip().split()
        if len(line_parts) >= 3:
            nome_coluna = line_parts[1]
            n_nao_nulos = line_parts[2]
            tipo_dado = line_parts[-1]
            data_info.append({
                'coluna': nome_coluna,
                'não_nulos': n_nao_nulos,
                'tipo': tipo_dado
            })

    # Criar DataFrame dicionário de dados
    return pd.DataFrame(data_info)

def normalize_column_name(columns_name):
    normalize_column = []
    for cn in columns_name:
        # Remove acentos, converte texto para minúscula e retirar espaços em branco no inicio e fim do texto
        cn = unicodedata.normalize("NFKD", cn).encode("ASCII", "ignore").decode().lower().strip()
        # Substitui todos os não-alfanuméricos por '_'
        cn = re.sub(r'\W+', '_', cn)
        # Reduz múltiplos '_' para um só
        cn = re.sub(r'_+', '_', cn)
        # Remove '_' do início/fim
        cn = cn.strip('_')
        normalize_column.append(cn)
    return normalize_column

def _read_all_csv_from_dir(directory: Path) -> pd.DataFrame | str:
    """Lê e concatena todos os arquivos CSV de um diretório."""
    all_dfs = []
    for csv_file in directory.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            df.columns = normalize_column_name(df.columns)
            df["__FONTE_ARQUIVO__"] = csv_file.name  # opcional: rastreabilidade
            all_dfs.append(df)
        except Exception as e:
            return f"Erro ao ler '{csv_file.name}': {str(e)}"
    
    if not all_dfs:
        return f"Nenhum arquivo CSV encontrado no diretório {directory}"
    
    return pd.concat(all_dfs, ignore_index=True)

def load_dataframes_from_folders() -> dict[str, pd.DataFrame] | str:
    """Carrega todos os CSVs de ./data/csv/heads e ./data/csv/items."""
    heads_df = _read_all_csv_from_dir(HEADS_DIR)
    if isinstance(heads_df, str):
        return heads_df  # erro

    items_df = _read_all_csv_from_dir(ITEMS_DIR)
    if isinstance(items_df, str):
        return items_df  # erro

    return {
        "heads": heads_df,
        "items": items_df
    }

