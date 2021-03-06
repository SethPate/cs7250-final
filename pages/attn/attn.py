import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app
from utils.functions import matrix_fig
from utils.functions import update_fig

from .style import stylesheet  # specific to cytoscape

WORDS_PER_ROW = 7  # at 800px width

def get_elements(params):
    """Makes nodes for the cytoscape."""

    element_list = []

    sample_ix = params["current_sample_ix"]
    words = params["layerdata"][sample_ix]["sample"]
    wordmap = get_wordmap(words)
    element_list += wordmap

    return element_list


def get_spans(params):
    """
    Displayed below the cytoscape. Shows attention by modifying
    word opacity according to the attention value, relative to the selected word.
    """

    sample_ix = params["current_sample_ix"]
    selected_word_ix = params["selected_word_ix"]
    words = params["layerdata"][sample_ix]["sample"]
    attn_weights = params["layerdata"][sample_ix]["attention"]

    if selected_word_ix is None:  # need not be selected
        attn = np.ones(len(words))
    else:
        attn = [
            #attn_weights[selected_word_ix][i] if i != selected_word_ix else 1.0
            attn_weights[selected_word_ix][i]
            for i in range(len(words))
        ]

    # set minimum opacity
    opacity = np.array(attn)
    opacity[opacity < 0.2] = 0.1

    spans = []
    tooltips = []
    for i, w in enumerate(words):
        display = w + " "
        o = opacity[i]
        a = attn[i]
        _id = f"span_{i}"
        span = html.Span(
            display,
            id=_id,
            className="attn-text",
            style={"opacity": o, "display": "inline-block", "padding": "2px"},
        )
        spans.append(span)
        tooltip = dbc.Tooltip(
            f"attn value: {round(a,2)}", target=_id, id="tooltip" + _id, placement = "bottom-start"
        )
        tooltips.append(tooltip)

    # tooltips to show attn value on hover
    return spans, tooltips


def get_wordmap(words):
    """
    Nodes for the cytoscape. 'ix' refers to the word order in the sentence.
    """

    elements = []
    for i, w in enumerate(words):
        word_node = {
            "data": {"id": f"word_{i}", "ix": i, "label": w},
            "classes": "node-word",
        }
        elements.append(word_node)
    return elements


def get_cyto_layout(params, n_rows):
    elements = get_elements(params)

    layout_cytoscape = cyto.Cytoscape(
        id="attn-cyto",
        layout={
            "name": "grid",
            "fit": True,
            "cols": WORDS_PER_ROW,
            "avoidOverlapPadding": 5,
            "condense": True,
        },
        style={
            "width": "800px",
            "height": f"{n_rows * 30 + 10}px",
        },
        panningEnabled=False,
        zoomingEnabled=False,
        elements=elements,
        stylesheet=stylesheet,
        autoungrabify=True,
        autounselectify=False,
    )

    return layout_cytoscape


def get_layout(params):
    """
    Construct the whole attention module, including the cytoscape element
    at the center.
    """


    current_sample_ix = params["current_sample_ix"]
    words = params["layerdata"][current_sample_ix]["sample"]

    # paragraph = html.P(" ".join(words))

    rows = len(words) // WORDS_PER_ROW
    cyto_layout = get_cyto_layout(params, n_rows=rows)

    spans, tooltips = get_spans(params)
    spans += tooltips  # roll tolltips into layout

    layout = html.Div(
        [
            dcc.Store(id="datastore", data=params),
            html.H1("Attention", id="attn-section"),
            html.Hr(),
            dcc.Markdown(
                """
                ## query, key, and value self-attention

                The embedding layer turned our sample into an
                **embedding matrix** of size **(T,d)**.
                Now our Transformer has to **encode** this information
                so that we can do useful things with it, like
                decide whether or not Ashton Kutcher is a good actor.

                The Transformer will do this through **self-attention**.
                This simply means that the Transformer will assign meaning
                to each word according to its relationship to all the *other*
                words in the sample. That relationship is called **attention**,
                and words that are closely related are said to **attend** strongly
                to each other.

                The first step in self-attention is transforming our **embedding matrix**
                into three different matrices: the **query, key** and **value** matrices.
                Each matrix is shaped the same as the original embedding, (T,d).
                Here's what they look like for a few of the words in our sample.
                """
            ),
            html.Div(dcc.Graph(id="q")),
            html.Div(dcc.Graph(id="k")),
            html.Div(dcc.Graph(id="v")),
            dcc.Markdown(
                """
                If you were to multiply the **query** and **key** matrices, you would
                end up with a square matrix, filled with the **dot product** of every word's
                query vector and every other word's value vector:
                """
            ),
            html.Div(dcc.Graph(id="qk")),
            dcc.Markdown(
                """
                Higher dot products will indicate stronger relationships, higher **attention**.

                ## scaled dot product attention

                These raw dot products can be turned into a **distribution** with the **softmax** function.
                But there is a problem. Dot products are **unbounded**, and as the vectors get longer
                (which happens when we increase the **dimension** of our model layers, to make them better),
                the dot products can run away. **Softmax** does not play nicely with runaway numbers;
                very large values can make softmax 'peaky', acting more like a regular **max** function.

                We don't want a peaky softmax, we want a distribution! So we scale the matrix by dividing
                it, *element wise*, by the square root of **d**. Now you can see that the values are under
                control again:
                """
            ),
            html.Div(dcc.Graph(id="scaled")),
            dcc.Markdown(
                """
                Now we can apply the softmax! And when we do, look at what we get -- **attention values**!
                """
            ),
            html.Div(dcc.Graph(id="attention")),
            dcc.Markdown(
                """
                The softmax changed every row into a distribution of numbers that sum to one.
                Values that were relatively high become very high, suppressing all the other numbers.
                The bright spots on this plot indicate word pairs (one x, one y) with **strong attention**.
                The model thinks there is some important relationship between those words,
                at least when it comes to classifying movie reviews.
                """
            ),
            html.Hr(),
            dcc.Markdown("""
                ## attention playground

                We've built a silly little widget for you to understand attention a little better.

                The grid below has words for all of your sample tokens. If you **click to select** a word,
                then the review below will change so that words are colored according to their **attention
                value**. The darkest words are the ones most relevant to your selection, according to the 
                Transformer. You can hover your mouse over the words below to see the exact attention score.
                """),
            cyto_layout,
            html.Br(),
            html.Div(id="span-holder", children=spans, className="sample-text"),
            html.Hr(),
            dcc.Markdown(
                """
                ## attention output

                We actually use the attention scores like **coefficients** or a **mask**.
                We multiply the mask with the **value** vector from earlier.
                Remember that **value** has one entry per word; it's shape **(T,d)**.
                So multiplying the attention matrix of **(T,T)** against **value**
                just results in another **(T,d)** matrix, the same shape as our input!
                
                But the attention process filtered that **value** data for us.
                Now the output will be weighted toward word pairs with strong attention values.
                """
            ),
            html.Div(dcc.Graph(id="attn-value")),
        ]
    )

    return layout


@app.callback(Output("attn-cyto", "elements"), Input("datastore", "data"))
def update_cyto(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return get_elements(params)


@app.callback(Output("q", "figure"), Input("datastore", "data"))
def update_q(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        ix = params["current_sample_ix"]
        layerdata = params["layerdata"][ix]
        sample = layerdata["sample"]
        q = layerdata["query"]
        qfig = matrix_fig(q[:5], "queries", ylabels=sample[:5])
        return qfig


@app.callback(Output("k", "figure"), Input("datastore", "data"))
def update_k(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        ix = params["current_sample_ix"]
        layerdata = params["layerdata"][ix]
        sample = layerdata["sample"]
        k = layerdata["key"]
        kfig = matrix_fig(k[:5], "keys", ylabels=sample[:5])
        return kfig


@app.callback(Output("v", "figure"), Input("datastore", "data"))
def update_v(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        ix = params["current_sample_ix"]
        layerdata = params["layerdata"][ix]
        sample = layerdata["sample"]
        v = layerdata["value"]
        vfig = matrix_fig(v[:5], "values", ylabels=sample[:5])
        return vfig


@app.callback(Output("qk", "figure"), Input("datastore", "data"))
def update_qk(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        labels = dict(x='tokens (T)', y='tokens (T)', color='value')
        fig = update_fig(params, "qk", "query * key", labels=labels)
        return fig


@app.callback(Output("scaled", "figure"), Input("datastore", "data"))
def update_scaled(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        labels = dict(x='tokens (T)', y='tokens (T)', color='value')
        fig = update_fig(params, "scaled", "scaled", labels=labels)
        return fig


@app.callback(Output("attention", "figure"), Input("datastore", "data"))
def update_attention(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        labels = dict(x='tokens (T)', y='tokens (T)', color='value')
        fig = update_fig(params, "attention", "attention", labels=labels)
        return fig


@app.callback(Output("attn-value", "figure"), Input("datastore", "data"))
def update_attn_value(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "attn_value", "attention * value")


@app.callback(Output("span-holder", "children"), Input("datastore", "data"))
def span_update(data):
    if not data:
        return
    else:
        spans, tooltips = get_spans(data)
        return spans + tooltips
