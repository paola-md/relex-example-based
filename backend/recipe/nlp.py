from transformers import AutoTokenizer, \
                        AutoModelForSequenceClassification, \
                        TextClassificationPipeline
import time

from .postgres_utils import  get_select

# Load models at the start and stores them as global variables
print("Loading models")
TOKENIZER = "annonymized for submission"
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER) 
vocab = tokenizer.vocab_size
start = time.time()

MODEL_NAME = "annonymized for submission"
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME , 
                                                        vocab_size=vocab,
                                                        ignore_mismatched_sizes=True,
                                                        num_labels=1, 
                                                        problem_type='regression')
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True) 
end = time.time()
print("Loading time: {}".format(end - start))



def predict_score(recipe):
    # To prevent exceeding the maximum lenght, we take the first 500 words
    shrten_recipe = " ".join(recipe.split(" ")[:500])
    start = time.time()
    res = pipe(shrten_recipe)
    end = time.time()
    print("Prediciton time: {}".format(end - start))
    print(res)
    while type(res)==list:
        res = res[0]
    res = float(res['score'])
    print(f"Score is {res}")
    return res


def select_range(res):
    # 2) Obtain recipes from database
    one_std = 0.387

    lower_bound = res + one_std*1
    upper_bound = res + one_std*1.5
    
    query = f"""
    select * from backend.recipes
    where gauss_mean >= {lower_bound}
    and gauss_mean <= {upper_bound};
    """

    df = get_select(query)
    print(f"Found options {len(df)}")
    return df    


def get_models_options(recipe):
    # 1) Predict score for recipe
    # To prevent exceeding the maximum lenght, we take the first 500 words
    res = predict_score(recipe)

    # 2) Obtain recipes from database
    df = select_range(res)

    return df


