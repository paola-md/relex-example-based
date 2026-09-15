from .utils import check_regex_rules, create_list_rules
import ast
from ..globals import df





def format_ingredients(ingredients, mask):
    ingredients_recipe = []
    ingredients_list = ast.literal_eval(ingredients)
    ids_ingredients = [0,1]

    df_ingredients = df[(df['component']=='ingredients') & (~df['first'].isna()) & (df['#'].isin(mask))]
    ingredients_rules_list = create_list_rules(df_ingredients)

    current = {"sentence": "\n Ingredients:",
               "class": int(mask[0]), "color": 1}
    ingredients_recipe.append(current)

    for ingredient in ingredients_list:

        current = {"sentence": "\n - ",
                    "class": int(mask[1]),"color": 1}
        ingredients_recipe.append(current)

        new_id, new_ingredient = check_regex_rules(ingredient, ingredients_rules_list)

        ingredients_recipe = ingredients_recipe + new_ingredient
        ids_ingredients = ids_ingredients + new_id

    current = {"sentence": "\n \n",
               "class": -1, "color": 1}
    ingredients_recipe.append(current)
    return ids_ingredients, ingredients_recipe


def format_steps(steps,  mask):
    steps_recipe = []
    ids_steps = [2]
    steps_list = ast.literal_eval(steps)

    df_steps = df[(df['component']=='steps') & (~df['first'].isna()) & (df['#'].isin(mask))]
    steps_rules_list = create_list_rules(df_steps)


    current = {"sentence": "\n \n \n \n Steps: \n",
               "class": int(mask[0]), "color": 1}
    steps_recipe.append(current)

    i = 1
    for step in steps_list:

        current = {"sentence": f" \n {i}. ",
                    "class": int(mask[2]), "color": 1}
        steps_recipe.append(current)

        new_id, new_step = check_regex_rules(step, steps_rules_list)

        steps_recipe = steps_recipe + new_step
        ids_steps = ids_steps + new_id

        i+=1
    return ids_steps, steps_recipe

