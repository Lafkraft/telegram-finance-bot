import os
from typing import Dict, List, Tuple

import sqlite3

def insert(table: str, column_values: Dict):
    cursor = get_cursor()
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    cursor.connection.commit()
    cursor.connection.close()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    cursor = get_cursor()
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    cursor.connection.close()
    return result


def delete(table: str, row_id: int) -> None:
    cursor = get_cursor()
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    cursor.connection.commit()
    cursor.connection.close()

def get_cursor():
    conn = sqlite3.connect(os.path.join("db", "finance.db"))
    return conn.cursor()


def _init_db():
    """Инициализирует БД"""
    cursor = get_cursor()
    with open("createdb.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.executescript(sql)
    cursor.connection.commit()
    cursor.connection.close()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor = get_cursor()
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    cursor.connection.close()
    if table_exists:
        return
    _init_db()

check_db_exists()
