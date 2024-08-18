from __future__ import annotations

import atexit
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

load_dotenv()
db_name = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
fallback_db_name = os.getenv("SQLITE_PATH")
assert db_name, "Database name must be provided"
postgres_db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
sqlite_db_url = f"sqlite:///{fallback_db_name}"


def create_postgres_db():
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Attempt to create the new database
        try:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"Database '{db_name}' created successfully")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{db_name}' already exists")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_engine_fallback():
    try:
        create_postgres_db()
        engine = create_engine(postgres_db_url)
        print("SQLAlchemy engine for PostgreSQL created successfully")
    except Exception as e:
        print(f"An error occurred with PostgreSQL: {e}")
        engine = create_engine(sqlite_db_url)
        print("SQLAlchemy engine for SQLite created successfully")
    return engine


engine = create_engine_fallback()

Base.metadata.create_all(engine)

maker = sessionmaker(bind=engine)
session = maker()


@atexit.register
def exit():
    session.close()
