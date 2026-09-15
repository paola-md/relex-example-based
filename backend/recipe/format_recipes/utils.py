import re
import numpy as np
from ..globals import NUMBER_OF_RULES

def create_list_rules(df):
    rules_list = []

    for index, row in df.iterrows():
        new_rule = [row['#'], str(row['first']), str(row['second']), row['color']]
        # class, first, second, color
        rules_list.append(new_rule)

    return rules_list


def regex_two(txt, first, second, class_match, color_match):
    new_list = []
    x = re.search(first, txt, re.IGNORECASE)
    if x:
        start1 = x.start()
        end1 = x.end()
        x = re.search(second, txt, re.IGNORECASE)
        if x:
            start2 = x.start()
            end2 = x.end()
            print(f"rules: {class_match}. text: {txt}.  first: {first}.  second: {second}. ")

            #flip end and start if they are flipped
            start = np.min([start1, end1, start2, end2])
            end = np.max([start1, end1, start2, end2])

            if start > 0:
                current = {"sentence": txt[:start],
                "class" : -1, "color": 0}
                new_list.append(current)

            current = {"sentence": txt[start:end],
                       "class" : class_match, "color": color_match}
            new_list.append(current)

            if end < len(txt):
                current = {"sentence": txt[end:],
                "class" : -1, "color": 0}
                new_list.append(current)

    return new_list


def regex_one(txt, first, class_match, color_match):
    new_list = []
    x = re.search(first, txt, re.IGNORECASE)
    if x:
        start = x.start()
        end = x.end()


        if start > 0:
            current = {"sentence": txt[:start],
            "class" : -1, "color": 0}
            new_list.append(current)

        current = {"sentence": txt[start:end],
                    "class" : class_match,
                    "color": color_match}
        new_list.append(current)

        if end < len(txt):
            current = {"sentence": txt[end:],
            "class" : -1, "color": 0}
            new_list.append(current)

    return new_list

def get_bool(ids_ingredients, ids_steps):
    max_rules = NUMBER_OF_RULES
    rules = np.unique(ids_ingredients+ ids_steps)
    print("rules", rules)
    bool_recipe = np.ones(max_rules)
    bool_recipe[rules] = 2
    bool_str = (np.array2string(bool_recipe,
                    separator='',
                    max_line_width=100)
                .replace('.', '')
                .replace('[', '')
                .replace(']', '')
               )

    return bool_str

def check_regex_rules(txt, rules_list):
    id_rule = []
    rule_list = []
    for rule in rules_list:
        if rule[2] =='nan':
               # class, first, second, color
            rule_list = regex_one(txt, rule[1], rule[0],rule[3])
        else:
            rule_list = regex_two(txt, rule[1], rule[2], rule[0], rule[3])
        if len(rule_list) > 0:
            # Found a match
            id_rule.append(rule[0])
            break

    if len(rule_list) ==0:
        # No match
        current = {"sentence": txt,
        "class" : -1, "color": 0}
        rule_list = [current]

    return id_rule, rule_list
