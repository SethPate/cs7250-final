from dash import html
from dash import dcc
import plotly.express as px
from maindash import app
from dash.dependencies import Input,Output
from utils.functions import matrix_fig

explain = dcc.Markdown('''
    ## purpose of a feedforward layer

    Nonlinearities. See example of transform and relu. What is a relu?
    - show unbalanced 'before' transformation
    - show unbalanced 'after' transformation

    ## residual connections
    - show two layers normally
    - show three layers residually

    ## layer norm

    Transform the outputs of a certain layer to mean 0 and std 1.
    Layer normalization is an alternative to batch normalization.

    - show 'after'
    - show post batch norm
    - show post layer norm

    ''')

def get_layout(params):
    layout = html.Div([
        html.H1("Feedforward", id="ff-section"),
        html.Hr(),
        explain,
        html.Div(id='ff-figure'),
        ])
    return layout

def make_ff_fig(params):
    ix = params['current_sample_ix']
    ff = params['layerdata'][ix]['linear_1'] # np.array(t,d)
    return matrix_fig(ff, "feedforward output")

@app.callback(Output("ff-figure","children"),
            Input("datastore","data"))
def update_ff(data):
    if not data:
        return
    else:
        return make_ff_fig(data)
