import pandas as pd
import sqlite3


def create_db_from_csv_with_pandas(csv_file, db_name, table_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Database created.")


