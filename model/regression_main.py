import pandas as pd
import numpy as np
import json

from transformers import AutoTokenizer, \
                          AutoModelForSequenceClassification, \
                          TrainingArguments, \
                          Trainer, \
                          EarlyStoppingCallback

from sklearn.metrics import mean_squared_error, mean_absolute_error

from finetuning_regression import *

DATA_DIR = "./data/"
RESULTS_DIR = './results/'
FIELD = 'Is'
EPOCHS = 10
SEED = 123
SAVE_MODEL = True



def train_model(model_name):

    df = pd.read_csv(f"{DATA_DIR}raw_examples.csv")

    ## ==== DATA PROCESSING ====
    # 1. Create dataset
    dataset = create_dataset(df)

    # 2. Tokenize dataset
    tokenized_datasets = tokenize_dataset(dataset)

    # 3. Shuffle datasets
    small_train_dataset = tokenized_datasets["train"].shuffle(seed=SEED)
    small_val_dataset = tokenized_datasets["val"].shuffle(seed=SEED)
    small_test_dataset = tokenized_datasets["test"].shuffle(seed=SEED)


    ## ==== TRAINING ====
    # 4. Load model
    TOKENIZER =  "distilroberta-base"
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)

    # 4.1 Parameters
    learning_rate = 2e-05
    weight_decay = 0.02
    batch_size = 256

    MODEL_NAME = f"anonymized/mlm_{model_name}"
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME ,
                                                            vocab_size=tokenizer.vocab_size,
                                                            ignore_mismatched_sizes=True,
                                                            num_labels=1,
                                                            problem_type='regression')



    # 5. Training arguments
    args = TrainingArguments(
        model_name,
        do_train = True,
        do_eval = True,

        evaluation_strategy="epoch",   # "steps"
        logging_strategy="epoch",
        save_strategy = "epoch",
        eval_steps = "epoch", # Evaluation and Save happens every 50 steps
        save_total_limit = 5, # Only last 5 models are saved. Older ones are deleted.
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,

        num_train_epochs=EPOCHS,
        weight_decay=weight_decay,

        push_to_hub=SAVE_MODEL,
        push_to_hub_token = 'anonymized',

        metric_for_best_model = 'mae',
        greater_is_better=False,
        load_best_model_at_end=True)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=small_train_dataset,
        eval_dataset=small_val_dataset,
        compute_metrics=compute_metrics,
        callbacks = [EarlyStoppingCallback(early_stopping_patience=2)]
    )

    trainer.train()

    if SAVE_MODEL:
        trainer.push_to_hub()

    ## ==== EVALUATION ====
    # 6. Store results
    hist = trainer.state.log_history

    with open(f"{RESULTS_DIR}dump-{model_name}.json", 'w') as f:
        json.dump(hist, f)

    # 7. Predict on new dataset
    predictions = trainer.predict(small_test_dataset)

    with open(f"{RESULTS_DIR}predictions-{model_name}.json", 'w') as f:
        json.dump(predictions.metrics, f)

    print(predictions)

    # Baseline
    labels_test = small_test_dataset['label']
    mean_train = np.mean(small_train_dataset['label'])
    print('MEAN TRAIN', mean_train)
    mean_train_list = [mean_train]*len(labels_test)

    baselines = {'mse': mean_squared_error(mean_train_list, labels_test),
                'mae': mean_absolute_error(mean_train_list, labels_test),
                'mean': mean_train

    }
    with open(f"{RESULTS_DIR}baseline-{model_name}.json", 'w') as f:
        json.dump(baselines, f)


