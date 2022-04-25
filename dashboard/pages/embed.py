from dash import html
from dash import dcc
from utils.functions import matrix_fig

"""
Section for how embeddings work.
Demonstrate the initial embedding, the position embed,
and how the two are combined.
"""

# blurb to explain things
explain = dcc.Markdown('''
    ## how embeddings work

    Humans use words, but computers only understand numbers.
    (actually, they only understand two numbers. Computers are pretty
    dumb).
    So before we can use our Transformer, we have to turn our sentence
    into a bunch of numbers.

    Here, click on one of the words to see how it works.

    When you choose a word, you are looking up its value in a dictionary
    called an **embedding layer**. In this case, the embedding layer
    simply assigns each word a set of 128 random floating point values,
    in something approaching a standard normal distribution.

    The result of the dictionary lookup -- the 'definition' of the word --
    is called an **embedding**.

    ## adding position information

    Transformer models don't have any inherent sense of position.
    To the Transformer, both of these sequences look the same:

    This is a good thing, because then they can do most of their work
    in parallel, as we'll see later.
    In the bad old days of 2016, recurrent models with LSTMs had to
    work in series, and that took forever, limiting our dataset size.

    But because word order is definitely important to humans, we have to
    'add' the information about word order into our embeddings. This sort
    of makes sense, right? The embedding is already representing the
    *semantic* meaning of the word. We just have to add the *syntax*
    information to the embedding.

    As it turns out, we can do this by literally adding another special
    vector, the **position encoding**, which we keep on hand for
    just this task.

    Here's those words from earlier. We just have to line them up with our
    position encodings and then add the two matrices together.

    As you can see, each embedding has been changed. Now you can see
    that the embeddings do have some bearing on the original position of
    the words in the sentence.
    ''')

def make_layout(params):
    ix = params['current_sample_ix']
    layerdata = params['layerdata'][ix]

    # make figures to show embeddings
    sample = layerdata['sample']
    embed = layerdata['embedding']
    position_fig = matrix_fig(embed[:5], "word embeddings",
        ylabels=sample[:5])

    layout = html.Div([
        html.H1("Embeddings"),
        html.Hr(),
        explain,
        position_fig,
    ])

    return layout
