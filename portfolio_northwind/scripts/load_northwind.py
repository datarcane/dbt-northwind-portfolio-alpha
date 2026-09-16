import duckdb
from pathlib import Path

# Déclarations des chemins (dossier actuel et dossier racine)
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

# Initialisation de la connexion
con = duckdb.connect(str(ROOT_DIR / "northwind.duckdb"))
con.execute('INSTALL httpfs;')
con.execute('LOAD httpfs;')

base_url = 'https://raw.githubusercontent.com/neo4j-contrib/northwind-neo4j/refs/heads/master/data'

# Sélection des tables
tables = ['categories', 'customers', 'employee-territories', 'employees', 'order-details', 'orders', 'products', 'regions', 'shippers', 'suppliers', 'territories']

# Boucle de chargement des tables
for table in tables:
    table_name = table.replace('-', '_')
    df = con.execute(f'''
        create or replace table raw_{table_name} as
        select * from read_csv('{base_url}/{table}.csv', header=True)
''')
    print(f'La table {table_name} a bien été chargée')

con.close()