from regression_main import train_model
from mlm import run_mlm
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='model name', type=str)

    args = parser.parse_args()
    model_name = args.name

    run_mlm(model_name)
    train_model(model_name)

