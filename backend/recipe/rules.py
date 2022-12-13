import re 
import numpy as np
import pandas as pd
import string
from .format_recipes.utils import create_list_rules
from .globals import NUMBER_OF_RULES, DIR_RULES, df



def rule_two_matches(txt, if_first, look_second, exception, offset = 30):
    res = 1 # does not apply 
    x = re.search(if_first, txt, re.IGNORECASE)
    if x:
        lower_bound = (x.start() - offset)
        if lower_bound < 0:
            lower_bound =0

        substr = txt[lower_bound:(x.end() + offset)]
        x = re.search(look_second, substr, re.IGNORECASE)
        if x:
            res = 2 
        else:
            res = 0 # not found
            if ((exception != 'nan') & (type(exception)!=float)):
                x = re.search(exception, substr, re.IGNORECASE)
                if x: # Rule does not apply
                    res = 1
      
    return res


def rule_one_match(txt, query, notap = 1):
    res = notap # does not apply 
    x = re.search(query, txt, re.IGNORECASE)
    if x:
        res = 2
    return res

def rule_error(txt, query):
    res = 1 # does not apply 
    x = re.search(query, txt, re.IGNORECASE)
    if x:
        res = 0
    return res


def ingredients_steps(txt):
    res = 0 # does not apply 
    query = "ingredient?"
    x = re.search(query, txt[:50], re.IGNORECASE)

    if x:
        query = "step?|method?|directions|instructions|steps"
        x = re.search(query, txt, re.IGNORECASE)
        if x:
            res = 2 #recipe succeeds 
        else:
            res = 0 #recipe fails 
    return str(res)    
    

def new_lines(txt):
    res = 0
    res_search = re.findall('\n',txt)
    if res_search:
        words = len(list(filter(None, txt.replace('\n', ' ').split(' '))))
        lines = len(res_search)
        words_per_line = words/lines

        if words_per_line< 10:
            res = 2

    return str(res)

    
def is_ennumerated(txt):
    """
    Is ennumerated if there are at least 3 numbered steps
    """
    res = 0
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    txt = txt.lower().replace('step', '').replace('steps', '').replace('number', '')
    text_lines = txt.splitlines()
    first_character = [x.strip()[0] for x in text_lines if len(x.strip())>0] 
    if set(['1','2','3', '4']) <= set(first_character):
        res = 2
    return res



def get_user_bool(txt):
    bool_user = np.ones(NUMBER_OF_RULES)

    bool_user[0] = ingredients_steps(txt)
    bool_user[1] = new_lines(txt[:150])
    bool_user[2] = is_ennumerated(txt)

    for num in range(3, NUMBER_OF_RULES):
        rule = df.iloc[num]
        first_rule = rule['first']
        second_rule = rule['second']
        exception = rule['exception']
        missing = rule['missing']
        error = rule['error']

        if type(error) == str:
            res = rule_error(txt, error)
        elif ((second_rule == 'nan') | (type(second_rule)==float)):
            res = rule_one_match(txt, first_rule, notap = missing)
        else:
            res = rule_two_matches(txt, first_rule, second_rule, exception)
        
        bool_user[num] = res
    
    bool_str = (np.array2string(bool_user, 
                separator='',
                max_line_width=100)
            .replace('.', '')
            .replace('[', '')
            .replace(']', '')
           )
        
    return bool_user, bool_str

def get_bool(txt):
    bool_user, bool_str = get_user_bool(txt)
    return bool_str
