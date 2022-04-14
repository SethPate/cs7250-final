import numpy as np


# softmax function that is applied on a specific axis
def softmax(x, axis=None):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x)
    logits = e_x / e_x.sum(axis=axis, keepdims=True)
    return logits