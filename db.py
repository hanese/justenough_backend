import psycopg2
import os


# connects with the database, straight forward
def connect():
    conn = psycopg2.connect(host="localhost",
                            database="justenough",
                            user="postgres",
                            password=os.getenv("pgpwd"))
    return conn


# performs an insert statement into postgres
def insert_query(table: str, columns: list, values: list) -> int:
    columns_sql = ", ".join(columns)
    values_sql = [f"'{val}'" if val else 'NULL' for val in values]
    values_sql = ", ".join(values_sql)
    sql = f"INSERT INTO {table}({columns_sql}) VALUES({values_sql});"
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql)
    except psycopg2.DatabaseError as err:
        return int(err.pgcode)
    return 0


# function to pass a string to perform any sql string
def arbitrary_query(sql: str) -> int:
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql)
    except psycopg2.Error as err:
        return int(err.pgcode)
    return 0


# performs a select statement
def select_query(sql: str, params: tuple) -> int or list[dict[str, any]]:
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql, params)
            res = cur.fetchall()
            return res
    except psycopg2.Error as err:
        return int(err.pgcode)


# performs a delete statement
def delete_query(table: str, condition: str) -> any:
    sql = f"DELETE FROM {table} WHERE {condition};"
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql)
            a = cur.rowcount
    except psycopg2.DatabaseError as err:
        return int(err.pgcode)
    return 0


# performs an update statement
def update_query(table: str, column: str, condition: str, updated_value: str) -> any:
    sql = f"UPDATE {table} SET {column} = '{updated_value}' WHERE {condition};"
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql)
    except psycopg2.DatabaseError as err:
        return int(err.pgcode)
    return 0


# perform a select query, the result is mapped
def mapped_select_query(table: str, columns: list[str], condition: str) -> int or list:
    columns_str = ", ".join(columns)
    sql = f"SELECT {columns_str} FROM {table} WHERE {condition};"

    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            res_mapped = [{f"{col}": f"{val}" for col, val in zip(columns, vals)} for vals in res]
            return res_mapped
    except psycopg2.Error as err:
        return int(err.pgcode)


# performs an insert statement where no columns must be defined
def insert_query_no_columns(table: str, values: list) -> int:

    prepared_list = []
    for attribute in values:
        if type(attribute) is str:
            attribute = attribute.replace("\r\n", "").replace("\n", "").replace("'", "''")
        prepared_list.append(attribute)

    values_sql = [f"'{val}'" if val else 'NULL' for val in prepared_list]
    values_sql = ", ".join(values_sql)
    sql = f"INSERT INTO {table} VALUES ({values_sql});"
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql)
    except psycopg2.DatabaseError as err:
        return int(err.pgcode)
    return 0
