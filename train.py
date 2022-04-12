"""
- Reads the config file for your specifications.
- Creates a Coach object, responsible for training and evaluation.
- Attempts to load a model and resume training.
- Otherwise, creates a models/{modelname} subfolder.
- Loads data.
- Trains and evaluates on a set cycle.
- Saves results to the models/{modelname} subfolder. 

Attributions:
Uses code from https://pytorch.org/tutorials/beginner/transformer_tutorial.html.
"""

import csv
import yaml
import os
import tqdm
import transformer as tf
import torch
from torch.utils.data import DataLoader
from torchtext.datasets import IMDB
from torchtext.datasets import WikiText2
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator


device = "cuda" if torch.cuda.is_available() else "cpu"

def get_data(batch_size:int) -> (DataLoader, DataLoader):
    """Just IMDB so far."""
    train_iter = IMDB(split="train") # [(label, line),...]
    tokenizer = get_tokenizer('basic_english')
    #print('train_iter, test_, tokenizer')
    #breakpoint()
    train_text = [x[1] for x in train_iter]

    vocab = build_vocab_from_iterator(map(tokenizer, train_text), specials=['<unk>'])
    vocab.set_default_index(vocab['<unk>'])
    #print('vocab')
    #breakpoint()

    text_pipeline = lambda x: vocab(tokenizer(x))
    label_pipeline = lambda x: int(x) - 1

    def collate(batch):
        """DataLoader uses this to prep data."""
        label_list, text_list, offsets = [], [], [0]
        for (_label, _text) in batch:
             label_list.append(label_pipeline(_label))
             processed_text = torch.tensor(text_pipeline(_text), dtype=torch.int64)
             text_list.append(processed_text)
             offsets.append(processed_text.size(0))
        label_list = torch.tensor(label_list, dtype=torch.int64)
        offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
        text_list = torch.cat(text_list)
        return label_list.to(device), text_list.to(device), offsets.to(device)


    # train_iter was "consumed" by the process of building the vocab,
    # so we have to create it again
    train_iter, test_iter = IMDB()
    train = DataLoader(train_iter, batch_size=8, collate_fn=collate)
    test = DataLoader(test_iter, batch_size=8, collate_fn=collate)

    return train, test

def get_model(config):
    vocab_size = config["vocab_size"]
    model_size = config["model_size"]
    num_heads = config["num_heads"]
    hidden_size = config["hidden_size"]
    num_layers = config["num_layers"]
    dropout = config["dropout"]

    model = tf.BinaryTransformer(
        vocab_size, model_size, num_heads, 
        hidden_size, num_layers, dropout
    )
    save_model_params(model.named_parameters())
    breakpoint()

    return model

def save_model_params(params):
    """Save in csv format."""
    parsed_params = [] # {'name','values'}
    for name, param in params:
        if param.requires_grad:
            parsed = {'name':name,'values':param.tolist()}
            parsed_params.append(parsed)
    field_names = ['name','values']
    with open('init_params.csv','w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for p in parsed_params:
            writer.writerow(p)
    return

def model_exists(model_dir_path: os.PathLike, model_path: os.PathLike) -> bool:
    """Returns true if there is a folder with a saved model file,
        false otherwise.
    """
    if os.path.isdir(model_dir_path):
        if os.path.exists(model_path):
            return True
    else:
        return False

def init_model_folder(model_dir_path: os.PathLike) -> None:
    """Creates a folder to store the saved model and results file."""
    try:
        os.mkdir(model_dir_path)
    except Exception as e:
        print(f"Failed to make {model_dir_path} with {e}")

    return

def init_results(model_dir_path: os.PathLike) -> None:
    """Creates a results.yaml file storing metrics."""
    
    metrics = ["train-accuracy", "loss",
                "test-accuracy",
                "samples-trained"]
    results = {m: [] for m in metrics}
    results_path = os.path.join(model_dir_path,"results.yaml")
    save_results(results, results_path)

    return

def train_loop(config: dict, model: tf.BinaryTransformer,
                train: DataLoader, test: DataLoader,
                model_dir_path: os.PathLike) -> None:
    """
    * trains the model
    * evaluates
    * tracks results
    * saves the model
    * returns updated results
    """
    # initialize loss function and optimizer
    lr = config['lr']
    weightdecay = config['weightdecay']
    lossfn = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(),
                    lr = lr, weight_decay = weightdecay)

    epochs = config['epochs'] # how many times to go thru dataset
    for i in tqdm(range(epochs)):
        loss = 0
        accuracy = []
        samples = results['samples-trained']

        for j, batch in enumerate(train):
            batch.to(device)
            target, x = batch
            y = model(x)

            batch_loss = lossfn(y, target)
            loss += batch_loss

            batch_acc = torch.eq(y.round(), target)
            batch_acc = batch_acc.mean()
            accuracy.append(batch_acc)

            samples += len(batch)
        
        # optimize the model
        optimizer.zero_grad()
        loss.backward()
        optimizer.step() 
    
        # update and save results
        accuracy = torch.mean(accuracy)
        results['samples-trained'].append(samples)
        results['train-accuracy'].append(accuracy)
        results['loss'].append(loss.item())

        # export results, save model
        print("*** saving results file.")
        save_results(results, model_dir_path)
        print("*** done saving results file.\n")
        print("*** saving model.")
        save_model(model, model_path)
        print("*** done saving model.\n")

    return

def save_model(model: torch.nn.Module, path: os.PathLike) -> None:
    try:
        torch.save(model.state_dict(), path)
    except Exception as e:
        print(f"Failed to save model to {path} with {e}")

    return

def load_results(path: os.PathLike) -> dict:
    try:
        results = yaml.unsafe_load(path)
    except Exception as e:
        print(f"Failed to load results from {path} with {e}")
        results = None

    return results


def save_results(results: dict, path: os.PathLike) -> None:
    try:
        with open(path,'r') as f:
            yaml.dump(results, f)
    except Exception as e:
        print(f"Failed to save new results to {results_path} with {e}")

    return

def main():
    # load config for preferences
    print("*** Opening config file.")
    with open("config.yaml") as f:
        config = yaml.unsafe_load(f)
        print("*** Loaded config file.")
        print(config, "\n")

    # grab the dataset
    print("*** Loading dataset.")
    batch_size = config['batch_size']
    #train, test = get_data(batch_size)
    print("*** Done loading dataset.\n")

    # create model
    print("*** Initializing model.")
    model = get_model(config)
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
    train_loop(config, model, results, train, test, model_dir_path)
    print("*** done with training loop.\n")

    return


if __name__ == "__main__":
    main()
