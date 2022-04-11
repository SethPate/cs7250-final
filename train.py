"""
- Reads the config file for your specifications.
- Creates a Coach object, responsible for training and evaluation.
- Attempts to load a model and resume training.
- Otherwise, creates a models/{modelname} subfolder.
- Loads data.
- Trains and evaluates on a set cycle.
- Saves results to the models/{modelname} subfolder. 
"""

import yaml
import os
from torchtext.datasets import IMDB
from torch.utils.data import DataLoader

import transformer as tf


def get_data():
    """Just IMDB so far."""
    train_iter = IMDB(split="train")
    test_iter = IMDB(split="test")  # [(label, line),...]

    def collate():
        """DataLoader uses this to prep data."""
        raise NotImplementedError

    train = DataLoader(train_iter, batch_size=8, shuffle=True, collate_fn=collate)
    test = DataLoader(test_iter, batch_size=8, shuffle=True, collate_fn=collate)

    return train_iter, test_iter


def get_model(config):
    model_size = config["model_size"]
    num_heads = config["num_heads"]
    hidden_size = config["hidden_size"]
    num_layers = config["num_layers"]
    dropout = config["dropout"]

    model = tf.BinaryTransformer(
        model_size, num_heads, hidden_size, num_layers, dropout
    )

    return model

def model_exists(model_dir_path: os.Path, model_path: os.Path) -> bool:
    """Returns true if there is a folder with a saved model file,
        false otherwise.
    """
    if os.path.isdir(model_dir_path):
        if os.path.exists(model_path):
            return True
    else:
        return False

def init_model_folder(model_dir_path: os.Path) -> None:
    """Creates a folder to store the saved model and results file."""
    try:
        os.mkdir(model_dir_path)
    except e as Exception:
        print(f"Failed to make {model_dir_path} with {e}")

    return

def init_results(model_dir_path: os.Path) -> None:
    """Creates a results.yaml file storing metrics."""
    
    metrics = ["train-accuracy", "train-loss",
                "test-accuracy", "test-loss"]
    results = {m: [] for m in metrics}
    results_path = os.path.join(model_dir_path,"results.yaml")
    save_results(results, results_path)

    return

def train_loop(config: dict, model: tf.BinaryTransformer) -> dict:
    raise NotImplementedError


def load_results(path: os.Path) -> dict:
    try:
        results = yaml.unsafe_load(path)
    except e as Exception:
        print(f"Failed to load results from {path} with {e}")
        results = None

    return results


def save_results(results: dict, path: os.Path) -> None:
    try:
        yaml.dump(results, path)
    except e as Exception:
        print(f"Failed to save new results to {results_path} with {e}")

    return

def main():
    # load config for preferences
    print("*** Opening config file.")
    with open("config.yaml") as f:
        config = yaml.unsafe_load(f)
        print("*** Loaded config file.")
        print(config + "\n")

    # grab the dataset
    print("*** Loading dataset.")
    train, test = get_data()
    print("*** Done loading dataset.\n")

    # create model
    print("*** Initializing model.")
    model = get_model()
    print("*** Done initializing model.\n")

    # path to saved model
    model_dir_path = os.path.join("saved_models", config["save_as"])
    model_path = os.path.join(model_dir_path, config["save_as"] + ".model")

    if not model_exists(model_dir_path, model_path):
        print(f"*** {model_dir_path} not found, creating new.\n")
        # init results folder if necessary
        init_model_folder(model_dir_path)
    else:
        # load state dict if present
        print(f"*** Loading model state dict from {model_dir_path}.")
        model.load_state_dict(model_path)
        print("*** Done loading model state dict.\n")

    # get existing results
    print("*** Loading results.")
    results = load_results(model_dir_path)
    print("*** done loading results.\n")

    # train and evaluate according to config
    print("*** Starting train loop.")
    results = train_loop(config, model, results)
    print("*** done with traing loop.\n")

    # export results and save model
    print("*** saving results file.")
    save_results(results, model_dir_path)
    print("*** done saving results file.\n")

    return


if __name__ == "__main__":
    main()
