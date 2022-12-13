


from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Union
from fastapi.middleware.cors import CORSMiddleware
from .postgres_utils import get_select,save_metadata
from .login import *
from random import randrange
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
import numpy as np
import time
from .example_recipe import choose_recipe 
from .format_recipes.recipe import get_format_recipe
from .format_recipes.user import format_show_recipe
from .globals import NUMBER_OF_RULES


# Place here the code the should be loaded only once
class Source(BaseModel):
    recipe: str = ""
    user: str = ""

class Answer(BaseModel):
    example_recipe: List[dict] = []
    user_recipe: List[dict] = []



class UserEvent(BaseModel):
    user: str = ""
    event: str = ""
    details: dict = {}

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

@app.get("/")
def wake_up():
    thankyou=1
    return thankyou



@app.post("/example/")
def complete(source: Source):

    try :
        print(source.recipe)
        df_example, mask = choose_recipe(source.recipe, source.user)

    except:
        query = """
        select * from backend.recipes
        where random() < 0.01
        limit 1;
        """
        df_example = get_select(query)
        df_example = df_example.iloc[0]
        mask = list(range(NUMBER_OF_RULES))
        print("Error in pipeline, returning random recipe.")

    bool_example, example = get_format_recipe(df_example['title'],
                                    df_example['ingredients'], 
                                    df_example['steps'], mask)

    print('MASK', mask)

    user_recipe = format_show_recipe(mask, source.recipe) 
    answer = Answer(user_recipe = user_recipe, 
                    example_recipe = example)
    return answer


@app.post("/example3/")
def complete_3(source: Source):


    query = f"""
    with chosen_recipes as (select * from backend.recipes
    limit 5)
    
    select *
    from chosen_recipes
    order by random()
    limit 1;
    """
    df_example = get_select(query)
    df_example = df_example.iloc[0]
    mask = [-1]*NUMBER_OF_RULES 
    print("Returning random recipe.")

    bool_example, example = get_format_recipe(df_example['title'],
                                    df_example['ingredients'], 
                                    df_example['steps'], mask)

    print('bool_example', bool_example)

    answer = Answer(example_recipe = example)
    return answer


@app.post("/test/")
def complete_test(source: Source):


    query = f"""
    with chosen_recipes as (select * from backend.recipes
    limit 5)
    
    select *
    from chosen_recipes
    order by random()
    limit 1;
    """
    df_example = get_select(query)
    df_example = df_example.iloc[0]
    mask =list(range(NUMBER_OF_RULES )) #show everything
    print("Returning selected recipe.")

    _, example = get_format_recipe(df_example['title'],
                                    df_example['ingredients'], 
                                    df_example['steps'], mask)

    print(example)

    user_recipe = format_show_recipe(mask, source.recipe) 
    print(user_recipe)

    answer = Answer(user_recipe = user_recipe, 
                    example_recipe = example)
    return answer


@app.post("/trace/")
def trace(event: UserEvent):
    print(event.user)
    print(event.event)
    metadata = {'user': event.user,
    'event': event.event, 
    'details': json.dumps(event.details)}

    print("saving metadata: ", metadata)

    save_metadata(metadata, "backend.users_events")

    return metadata




@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    keyapps = {"knife": "1", #cut 1
    "cup": "2", #measure 2
    "microwave": "3", #heat 3
    "salt": "4", #season 4
    "bread": "5", #eat 5,
    "boil": "1", # 6
     "test": "1", #cut 1
    "ilovewriting": "1"} #cut 1}

    key = form_data.password

    if not key in keyapps.keys():
        raise HTTPException(status_code=400, detail="Incorrect username or key")
    
    else:
        group = keyapps[key]

    return {"access_token": form_data.username, "token_type": group}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

