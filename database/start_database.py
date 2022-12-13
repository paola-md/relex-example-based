import sys
import pandas as pd
sys.path.append('../')
from backend.recipe.postgres_utils import execute_query, insert_df


def create_schema():
    # Create schema
    query = "create schema if not exists backend;"
    execute_query(query)
    print("Schema created")

def create_tables():
    # Create tables
    query = """
    drop table if exists backend.recipes;
    create table if not exists backend.recipes (
        recipe_id int,
        bm25 text[],
        gauss_mean float, 
        bool text,
        title text, 
        ingredients text,
        steps text
    );
    """ 
    execute_query(query)
    print("Recipe table created")

    query = """
    create table if not exists backend.users_events (
        event_date timestamp,
        user_id text,
        event_type text,
        details jsonb
    );
    """ 
    execute_query(query)
    print("User events table created")

    query = """
    drop table if exists backend.recipes_seen;
    create table if not exists backend.recipes_seen (
        event_date timestamp,
        user_id text,
        recipe_id int,
        user_bool text,
        user_recipe text,
        show_mask text
    );
    """ 
    execute_query(query)
    print("Recipe seen table created")


def load_recipes():
    df_save = pd.read_csv("./data/examples.tsv")
    n = 100 #chunk row size
    list_df = [df_save[i:i+n] for i in range(0,df_save.shape[0],n)]

    for i in range(len(list_df)):
        print(i)
        insert_df(list_df[i], 'backend.recipes')

    print("Examples loaded")

    query = """
    create index if not exists bool on backend.recipes(bool);
    """
    execute_query(query)

def main():
    create_schema()
    create_tables()
    load_recipes()

main()