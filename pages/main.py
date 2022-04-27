import pickle

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from maindash import app
from scipy.special import softmax

from . import intro, embed, nln, sidebar, decoder, about
from .attn import attn

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

# init params and grab data
params = {
    "current_sample_ix": -1,
    "selected_word_ix": 0,
}
params["update_figs"] = True
params["layerdata"] = get_dummy_data(params)

# app page
app_layout = html.Div(
    [
        intro.make_layout(params),
        embed.make_layout(params),
        attn.get_layout(params),
        nln.get_layout(params),
        decoder.get_layout(),
    ])

sidebar = sidebar.get_sidebar()


"""Pulls together all the content and structure pages."""
main_layout = html.Div([
    # make all the layouts and put em together
    dcc.Location(id="url"),
    sidebar,
    # start by displaying app
    html.Div(app_layout, id='page-content'),
    ])

"""
Manage multiple pages (for 'about' page)
"""
@app.callback(
    Output("page-content","children"),
    Input("url","pathname"))
def switch_pages(pathname):
    if pathname == '/about':
        return about.layout
    else:
        return app_layout

"""
Update the data to reflect a selected word from the cytoscape.
"""
@app.callback(
    Output("datastore", "data"),
    Input("attn-cyto", "selectedNodeData"),
    #Input("attn-cyto", "mouseoverNodeData"),
    Input("dropdown-samples", "value"),
    State("datastore", "data"),
)
def selectHelper(selections, dropdown_value, data):
    # hacks all day
    sample = int(dropdown_value[7]) - 1
    if sample != data["current_sample_ix"]:
        data["current_sample_ix"] = sample
        data["update_figs"] = True
    else:
        data["update_figs"] = True
    if selections:
        data["selected_word_ix"] = selections[0]["ix"]
    #elif mouseover:
    #    data["selected_word_ix"] = mouseover["ix"]
    else:
        data["selected_word_ix"] = None
    return data
