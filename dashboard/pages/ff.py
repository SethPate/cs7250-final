from dash import html
from dash import dcc
import plotly.express as px
from maindash import app
from dash.dependencies import Input,Output
from utils.functions import matrix_fig

def get_layout(params):
    layout = html.Div([
        html.H1("Feedforward", id="ff-section"),
        html.Hr(),
        dcc.Markdown('''
        ## purpose of a feedforward layer

        Nonlinearities. See example of transform and relu. What is a relu?
        - show unbalanced 'before' transformation
        - show unbalanced 'after' transformation
        '''),
        html.Div(id='after-linear'),
        dcc.Markdown('''
        ## residual connections
        - show two layers normally
        - show three layers residually
        '''),
        dcc.Markdown('''
        ## layer norm

        Transform the outputs of a certain layer to mean 0 and std 1.
        Layer normalization is an alternative to batch normalization.

        - show 'after'
        - show post batch norm
        - show post layer norm
        ''')
        ])
    return layout



@app.callback(Output("after-linear","children"),
            Input("datastore","data"))
def update_after_linear(params):
    if not params:
        return
    else:
        ix = params['current_sample_ix']
        linear = params['layerdata'][ix]['linear'] # np.array(t,d)
        return matrix_fig(linear, "feedforward output")
