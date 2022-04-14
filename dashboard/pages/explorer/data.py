import dash_cytoscape as cyto
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.colors as mcol
import numpy as np
from utils.functions import softmax

from .style import stylesheet


def get_dummy_sentences():
    sentences = ["I am a sentence with several words!", "What a great day! Let's go out!", "a b c d e f g h i j k"]
    sentences = [sentence.split(" ") for sentence in sentences]
    attention_weights = [
        softmax(np.random.random((len(sentence), len(sentence))) * 100, axis=1)
        for sentence in sentences
    ]

    scores = [np.random.random(len(sentence)) for sentence in sentences]

    dict_sentences = {
        "sentences": sentences,
        "attention_weights": attention_weights,
        "scores": scores,
    }
    return dict_sentences


def get_node_dicts(params):
    current_sample = params["current_sample"]
    words = params["sentences"][current_sample]
    scores = params["scores"][current_sample]
    attention_weights = params["attention_weights"][current_sample]
    element_list = []
    for i, word_input in enumerate(words):
        column = 0
        element_list.append(
            {
                "data": {"id": f"word_{i}_input", "label": word_input},
                "position": {
                    "x": params["x_first_node"]
                    + column * params["x_space_between_nodes"],
                    "y": params["y_first_node"]
                    + (params["current_top_node_word"] + i)
                    * params["y_space_between_nodes"],
                },
                "classes": "node-word",
            }
        )

    for j, word_attention in enumerate(words):
        column = 1
        element_list.append(
            {
                "data": {"id": f"word_{j}_attention", "label": word_attention},
                "position": {
                    "x": params["x_first_node"]
                    + column * params["x_space_between_nodes"],
                    "y": params["y_first_node"]
                    + (params["current_top_node_attention"] + j)
                    * params["y_space_between_nodes"],
                },
                "classes": "node-word",
            }
        )
        for i, word_input in enumerate(words):
            element_list.append(
                {
                    "data": {
                        "id": f"word_{i}_attention_{j}",
                        "label": word_attention,
                        "target": f"word_{j}_attention",
                        "source": f"word_{i}_input",
                        "weight": attention_weights[i][j],
                    },
                    "classes": "edge-attention",
                }
            )

    column = 2
    for z in range(len(words)):
        element_list.append(
            {
                "data": {
                    "id": f"word_{z}_output",
                    "label": "",
                    "color": mcolors.to_hex(cm.bwr(scores[z])),
                },
                "position": {
                    "x": params["x_first_node"]
                    + column * params["x_space_between_nodes"],
                    "y": params["y_first_node"]
                    + (params["current_top_node_attention"] + z)
                    * params["y_space_between_nodes"],
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
                "y": len(words) // 2 * params["y_space_between_nodes"] - 10,
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


def get_cyto_layout(params):
    elements = get_node_dicts(params)  # + data.get_node_headers(params)
    layout_cytoscape = cyto.Cytoscape(
        id="explorer-view-cytoscape",
        layout={"name": "preset", "fit": True},
        style={
            "width": "800px",
            "height": f"{params['max_nodes_to_visualize']*20+3}px",
        },
        panningEnabled=False,
        zoomingEnabled=False,
        elements=elements,
        stylesheet=stylesheet,
        autoungrabify=True,
        autounselectify=False,
    )
    return layout_cytoscape
