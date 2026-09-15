import re
import pandas as pd
import numpy as np
from ..globals import df

rules = df[~df['first'].isna()]

def get_user_rules_index(mask, recipe):
    important_rules = np.unique(mask)

    df_rules = rules[rules['#'].isin(list(important_rules))]

    start_list = []
    end_list = []
    color_list = []
    class_list = []

    for i, row in df_rules.iterrows():
        error = row['error']
        if type(error) == str:
            query = error
        else:
            query = row['first']
        aux = re.search(query, recipe)
        if aux:
            start_list.append(aux.start())
            end_list.append(aux.end())
            class_list.append(row['#'])
            color_list.append(row['color'])


    df_show = pd.DataFrame({'start': start_list, 'end':end_list,
                            'class': class_list, 'color': color_list})

    df_show = df_show.drop_duplicates(['end']).drop_duplicates(['start']).sort_values('start')
    df_show['previous_end'] =   df_show['end'].shift(fill_value=0)
    df_show = df_show[df_show['start']>=df_show['previous_end']]
    return df_show


def format_user_recipe(df_show, recipe):
    recipe_list = []

    if len(df_show)>0:

        end = 0
        for i, row in df_show.iterrows():
            start = row['start']
            if start>end:
                previous = {"sentence": recipe[end:start],
                    "class" : -1, "color": 0}

                recipe_list.append(previous)

            end = row['end']
            current = {"sentence": recipe[start:end],
                 "class" : int(row['class']), "color": int(row['color'])}
            recipe_list.append(current)


        last = {"sentence": recipe[end:],
         "class" : -1, "color": 0}
        recipe_list.append(last)
    else:
        previous = {"sentence": recipe,
        "class" : -1, "color": 0}

        recipe_list.append(previous)

    return recipe_list


def format_show_recipe(mask, recipe):
    recipe = recipe.replace('\n', ' \n ')
    df_show = get_user_rules_index(mask, recipe)
    recipe_list = format_user_recipe(df_show, recipe)
    return recipe_list