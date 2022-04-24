from dash import dcc
from dash import html

explain = dcc.Markdown('''
    Now that we have encoded the information from the sample,
    we have to **decode** it to answer our original question:
    was this a positive or negative movie review?

    In this simple 'binary classification' task, we only need a linear
    transformation to determine a single number. That number
    represents the model's confidence that the sample is positive.

    Logistic layer...

    Transformer models with more complicated tasks, like language modeling,
    have more complicated decoders. Translation network. Decoder-only.
''')

def get_layout():
    return html.Div([
        html.H1("Decoder"),
        html.Hr(),
        explain,
    ])
