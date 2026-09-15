"""
Useful functions for postgres database
"""
import psycopg2
#import psycopg2.extras
import pandas as pd
import numpy
from datetime import datetime

from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)


user = "postgres"
password = "1570"
port = 5432
database_name = "relex"
hostname = "localhost"
DATABASE_URL = f"postgres://{user}:{password}@{hostname}:{port}/{database_name}"

# For heroku
#DATABASE_URL = os.environ['HEROKU_POSTGRESQL_TEAL_URL']

def get_connection():
    """ create new engine
    Returns:
        connection: engine
    """
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as error:
        print("Error while creating connection", error)


def get_select(query):
    """ Obtiene dataframe de resultado de un select
    Returns:
        df: dataframe con resultado del select
    """
    try:
        connection = get_connection()
        df = pd.read_sql_query(query,con=connection)
        connection.close()
        return df
    except Exception as error:
        print("Error while fetching data from PostgreSQL", error)


def execute_query(query):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Exception as error:
        print("Error while fetching data from PostgreSQL", error)


def insert_df(df, table_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        num_cols = len(df.columns)
        query = """insert into {table_name}
        values (%s {new_cols}) """.format(table_name = table_name,
                                         new_cols = ', %s'*(num_cols -1) )

        for i in range(len(df)):
            values = tuple(df.iloc[i].values)
            cursor.execute(query, values)

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)

def insert_query(query, record_to_insert):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, record_to_insert)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)


def save_metadata(metadata, table_name):
    timestamp = datetime.now()
    values = (timestamp,) + tuple(metadata.values())

    num_cols = len(values)
    query = """insert into {table_name}
    values (%s {new_cols}) """.format(table_name = table_name,
                                     new_cols = ', %s'*(num_cols -1) )
    insert_query(query, values)




