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
    Input("button-sample-back", "n_clicks"),
    Input("button-sample-forward", "n_clicks"),
    State("explorer-view-store", "data"),
)
def update_explorer_view_store(
    btn_word_up,
    btn_word_down,
    btn_attn_up,
    btn_attn_down,
    btn_sample_back,
    btn_sample_forward,
    cytoscape_params,
):
    id_btn = [p["prop_id"] for p in callback_context.triggered][0]
    len_cur_word = len(
        cytoscape_params["sentences"][cytoscape_params["current_sample"]]
    )
    if "button-word-up" in id_btn:
        if cytoscape_params["current_top_node_word"] < 0:
            cytoscape_params["current_top_node_word"] += 1
    if "button-word-down" in id_btn:
        if (
            cytoscape_params["current_top_node_word"]
            > cytoscape_params["max_nodes_to_visualize"] - len_cur_word
        ):
            cytoscape_params["current_top_node_word"] -= 1
    if "button-attention-up" in id_btn:
        if cytoscape_params["current_top_node_attention"] < 0:
            cytoscape_params["current_top_node_attention"] += 1
    if "button-attention-down" in id_btn:
        if (
            cytoscape_params["current_top_node_attention"]
            > cytoscape_params["max_nodes_to_visualize"] - len_cur_word
        ):
            cytoscape_params["current_top_node_attention"] -= 1
    if "button-sample-back" in id_btn:
        if cytoscape_params["current_sample"] > 0:
            cytoscape_params["current_sample"] -= 1
            cytoscape_params["current_top_node_attention"] = 0
            cytoscape_params["current_top_node_word"] = 0
    if "button-sample-forward" in id_btn:
        if cytoscape_params["current_sample"] < len(cytoscape_params["sentences"]) - 1:
            cytoscape_params["current_sample"] += 1
            cytoscape_params["current_top_node_attention"] = 0
            cytoscape_params["current_top_node_word"] = 0
    return cytoscape_params


@app.callback(
    Output("explorer-view-cytoscape", "elements"),
    Input("explorer-view-store", "data"),
)
def update_elements(cytoscape_params):
    return get_node_dicts(cytoscape_params)


@app.callback(
    Output("text-id-sample", "children"),
    Input("explorer-view-store", "data"),
)
def update_id_sample(cytoscape_params):
    sample_id = cytoscape_params["current_sample"]
    return f"Sample {str(sample_id+1).zfill(3)}"


@app.callback(
    Output("text-sentence", "children"),
    Input("explorer-view-store", "data"),
)
def update_text_sentence(cytoscape_params):
    sample_id = cytoscape_params["current_sample"]
    return cytoscape_params["raw_sentences"][sample_id]
