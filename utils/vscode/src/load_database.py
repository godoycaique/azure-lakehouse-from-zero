import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHM_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)


def normalize_columns(df):
    df.columns = (
        df.columns.str.normalize('NFKD')
        .str.replace(' ', "_", regex=True)
        .str.replace('-', "_", regex=True)
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8')
        .str.lower()
        .str.strip()
    )
    return df

def load_csv_database():
    file_path = 'data/sales_supermarket.csv'
    df = pd.read_csv(file_path, sep=',', quotechar='"')
    df = df.dropna(subset=['Order ID']).drop(columns=['Row ID'])
    df = normalize_columns(df)
    return df

def get_tables(df, schema):
    customers_df = df[['customer_id', 'customer_name', 'segment', 'country', 'state', 'postal_code', 'region']].drop_duplicates().reset_index(drop=True)
    customers_df.to_sql('dim_customers', engine, if_exists='replace', index=True, schema=schema)
    print(f' > Tabela dim_customer carregada com {customers_df.count()} linhas')

    products_df = df[['product_id', 'product_name', 'category', 'sub_category']].drop_duplicates().reset_index(drop=True)
    products_df.to_sql('dim_products', engine, if_exists='replace', index=True, schema=schema)
    print(f' > Tabela dim_products carregada com {products_df.count()} linhas')

    sales_df = df[['order_id', 'order_date', 'ship_date', 'ship_mode', 'customer_id', 'product_id', 'sales']].drop_duplicates().reset_index(drop=True)
    sales_df.to_sql('fact_sales', engine, if_exists='replace', index=True, schema=schema)
    print(f' > Tabela fact_sales carregada com {sales_df.count()} linhas')

    return True

if __name__ == "__main__":
    df = load_csv_database()
    get_tables(df, schema='public')