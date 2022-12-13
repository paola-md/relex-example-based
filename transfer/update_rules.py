import pandas as pd
sys.path.append('../')
from backend.recipe.globals import df

colors_dict = {1: {'noti': 'is-warning', 'color_text': "hsl(48, 100%, 57%)" , 'darktext': "#947600" },
    3:  {'noti': 'is-link', 'color_text':'hsl(217, 51%, 73%)' , 'darktext': '#2160c4'},  
    2: {'noti': 'is-success', 'color_text':'hsl(141, 71%, 68%)' , 'darktext': '#257942'},  
    4: {'noti': 'is-primary', 'color_text':'hsl(171, 80%, 61%)' , 'darktext': '#00947e'}
    }
    
def create_html_rules(df):
    complete_txt = ""
    headings_flag = 1
    
    labels_dict = {1 : 'Tips on Structure',
                   2 : 'Tips on the Specificity of Ingredients',
                   3 : 'Tips on the Specificity of Steps',
                   4 : 'Tips for Clarity of Steps'}
    
    
    for index, row in df.iterrows():
        rule_num = int(row['#'])
        txt = row['text'].rstrip()
        color = row['color']
        exp = row['explaination']
        
        title_exp = ""
        
        if pd.isna(exp)==False:
            title_exp = f'title= "{exp}" '
        
        colortext = colors_dict[color]['noti']
        
        if headings_flag  == color:
            next_txt = f"""
            <span class="hint-{color}" id="hint-{color}"  style="display: none;">{labels_dict[color]}</span>
            """
            complete_txt = complete_txt + next_txt
            headings_flag +=1

        next_txt = f"""
        <div class="notification {colortext} is-light" id="noti-{rule_num}" {title_exp} style="display: none;" onmouseenter="onHoverSentenceClass({rule_num})" onmouseleave="onOutHoverSentenceClass({rule_num})"> 
             {txt} 
             <button class="delete" id="butt-{rule_num}"> </button>
        </div> 
        """
        complete_txt = complete_txt + next_txt
    return complete_txt

print(create_html_rules(df))

