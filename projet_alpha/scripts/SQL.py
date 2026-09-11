import duckdb
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

con = duckdb.connect(str(ROOT_DIR / "northwind.duckdb"))

df = con.execute('''

Select *
from raw_regions
limit 10

''').df()

print(df)

con.close()