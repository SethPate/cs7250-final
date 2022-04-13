import numpy as np
import random
import dash_cytoscape as cyto
from scipy.special import softmax
from .style import stylesheet

def calc_div_height(words):
    return len(words) * 20 + 60 + 20

def get_cyto_layout(words, params):
    div_height = calc_div_height(words)
    elements = get_node_dicts(words, params) + get_node_headers(params)

    layout = cyto.Cytoscape(
    id="explorer-view",
    layout={"name": "preset", "fit": True},
    style={"width": "100%", "height": f"{div_height}px"},
    panningEnabled=False,
    zoomingEnabled=False,
    elements=elements,
    stylesheet=stylesheet,
    autoungrabify=True,
    autounselectify=False,
    )

    return layout

def get_node_dicts(cyto_data, params):
    words = cyto_data['words']
    attn = cyto_data['attn']
    attn_smx = softmax(attn, axis=1) # sum over columns

    element_list = []

    # first column: Input Words
    column = 0
    for i, word_input in enumerate(words):
        element_list.append(
            {
                "data": {"id": f"word_{i}_input", "label": word_input},
                "position": {
                    "x": params["x_first_node"]
                    + column * params["x_space_between_nodes"],
                    "y": params["y_first_node"] + i * params["y_space_between_nodes"],
                },
                "classes": "node-word",
            }
        )

    # first column: Attended Words
    column = 1
    for j, word_attention in enumerate(words):
        element_list.append(
            {
                "data": {"id": f"word_{j}_attention", "label": word_attention},
                "position": {
                    "x": params["x_first_node"]
                    + column * params["x_space_between_nodes"],
                    "y": params["y_first_node"] + j * params["y_space_between_nodes"],
                },
                "classes": "node-word",
            }
        )

        # edges between words 
        for i, word_input in enumerate(words):
            element_list.append(
                {
                    "data": {
                        "id": f"word_{i}_attention_{j}",
                        "label": word_attention,
                        "target": f"word_{j}_attention",
                        "source": f"word_{i}_input",
                        "weight": round(attn_smx[j][i] * 6,2)
                    },
                    "classes": "edge-attention",
                }
            )

    # feedforward layer
    column = 2
    for z in range(len(words)):
        element_list.append(
            {
                "data": {
                    "id": f"word_{z}_output",
                    "label": "",
                    "color": random.choice(
                        ["blue", "lightblue", "cyan", "pink", "red"]
                    ),
                },
                "position": {
                    "x": params["x_first_node"]
                    + column * params["x_space_between_nodes"],
                    "y": params["y_first_node"] + z * params["y_space_between_nodes"],
                },
                "classes": "node-output",
            }
        )
        for j, word_input in enumerate(words):
            element_list.append(
                {
                    "data": {
                        "id": f"attention_{j}_output_{z}",
                        "source": f"word_{j}_attention",
                        "target": f"word_{z}_output",
                        "weight": np.random.rand() * 0.25,
                    },
                    "classes": "edge-attention",
                }
            )

    # last linear layer
    column = 3
    element_list.append(
        {
            "data": {
                "id": "classification_result",
                "label": "",
                "color": "red",
            },
            "position": {
                "x": params["x_first_node"] + column * params["x_space_between_nodes"],
                "y": params["y_first_node"]
                + len(words) // 2 * params["y_space_between_nodes"],
            },
            "classes": "node-class",
        }
    )

    return element_list


# TODO: disable interactivity for all nodes that shouldn't have it -for example, headers-


def get_node_headers(params):
    return [
        {
            "data": {"id": "header_input", "label": "Input words"},
            "position": {"x": params["x_first_node"], "y": params["y_first_node"] - 40},
            "classes": "node-header",
        },
        {
            "data": {"id": "header_attention", "label": "Attended words"},
            "position": {
                "x": params["x_first_node"] + params["x_space_between_nodes"],
                "y": params["y_first_node"] - 40,
            },
            "classes": "node-header",
        },
        {
            "data": {"id": "header_output", "label": "Output"},
            "position": {
                "x": params["x_first_node"] + params["x_space_between_nodes"] * 2,
                "y": params["y_first_node"] - 40,
            },
            "classes": "node-header",
        },
        {
            "data": {"id": "header_class", "label": "Class"},
            "position": {
                "x": params["x_first_node"] + params["x_space_between_nodes"] * 3,
                "y": params["y_first_node"] - 40,
            },
            "classes": "node-header",
        },
    ]
