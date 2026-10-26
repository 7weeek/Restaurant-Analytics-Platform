import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file.")

# Use psycopg 3 with SQLAlchemy.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_row_count():
    with engine.connect() as connection:
        return connection.execute(
            text("SELECT COUNT(*) FROM public.restaurant_analytics")
        ).scalar_one()


def get_existing_order_ids(order_ids):
    existing = set()

    with engine.connect() as connection:
        for start in range(0, len(order_ids), 500):
            batch = list(dict.fromkeys(order_ids[start:start + 500]))

            result = connection.execute(
                text("""
                    SELECT order_id
                    FROM public.restaurant_analytics
                    WHERE order_id = ANY(:ids)
                """),
                {"ids": batch}
            )

            existing.update(result.scalars().all())

    return existing


def upload_rows(df):
    if df.empty:
        return 0

    df.to_sql(
        name="restaurant_analytics",
        schema="public",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=250,
        method="multi"
    )

    return len(df)