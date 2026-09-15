
import re
from nltk.corpus import stopwords
from rank_bm25 import BM25Okapi
from .postgres_utils import get_select


def filter_out_seen(df_model, user):
    # We first filter out the recipes that the user has already seen
    df_sim = df_model

    query = f"""
    select recipe_id
    from backend.recipes_seen
    where user_id = '{user}'
    """
    print(query)
    res = get_select(query)

    if len(res) > 0:
        options = list(df_model['recipe_id'])
        seen_activities = list(res['recipe_id'])
        unseen =  list(set(options) - set(seen_activities))
        print(f"{len(options)} recipes to show, {len(unseen)} have not been seen")
        if len(unseen) < len(options):
            df_sim = df_model[df_model['recipe_id'].isin(unseen)]
            if len(df_sim)==0:
                # user has seen them all
                df_sim = df_model

    return df_sim

def get_similar_options(recipe, df_sim, search=1):


    num_words = 60
    fields_clean =   df_sim['bm25']
    tokenized_corpus = (fields_clean).tolist()
    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query =  clean_bm25(re.sub('[^a-zA-Z ]+', '', recipe.lower()).split()[:num_words])

    # find closest elements
    docs = bm25.get_top_n(tokenized_query, df_sim['recipe_id'].tolist(), n=search)

    # top n (unseen)
    df_sim = df_sim[df_sim['recipe_id'].isin(docs)]
    df_sim = df_sim.iloc[0]

    return df_sim



def clean_bm25(element):
    stop = set(stopwords.words('english'))
    # remove irrelevant common words. word count.
    stop = stop.union({'cup', 'lb', 'lbs','cups',
                       'ounces', 'ounce', 'inch',
                      'teaspoon', 'teaspoons',
                      'tablespoon', 'tablespoons',
                        'into', 'on', 'or', 'for', 'of',
                         'with', 'in',
                        'to', 'a', 'the', 'and'
                      '0', '1', '2', '3', '4', '5', '6', '7', '8',
                      '1/2', '1/3', '2/3', '1/4', '2/4', '3/4',
                       '1/5', '2/5', '3/5', '4/5'})
    tokens_without_sw = [word for word in element if word not in stop]
    return tokens_without_sw

