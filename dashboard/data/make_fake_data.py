import pickle
import math
import numpy as np
from scipy.special import softmax

save_as = "fake_data.pickl"

## reviews (real from the dataset)

neg = "11 years after this film was released only 5 people have reviewed it here on IMDb. There is a reason for this utter lack of interest in Across the Moon. It is coherent, but lacks all cinematic virtue. See this film for examples of terrible production in all respects."

pos = "My yardstick for measuring a movie's watch-ability is if I get squirmy. If I start shifting positions and noticing my butt is sore, the film is too long. This movie did not even come close to being boring. Predictable in some parts sure, but never boring."

# layers from the tf we want to visualize
layers = [
    'embedding',
    'position',
    'combined',
    'query',
    'key',
    'value',
    'attention',
    'linear',
    'relu',
    'norm',
    'scaling',
    'decoder',
    ]

def make_pos_vectors(t,d):
    """Borrowed from pytorch.org"""
    position = np.expand_dims(np.arange(t),1)
    div_term = np.exp(np.arange(0, d, 2) * (-math.log(10000.0) / d))
    pe = np.zeros((t, 1, d))
    pe[:, 0, 0::2] = np.sin(position * div_term)
    pe[:, 0, 1::2] = np.cos(position * div_term)
    pe = pe.squeeze(1)
    return pe

def sample_to_layers(s):
    sample = s.split(" ")
    t = len(sample) # number of tokens
    d = 128 # model hidden dimension
    lo, hi = -3, 3

    embedding = np.random.normal(size=(t,d))
    #position = np.random.normal(size=(t,d))
    position = make_pos_vectors(t,d)
    combined = embedding + position

    query = np.random.uniform(lo,hi,size=(t,d))
    key = np.random.uniform(lo,hi,size=(t,d))
    value = np.random.uniform(lo,hi,size=(t,d))

    qk = np.matmul(query, key.transpose())
    scale_term = np.sqrt(d)
    scaled = qk / scale_term

    attention = softmax(scaled, axis=1)
    attn_value = np.matmul(attention, value)

    # throw the data off gaussian to make norm effect clear
    w_linear = np.random.uniform(lo-1,hi+1,size=(t,d))
    linear = attn_value * w_linear
    relu = linear.copy()
    relu[relu < 0] = 0.
    norm = relu - relu.mean(axis=0)
    norm /= norm.std(axis=0)

    decoder = np.random.normal(size=(1,1))
    final = 1 / (1 + np.exp(-1 * decoder))

    l = {
        'sample' : sample, # list of words
        'embedding' : embedding,
        'position' : position,
        'combined' : combined,
        'query' : query,
        'key' : key,
        'value' : value,
        'qk' : qk, # Q * K
        'scaled': scaled, # apply scaled dot product
        'attention': attention, # smx(scaled_qk)
        'attn_value': attn_value, # attn * value
        'w_linear': w_linear, # weights
        'linear' : linear, # raw linear output
        'relu' : relu, # after relu
        'norm' : norm, # after layer norm
        'decoder' : decoder,
        'final': final,
        }

    return l

fake = [sample_to_layers(s) for s in (neg,pos)]

with open(save_as, "wb") as f:
    pickle.dump(fake, f)

print('Finished dumping fake data.')
