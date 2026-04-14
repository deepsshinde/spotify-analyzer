from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class DBLoader:
    def __init__(self):
        db_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(db_string)
    
    def load_data(self, df, table_name):
        """Load dataframe to PostgreSQL"""
        df.to_sql(table_name, self.engine, if_exists='append', index=False)
        print(f"Loaded {len(df)} rows to {table_name}")

# Usage
if __name__ == "__main__":
    loader = DBLoader()
    df = pd.read_csv('data/raw_listening_history.csv')
    loader.load_data(df, 'raw_listening_history')