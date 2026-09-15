import itertools
import numpy as np
from .postgres_utils import get_select
from .globals import NUMBER_OF_RULES


def get_search_bool(bool_user, index_zero, tolerance=0):

    regex_list = ""

    if tolerance>0:
        for subset in itertools.combinations(index_zero, tolerance):

            b = bool_user.copy()
            for i in subset:
                b[i] = 3
            new_str = (np.array2string(b,
                separator='',
                max_line_width=100)
            .replace('.', '')
            .replace('[', '')
            .replace(']', '')
            .replace('2', 'a')
            .replace('0', '[2]')
            .replace('1', '[0|1|2]')
            .replace('3', '[0|1|2]')
            .replace('a', '[0|1|2]')
            )
            regex_list = regex_list + '|' + new_str
        regex_list = regex_list[1:]
    else: # look for the perfect one
        regex_list = (np.array2string(bool_user,
        separator='',
        max_line_width=100)
        .replace('.', '')
        .replace('[', '')
        .replace(']', '')
        .replace('2', 'a')
        .replace('0', '[2]')
        .replace('1', '[0|1|2]')
        .replace('a', '[0|1|2]')
        )


    return  regex_list



def get_bool_options(recipe, bool_user):
    tolerance=0
    index_zero = np.where(bool_user==0)[0]
    search_bool = get_search_bool(bool_user,  index_zero, tolerance)

    print(f"searching for recipes with the following string {search_bool}")
    query = f"""
    select * from backend.recipes
    where bool ~ '{search_bool}';
    """
    df = get_select(query) #options
    print(len(df), "perfect options")


    while(len(df)==0) & (tolerance <2):

        tolerance += 1
        print(tolerance)
        search_bool = get_search_bool(bool_user,  index_zero, tolerance)

        query = f"""
        select * from backend.recipes
        where bool ~* '{search_bool}';
        """
        df = get_select(query)

    if tolerance>=2:
        search_bool = "[2]"*3 + "[0|1|2]"*(NUMBER_OF_RULES-6) + "[2]"*3

        query = f"""
        select * from backend.recipes
        where bool ~* '{search_bool}';
        """
        df = get_select(query)



    return df






