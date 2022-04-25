from dash import dcc, html
from dash.dependencies import Input,Output,State
from maindash import app

def make_layout(params):

    return html.Div(
        [
            dcc.Markdown('''
            Transformer networks are the basic technology powering many
            new AI products, including:
            * [Google Pathways Language Model](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html), which explain bad jokes about TPU 'pods',
            * arst
            '''),
            html.Div(id='show-sample'),
        ],
        id="home",
    )

@app.callback(Output("show-sample","children"),
        Input("datastore","data"))
def update_sample(params):
    if not params:
        return
    else:
        ix = params["current_sample_ix"]
        sample = params["layerdata"][ix]["sample"]
        return html.P(sample)
