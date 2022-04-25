from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app


def make_dropdown(params):
    ix = params["current_sample_ix"]
    samples = [0, 1]
    sample_ids = [f"Sample {i+1}" for i in samples]
    return html.Div(
        [
            dcc.Dropdown(sample_ids, sample_ids[0], id="dropdown-samples"),
        ],
    )


def make_layout(params):

    return html.Div(
        [
            dcc.Markdown(
                """
            Transformer networks are the basic technology powering many
            new AI products, including:
            * [Google Pathways Language Model](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html), which explain bad jokes about TPU 'pods',
            * arst
            """
            ),
            make_dropdown(params),
            html.Div(id="show-sample"),
        ],
        id="home",
    )


@app.callback(Output("show-sample", "children"), Input("datastore", "data"))
def update_sample(params):
    if not params:
        return
    else:
        ix = params["current_sample_ix"]
        sample = params["layerdata"][ix]["sample"]
        print(sample)
        return html.P(" ".join(sample))
