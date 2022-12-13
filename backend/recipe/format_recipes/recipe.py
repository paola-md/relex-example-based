
from .ingredients import format_ingredients, format_steps
from .utils import get_bool
import numpy as np
from ..globals import NUMBER_OF_RULES

def format_title(title):
    title_recipe = []
    current = {"sentence": f"Title: {title} \n \n", 
               "class": -1, "color":0}
    title_recipe.append(current) 
    return title_recipe


def get_format_recipe(title, ingredients, steps, mask = list(range(NUMBER_OF_RULES))):
    title_recipe = format_title(title)
    ids_ingredients, ingredients_recipe = format_ingredients(ingredients, mask)
    ids_steps, steps_recipe = format_steps(steps, mask)
    
    bool_recipe = get_bool(ids_ingredients, ids_steps)

    final_text = title_recipe + ingredients_recipe + steps_recipe
    return bool_recipe, final_text
    