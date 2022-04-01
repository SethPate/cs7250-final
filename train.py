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
from torchtext.datasets import IMDB
from torch.utils.data import DataLoader

import transformer as tf

def get_data():
    """Just IMDB so far."""
    train_iter = IMDB(split='train')
    test_iter = IMDB(split='test') # [(label, line),...]

    def collate():
        """DataLoader uses this to prep data."""
        raise NotImplementedError

    train = DataLoader(train_iter, batch_size=8, shuffle=True, collate_fn=collate)
    test = DataLoader(test_iter, batch_size=8, shuffle=True, collate_fn=collate)

    return train_iter, test_iter

def get_model(config):
    model_size = config['model_size']
    num_heads = config['num_heads']
    hidden_size = config['hidden_size']
    num_layers = config['num_layers']
    dropout = config['dropout']

    model = tf.BinaryTransformer(model_size, num_heads, hidden_size, num_layers, dropout)

    return model

def main():
    # load config for preferences
    with open('config.yaml') as f:
        config = yaml.unsafe_load(f)

    # grab the dataset
    train, test = get_data()
    
    # create model
    model = get_model()

    # init results folder if necessary
    # load state dict if present

    # train and evaluate according to config
    
    # export results and save model


if __name__ == "__main__":
    main()
