import duckdb
import pandas as pd
from pathlib import Path

# Déclarations des chemins (dossier actuel et dossier racine)
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_Q_DIR = ROOT_DIR / "data_quality"

# Objectif : identifier les tables mal chargées (1 seule colonne = ERREUR)
def conflit_nb_colonnes():
    # Etablissement de la connexion
    con = duckdb.connect(str(ROOT_DIR / "northwind.duckdb"))

    # Création de la liste des tables à contrôler
    a_verifier = []

    tables = [t[0] for t in con.execute('SHOW TABLES').fetchall()]
    print(tables)
    for table in tables:
        result = con.execute(f"SELECT count(1) FROM duckdb_columns() WHERE table_name = '{table}';").fetchone()[0]
        if result <= 1:
            a_verifier.append({"table" : table, "nb_colonnes" : result, "statut": ""})

    df = pd.DataFrame(a_verifier)
    df.to_csv(DATA_Q_DIR / "tables_a_verifier.csv", index=False, sep=";", encoding="utf-8-sig")

    print(f"{len(a_verifier)} tables sont à contrôler - fichier de contrôle créé à l'emplacement {DATA_Q_DIR}")

    con.close()

conflit_nb_colonnes()