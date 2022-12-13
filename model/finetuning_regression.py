from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
import os
import torch
import json


from transformers import AutoTokenizer, \
                          AutoModelForSequenceClassification, \
                          TrainingArguments, \
                          Trainer, \
                          EarlyStoppingCallback, \
                          IntervalStrategy

from datasets.dataset_dict import DatasetDict
from datasets import Dataset, load_metric
from sklearn.metrics import mean_squared_error, mean_absolute_error


# MODEL_NAME = "./pretrain_bert" #"dbmdz/bert-base-italian-xxl-cased"
DATA_DIR = './data/'
MODEL_DIR = './models/'
RESULTS_DIR = './results/'

FIELD = 'text'
EPOCHS = 20
SEED = 123
SAVE_MODEL = True


def seed_everything(seed=123):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

seed_everything(seed=123)



def create_dataset(df):
    """
    TODOs:
    - Save datasets
    - Try with single user dataset
    Args:
        df:
        recipes:
        field:
    Returns:

    """

    y = df['evaluation']
    X = df['text']

    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.1, random_state=SEED)
    X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.1, random_state=SEED)

    dataset = DatasetDict(
      {'train': Dataset.from_dict({'label': y_train,
                                    'text': X_train}),
      'val': Dataset.from_dict({'label': y_val,
                                    'text': X_val}),
      'test': Dataset.from_dict({'label': y_test,
                                    'text': X_test})
      })   

    return dataset


                             
def tokenize_dataset(dataset):                              
    TOKENIZER = "distilroberta-base" 
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER) 

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding="max_length",  truncation=True)
        
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    return tokenized_datasets


def compute_metrics(eval_pred):
    metric1 = load_metric("mse")
    metric2 = load_metric("mae")
    
    logits, labels = eval_pred
    predictions =logits
    mse = metric1.compute(predictions=predictions, references=labels)["mse"]
    mae = metric2.compute(predictions=predictions, references=labels)["mae"]
    rmse = mean_squared_error(labels, predictions, squared=False)

    return {"rmse": rmse, "mse": mse, "mae": mae}