import pickle
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
    'linear-1',
    'linear-2',
    'decoder'
    ]

def sample_to_layers(s):
    sample = s.split(" ")
    t = len(sample) # number of tokens
    d = 128 # model hidden dimension

    embedding = np.random.random((t,d))
    position = np.random.random((t,d))
    combined = embedding + position

    query = np.random.random((t,d))
    key = np.random.random((t,d))
    value = np.random.random((t,d))

    attention = np.random.random((t,t))
    attention *= 50 # make softmax less uniform
    attention = softmax(attention, axis=1)

    linear_1 = np.random.random((t,d))
    linear_2 = np.random.random((t,d))
    decoder = np.random.random(1)

    l = {
        'sample' : sample, # list of words
        'embedding' : embedding,
        'position' : position,
        'combined' : combined,
        'query' : query,
        'key' : key,
        'value' : value,
        'attention' : attention,
        'linear_1' : linear_1,
        'linear_2' : linear_2,
        'decoder' : decoder,
        }

    return l

fake = [sample_to_layers(s) for s in (neg,pos)]

with open(save_as, "wb") as f:
    pickle.dump(fake, f)

print('Finished dumping fake data.')
