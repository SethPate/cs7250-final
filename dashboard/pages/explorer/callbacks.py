from app import app
from dash import callback_context
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .data import get_node_dicts


# from dash.exceptions import PreventUpdate
@app.callback(
    Output("explorer-view-store", "data"),
    Input("button-word-up", "n_clicks"),
    Input("button-word-down", "n_clicks"),
    Input("button-attention-up", "n_clicks"),
    Input("button-attention-down", "n_clicks"),
    State("explorer-view-store", "data"),
)
def update_explorer_view_store(
    btn_word_up, btn_word_down, btn_attn_up, btn_attn_down, cytoscape_params
):
    id_btn = [p["prop_id"] for p in callback_context.triggered][0]
    if "button-word-up" in id_btn:
        if cytoscape_params["current_top_node_word"] < 0:
            cytoscape_params["current_top_node_word"] += 1
    if "button-word-down" in id_btn:
        if cytoscape_params["current_top_node_word"] > cytoscape_params[
            "max_nodes_to_visualize"
        ] - len(cytoscape_params["words"]):
            cytoscape_params["current_top_node_word"] -= 1
    if "button-attention-up" in id_btn:
        if cytoscape_params["current_top_node_attention"] < 0:
            cytoscape_params["current_top_node_attention"] += 1
    if "button-attention-down" in id_btn:
        if cytoscape_params["current_top_node_attention"] > cytoscape_params[
            "max_nodes_to_visualize"
        ] - len(cytoscape_params["words"]):
            cytoscape_params["current_top_node_attention"] -= 1
    return cytoscape_params


@app.callback(
    Output("explorer-view-cytoscape", "elements"),
    Input("explorer-view-store", "data"),
)
def update_elements(cytoscape_params):
    return get_node_dicts(cytoscape_params)
