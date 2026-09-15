import torch
from transformers import set_seed
import pandas as pd
import random
import argparse

from mlm import finetune



# Set seed for reproducibility,
SEED = 123
random.seed(SEED)
set_seed(SEED)
results_dir = './results'
data_dir = './data'
models_dir = './models'

# Look for gpu to use. Will use `cpu` by default if no gpu found.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)




if __name__ == '__main__':
    # 'tis', 'ts', 'clean_steps', 'is'
    #python src/train_main.py -l "is" -m 1 -f 0.0005 -e 1 -s 10
    #python src/mlm_main.py -l "is" -e 1 -s 1 -h 0 -m distilbert-base-uncased
    # python src/mlm_main.py -l "is" -e 1 -s 1 -h 0 -m distilbert-base-uncased
    # python src/mlm_main.py -l "Is" -e 1 -s 1 -h 0 -m distilroberta-base


    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='delimited list input', type=str)
    parser.add_argument('-e', '--epochs', type=int)
    parser.add_argument('-s', '--sample', type=int)
    parser.add_argument('-u', '--save', type=int)
    parser.add_argument('-m', '--model', help='delimited list input', type=str)

    args = parser.parse_args()
    fields  = [str(item) for item in args.list.split(',')]

    EPOCHS = args.epochs #4
    SAMPLE = args.sample # 0 off, 1 only first 20
    SAVE = args.save
    MODELS = [str(item) for item in args.model.split(',')]

    if SAVE==1:
        SAVE=True
    else:
        SAVE=False

    print(f"Fields: {fields}.  Epochs: {EPOCHS}. Sample: {SAMPLE}. Save: {SAVE}. Models: {MODELS}")

    df = pd.read_csv('{}/recipes_roberta.csv.gz'.format(data_dir))

    if SAMPLE:
        df = df.sample(n=100)

    for model in MODELS:
        for field in fields:
            print(field, model)
            X = df[field]
            y = df.index
            finetune(X, y, EPOCHS= EPOCHS, FIELD=field, RESULTS_DIR='./results/', SAVE_MODEL=SAVE,
                     model_checkpoint = model)
