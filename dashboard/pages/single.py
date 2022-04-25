import pickle

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app
from scipy.special import softmax

from . import decoder
from . import embed
from . import intro
from . import nln
from . import sidebar
from .attn import attn

"""
Experimental single scroll layout.
"""

fake_data_path = "./data/fake_data.pickl"


def get_dummy_data(params):
    """
    Called by view.py to supplement params.
    Returns a list of samples.
    Each sample has the following keys:
        sample,
        embedding, position, combined,
        query, key, value,
        qk, scaled, attention, attn_value,
        w_linear, linear, relu, norm,
        decoder, final
    """
    with open(fake_data_path, "rb") as f:
        fake_data = pickle.load(f)

    return fake_data


def make_single_layout():
    """Pulls together all the content and structure pages."""

    # init params and grab data
    params = {
        "current_sample_ix": 0,
        "selected_word_ix": 0,
    }
    params["update_figs"] = True
    params["layerdata"] = get_dummy_data(params)

    # make all the layouts and put em together
    loc = dcc.Location(id="url")
    sb = sidebar.sidebar_layout
    content = html.Div(
        [
            intro.make_layout(params),
            html.Div(embed.make_layout(params), id="embed-section"),
            attn.get_layout(params),
            nln.get_layout(params),
            decoder.get_layout(),
        ],
        id="page-content",
    )

    return html.Div([loc, sb, content])


# Test case to show the selection reactively
@app.callback(Output("display", "children"), Input("datastore", "data"))
def displayer(data):
    return data["selected_word_ix"]


"""
Update the data to reflect a selected word from the cytoscape.
"""


@app.callback(
    Output("datastore", "data"),
    Input("attn-cyto", "selectedNodeData"),
    Input("attn-cyto", "mouseoverNodeData"),
    Input("dropdown-samples", "value"),
    State("datastore", "data"),
)
def selectHelper(selections, mouseover, dropdown_value, data):
    sample = int(dropdown_value.split(" ")[-1]) - 1
    if sample != data["current_sample_ix"]:
        data["current_sample_ix"] = sample
        data["update_figs"] = True
    else:
        data["update_figs"] = True
    if selections:
        data["selected_word_ix"] = selections[0]["ix"]
    elif mouseover:
        data["selected_word_ix"] = mouseover["ix"]
    else:
        data["selected_word_ix"] = None
    return data


@app.callback(Output("embed-section", "children"), Input("datastore", "data"))
def update_embed(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return embed.make_layout(params)
