import pandas as pd
NUMBER_OF_RULES = 45
DIR_RULES = ''

# For notebook
DIR_RULES = '/../app/backend'

# For analysis
DIR_RULES = '/../../app/backend'

df = pd.read_csv(f".{DIR_RULES}/recipe/data/example-rules.csv")