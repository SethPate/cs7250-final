import dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from maindash import app
from utils.functions import update_fig

"""
Section for how embeddings work.
Demonstrate the initial embedding, the position embed,
and how the two are combined.
"""

# blurb to explain things
md = [
    dcc.Markdown(
        """
    ## how embeddings work

    Humans use words, but computers only understand numbers.
    (actually, they only understand two numbers. Computers are pretty
    dumb).
    So before we can use our Transformer, we have to turn our sentence
    into a bunch of numbers.

    Here's how it looks for the first few words of our movie review:
    """
    ),
    dcc.Markdown(
        """
    When you choose a word, you are looking up its value in a dictionary
    called an **embedding layer**. In this case, the embedding layer
    simply assigns each word a set of 128 random floating point values,
    in something approaching a standard normal distribution. We call the
    size of the embedding **d**, for **dimension**.

    The result of the dictionary lookup -- the 'definition' of the word --
    is called an **embedding**. When we embed the entire text of **T** tokens,
    we end up with a matrix of shape **(T,d)**, the number of tokens by the
    size of each embedding.

    Here's how the whole sequence looks when embedded.
    """
    ),
    dcc.Markdown(
        """
    ## adding position information

    Transformer models don't have any inherent sense of position.

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
    """
    ),
    dcc.Markdown(
        """
    Here's those words from earlier. We just have to line them up with our
    position encodings and then add the two matrices together.

    As you can see, each embedding has been changed. Now you can see
    that the embeddings do have some bearing on the original position of
    the words in the sentence.
    """
    ),
]


def make_layout(params):
    layout = html.Div(
        [
            html.H1("Embeddings"),
            html.Hr(),
            md[0],  # markdown
            html.Div(dcc.Graph(id="embed_fig")),
            md[1],
            html.Div(dcc.Graph(id="embed_fig2")),
            md[2],
            html.Div(dcc.Graph(id="pos_fig")),
            md[3],
            html.Div(dcc.Graph(id="combo_fig")),
        ]
    )

    return layout


@app.callback(Output("embed_fig", "figure"), Input("datastore", "data"))
def update_embed_fig(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "embedding", "embed")


@app.callback(Output("embed_fig2", "figure"), Input("datastore", "data"))
def update_embed_fig2(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "embedding", "embed2")


@app.callback(Output("pos_fig", "figure"), Input("datastore", "data"))
def update_pos(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "position", "position")


@app.callback(Output("combo_fig", "figure"), Input("datastore", "data"))
def update_combo(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "combined", "words + position")
