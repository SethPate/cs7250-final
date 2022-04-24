from dash import html
from dash import dcc

explain = dcc.Markdown('''
    ## purpose of a feedforward layer

    Nonlinearities. See example of transform and relu. What is a relu?

    ## layer norm

    Transform the outputs of a certain layer to mean 0 and std 1.

    Layer normalization is an alternative to batch normalization.

    ## scaling

    Scaling is meant to 'stabilize' training by reducing the
    'temperature' of the softmax.
    ''')

def get_layout():
    layout = html.Div([
        html.H1("Feedforward", id="ff-section"),
        html.Hr(),
        explain,
        ])
    return layout
