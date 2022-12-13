from .completeness import get_bool_options
from .similarity import get_similar_options, filter_out_seen 
#from .nlp import get_models_options
from .rules import get_user_bool
from .postgres_utils import save_metadata
from .globals import NUMBER_OF_RULES

import numpy as np
import pandas as pd


def create_mask(bool_user, example_bool):
    # Return what to show
    missing =  np.where(bool_user==0) #missing or na
    found = np.where(example_bool==2)
    show_bool = np.intersect1d(missing, found)
    print(show_bool, missing, found)
    mask = np.full(NUMBER_OF_RULES, fill_value=-1)
    mask[show_bool] = show_bool
    return mask, show_bool

def choose_recipe(recipe, user, study=False):
    # 1) Choose options with rules
    bool_user, bool_str = get_user_bool(recipe) 
    print(f"user bool is {bool_str}")

    df_bool = get_bool_options(recipe, bool_user) 
    print("{} bool options".format(len(df_bool)))

    if study:
        # 2) Choose options with model
        df_model = pd.DataFrame() #get_models_options(recipe)
        print("{} model options".format(len(df_model)))
        #print("{}".format(list(df_model['title'])))
        #print(df_model.columns)

        # 3) Filter out recipes seen
        # We first filter out the recipes that the user has already seen
        df_bool = filter_out_seen(df_bool, user)
        
        # 4) Return intersection of both (chosen by the rules and by the model)
        recipes_bool = list(df_bool['recipe_id'].values)
        recipes_model = list(df_model['recipe_id'].values)
        recipes_both = list(set(recipes_bool).intersection(set(recipes_model)))
        print(f"{len(recipes_both)} recipes in commom")
        
        if len(recipes_both)>0:
            df_both = df_model[df_model['recipe_id'].isin(recipes_both)]
        else:
            # There are no common recipes between both 
            df_both = df_bool
    else:
        df_both = df_bool


    # 5) Return most simlar recipe
    df_example = get_similar_options(recipe, df_both, search =1)
    print("Recipe chosen: {}".format(df_example['title']))
    
    # 6) Create mask of rules to show
    example_bool = df_example['bool']
    print(f"example bool is {example_bool}")    
    example_bool = np.array(list(example_bool), dtype=int)

    mask, show_bool = create_mask(bool_user, example_bool)

    # 7) Finally we update the table
    metadata = {'user_id': user, 
    'recipe_id': df_example['recipe_id'],
    'user_bool': str(bool_str),
    'user_recipe': recipe,
    'show_mask': str(show_bool)
    }

    print(metadata.values())
    save_metadata(metadata, 'backend.recipes_seen')

    return df_example, list(mask)

