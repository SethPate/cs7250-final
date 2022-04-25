"""
Transformer models subclassed from PyTorch.

Respect to https://pytorch.org/tutorials/beginner/transformer_tutorial.html.
"""

import torch.nn as nn
from typing import Tuple

class BinaryTransformer(nn.Module):
    def __init__(self, model_size: int, num_heads: int, hidden_size: int, num_layers: int, dropout: float=0.5):
        super().__init__()
        self.model_size = model_size
        self.positional = PositionalEncoder(model_size, dropout)
        transformer_layers = nn.TransformerEncoderLayer(model_size, num_heads, hidden_size, dropout)
        self.transformer = nn.TransformerEncoder(transformer_layers, num_layers)
        self.decoder = nn.Linear(model_size, 1) # binary probability output

    def forward(self, x: Tensor) -> Tensor:
        """
        Return a single logit.
        Note that we are not using a mask here to hide any input
        to the transformer. That would be important for a language
        modeling task, but we are doing a binary classifier.
        """
        x_encoded = self.encoder(x)
        x_sqrt = x.encoded * math.sqrt(self.model_size)
        x_pos = self.positional(x_sqrt)
        y = self.transformer(x_pos)
        y_dec = self.decoder(y)

        return y_dec

def generate_square_subsequent_mask(sz: int) -> Tensor:
    """Generates an upper-triangular matrix of -inf, with zeros on diag."""
    return torch.triu(torch.ones(sz, sz) * float('-inf'), diagonal=1)

class PositionalEncoder(nn.Module):
    """Add sin and cos information to represent position in the sequence."""
    def __init__(self, model_size: int, dropout: float=0.5, max_len: int=1000):
        super().__init__(self, dropout)
        self.dropout = nn.Dropout(p=dropout)
        position = torch.arange(max_len).unsqueeze(1)
        modifier = torch.exp(torch.arange(0,model_size,2)) * (-math.log(10000) / model_size)
        encodings = torch.zeros(max_len, 1, model_size)
        encodings[:,0,0::2] = torch.sin(position * modifier)
        encodings[:,0,1::2] = torch.cos(position * modifier)
        self.register_buffer('encodings',encodings)
        """
        Saving to register buffer means torch will not track them as parameters.
        """
        
    def forward(self, x: Tensor) -> Tensor:
        x_pos = x + self.encodings[:x.size(0)]
        x_drop = self.dropout(x_pos)
