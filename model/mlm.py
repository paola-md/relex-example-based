import torch

from transformers import (AutoTokenizer,
                          AutoModelForMaskedLM,
                          DataCollatorForLanguageModeling,
                          default_data_collator,
                          TrainingArguments,
                          Trainer,
                          set_seed,
                          )
import torch
import collections
import numpy as np
import json
from sklearn.model_selection import train_test_split
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import pandas as pd

# Look for gpu to use. Will use `cpu` by default if no gpu found.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SEED = 123
DATA_DIR = './data/'

# Set seed for reproducibility,
set_seed(SEED)



def finetune(X, y, model_name, EPOCHS = 2,FIELD = 'is', RESULTS_DIR = './results/',
             SAVE_MODEL = False, model_checkpoint = "distilbert-base-uncased"):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.10, random_state=42)

    print(len(X_train), "Train size")

    # Format data
    my_dataset = DatasetDict(
        {'train': Dataset.from_dict({'label': y_train, 'text': X_train}),
         'test': Dataset.from_dict({'label': y_test, 'text': X_test})
         }
    )

    ## ============== Main ==============
    tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

    MODEL_NAME = "distilroberta-base"
    model = AutoModelForMaskedLM.from_pretrained(MODEL_NAME ,
                                                vocab_size=tokenizer.vocab_size,
                                                ignore_mismatched_sizes=True)


    #model = AutoModelForMaskedLM.from_pretrained(model_checkpoint)
    #tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    ## ============== Functions ==============
    def tokenize_function(examples):
        result = tokenizer(examples["text"])
        if tokenizer.is_fast:
            result["word_ids"] = [result.word_ids(i) for i in range(len(result["input_ids"]))]
        return result

    def group_texts(examples, chunk_size=128):
        # Concatenate all texts
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        # Compute length of concatenated texts
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        # We drop the last chunk if it's smaller than chunk_size
        total_length = (total_length // chunk_size) * chunk_size
        # Split by chunks of max_len
        result = {
            k: [t[i: i + chunk_size] for i in range(0, total_length, chunk_size)]
            for k, t in concatenated_examples.items()
        }
        # Create a new labels column
        result["labels"] = result["input_ids"].copy()
        return result

    def whole_word_masking_data_collator(features, wwm_probability=0.2):
        for feature in features:
            word_ids = feature.pop("word_ids")

            # Create a map between words and corresponding token indices
            mapping = collections.defaultdict(list)
            current_word_index = -1
            current_word = None
            for idx, word_id in enumerate(word_ids):
                if word_id is not None:
                    if word_id != current_word:
                        current_word = word_id
                        current_word_index += 1
                    mapping[current_word_index].append(idx)

            # Randomly mask words
            mask = np.random.binomial(1, wwm_probability, (len(mapping),))
            input_ids = feature["input_ids"]
            labels = feature["labels"]
            new_labels = [-100] * len(labels)
            for word_id in np.where(mask)[0]:
                word_id = word_id.item()
                for idx in mapping[word_id]:
                    new_labels[idx] = labels[idx]
                    input_ids[idx] = tokenizer.mask_token_id

        return default_data_collator(features)

    def save_metadata(hist):
        with open(f"{RESULTS_DIR}dump_{FIELD}_{EPOCHS}.json", 'w') as f:
            json.dump(hist, f)

        val_loss = []
        train_loss = []
        for i in range(EPOCHS):
            elem_info = hist[(i * 2)]
            elem_loss = hist[(i * 2) + 1]

            train_loss.append(elem_info.get('loss'))
            val_loss.append(elem_loss.get('eval_loss'))

        df = pd.DataFrame({'epoch': list(range(EPOCHS)), 'train_loss': train_loss, 'val_loss': val_loss})
        df.to_csv(f"{RESULTS_DIR}{FIELD}_{EPOCHS}.csv")


    # Use batched=True to activate fast multithreading!
    tokenized_datasets = my_dataset.map(
        tokenize_function, batched=True, remove_columns=["text", "label"]
    )

    lm_datasets = tokenized_datasets.map(group_texts, batched=True)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

    ## Training
    batch_size = 64
    logging_steps = len(lm_datasets["train"]) // batch_size
    model_name = model_checkpoint.split("/")[-1]

    base = model_checkpoint.split('-')[0]
    training_args = TrainingArguments(
        output_dir=f"anonymized/mlm_{model_name}",
        overwrite_output_dir=True,
        evaluation_strategy="epoch",
        save_total_limit=1,
        logging_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        num_train_epochs= EPOCHS,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        push_to_hub=SAVE_MODEL,
        push_to_hub_token = 'anonymized',
        fp16=True,
        logging_steps=logging_steps,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_datasets["train"],
        eval_dataset=lm_datasets["test"],
        data_collator=data_collator
    )

    trainer.train()

    hist = trainer.state.log_history
    save_metadata(hist)

    if SAVE_MODEL:
      trainer.push_to_hub()


def run_mlm(model_name):
    df = pd.read_csv('{}/raw_example.csv'.format(DATA_DIR))
    X = df[['text']]
    y = df[['evaluation']]

    finetune(X, y,
    model_name = model_name,
    EPOCHS = 2,FIELD = 'text', RESULTS_DIR = './results/',
    SAVE_MODEL = True,
    model_checkpoint = "distilroberta-base")