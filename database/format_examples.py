import sys
import pandas as pd
sys.path.append('../')
from backend.recipe.rules import get_bool
from backend.recipe.similarity import prepare_bm25


df = pd.read_csv('./../model/data/raw_examples.csv')


df['bool'] = df['text'].apply(lambda x: get_bool(x))
df['bm_25'] = df['text'].apply(lambda x: prepare_bm25(x))


df.to_csv('./data/examples.tsv', sep='\t')