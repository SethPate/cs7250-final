import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from maindash import app
from utils.functions import matrix_fig

def get_layout(params):
    layout = html.Div([
        html.H1("Nonlinearity", id="nln-section"),
        html.Hr(),
        dcc.Markdown('''
        ## purpose of a feedforward layer

        Nonlinearities. See example of transform and relu. What is a relu?
        - show unbalanced 'before' transformation
        - show unbalanced 'after' transformation
        '''),
        html.Div(id='linear'),
        dcc.Markdown('''
        ## residual connections
        - show two layers normally
        - show three layers residually
        '''),
        html.Div(id='relu'),
        dcc.Markdown('''
        ## layer norm

        Transform the outputs of a certain layer to mean 0 and std 1.
        Layer normalization is an alternative to batch normalization.

        '''),
        html.Div(id='norm'),
        ])
    return layout

def update_fig(params, key, title):
    ix = params['current_sample_ix']
    data = params['layerdata'][ix][key] # np.array(t,d)
    return matrix_fig(data, title)

@app.callback(Output("linear","children"),
            Input("datastore","data"))
def update_linear(params):
    if not params:
        return
    else:
        return update_fig(params, 'linear', "linear")

@app.callback(Output("relu","children"),
            Input("datastore","data"))
def update_relu(params):
    if not params:
        return
    else:
        return update_fig(params, "relu", "ReLU")

@app.callback(Output("norm", "children"),
            Input("datastore","data"))
def update_norm(params):
    if not params:
        return
    else:
        return update_fig(params, "norm", "normalized")
