sys.path.append('../')
from backend.recipe.globals import df

colors_dict = {1: {'noti': 'is-warning', 'color_text': "hsl(48, 100%, 57%)" , 'darktext': "#947600" },
    3:  {'noti': 'is-link', 'color_text':'hsl(217, 51%, 73%)' , 'darktext': '#2160c4'},
    2: {'noti': 'is-success', 'color_text':'hsl(141, 71%, 68%)' , 'darktext': '#257942'},
    4: {'noti': 'is-primary', 'color_text':'hsl(171, 80%, 61%)' , 'darktext': '#00947e'}
    }

def generate_css(df):
    complete_txt = ""

    for index, row in df.iterrows():
        rule_num = int(row['#'])
        txt = row['text']
        color = row['color']

        colortext = colors_dict[color]['color_text']
        darktext = colors_dict[color]['darktext']


        next_txt = f"""
        .sentence-class-{rule_num} {{
            border-bottom: 0.15em solid {colortext};
            transition: all 0.25s;
        }}

        .sentence-class-background-{rule_num} {{
            background-color: {colortext};
        }}

        #noti-{rule_num} {{
            border: 2px solid transparent;
            transition: all 0.25s;
        }}
        """
        complete_txt = complete_txt + next_txt

    for i in colors_dict.keys():
        next_txt = f"""
        .hint-{i} {{
        background-color: {colors_dict[i]['color_text']};
        padding: 10px;
        padding-left: 26px;
        padding-right: 26px;
        display: inline-block;
        font-weight: bold;
        margin-bottom: 10px;
        margin-top: 10px;
        display: none; 
        }}
        """
        complete_txt = complete_txt + next_txt

    return complete_txt


css = generate_css(df)
print(css)