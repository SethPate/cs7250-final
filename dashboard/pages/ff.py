from dash import html
from dash import dcc
import plotly.express as px
from pages.maindash import app
from dash.dependencies import Input,Output

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
    fig = px.imshow(ff)
    return dcc.Graph(figure=fig)

@app.callback(Output("ff-figure","children"),
            Input("datastore","data"))
def update_ff(data):
    if not data:
        return
    else:
        return make_ff_fig(data)
