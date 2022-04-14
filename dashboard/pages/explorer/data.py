import dash_cytoscape as cyto
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.colors as mcol
import numpy as np
from utils.functions import softmax

from .style import stylesheet


def get_dummy_sentences(params):
    raw_sentences = [
            "I went and saw this movie last night after being coaxed to by a few friends of mine. I'll admit that I was reluctant to see it because from what I knew of Ashton Kutcher he was only able to do comedy.",
            "I think this is one of those few movies that I want to rate it as low as possible just to pay it a compliment."
    ]
    sentences = [sentence.split(" ") for sentence in raw_sentences]
    attention_weights = [
        softmax(np.random.random((len(sentence), len(sentence))) * 100, axis=1)
        for sentence in sentences
    ]
    scores = [
        np.random.random(params["n_weights_ff"]).reshape(16, -1)
        for sentence in sentences
    ]

    dict_sentences = {
        "raw_sentences": raw_sentences,
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
    for z_i in range(len(scores)):
        for z_j in range(len(scores[0])):
            element_list.append(
                {
                    "data": {
                        "id": f"ff_{z_i}_{z_j}_output",
                        "label": "",
                        "color": mcolors.to_hex(cm.bwr(scores[z_i][z_j])),
                    },
                    "position": {
                        "x": params["x_first_node"]
                        + column * params["x_space_between_nodes"]
                        - 50
                        + z_j * params["x_space_between_nodes_ff"],
                        "y": params["y_first_node_ff"]
                        + 15
                        + z_i * params["y_space_between_nodes_ff"],
                    },
                    "classes": "node-output",
                }
            )
        # for j, word_input in enumerate(words):
        #     element_list.append(
        #         {
        #             "data": {
        #                 "id": f"attention_{j}_output_{z}",
        #                 "source": f"word_{j}_attention",
        #                 "target": f"word_{z}_output",
        #                 "weight": np.random.rand() * 0.25,
        #             },
        #             "classes": "edge-attention",
        #         }
        #     )

    column = 3

    element_list.append(
        {
            "data": {
                "id": "classification_result",
                "label": "",
                "color": mcolors.to_hex(cm.bwr(np.mean(scores))),
            },
            "position": {
                "x": params["x_first_node"] + column * params["x_space_between_nodes"],
                "y": (params["max_nodes_to_visualize"] // 2)
                * params["y_space_between_nodes"]
                + 7,
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
            "height": f"{params['max_nodes_to_visualize']*20+4}px",
        },
        panningEnabled=False,
        zoomingEnabled=False,
        elements=elements,
        stylesheet=stylesheet,
        autoungrabify=True,
        autounselectify=False,
    )
    return layout_cytoscape
