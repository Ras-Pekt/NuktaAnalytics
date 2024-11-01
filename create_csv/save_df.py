#!/usr/bin/python3
import pandas as pd
from sqlalchemy import create_engine, text


def to_csv(df, filename):
    # Save to CSV file
    df.to_csv(filename, index=False)


def to_sql(df, engine):
    # Convert timestamp column to datetime (optional, but recommended)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Step 1: Create a SQLAlchemy engine for your database
    # Example: SQLite (for testing), but you can replace this with your database connection string
    # For MySQL: 'mysql+pymysql://username:password@localhost/db_name'
    # For PostgreSQL: 'postgresql://username:password@localhost/db_name'
    engine = create_engine(
        "sqlite:///games.db"
    )  # This creates a SQLite database called games.db

    # Step 2: Use pandas to create the table and insert the data
    # The `if_exists='replace'` will drop the table if it exists and create a new one
    df.to_sql("games", con=engine, if_exists="replace", index=False)

    with engine.connect() as connection:
        query = text("SELECT * FROM games")
        result = connection.execute(query)
        for row in result:
            print(row)
