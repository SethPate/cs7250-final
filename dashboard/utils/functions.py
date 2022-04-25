import numpy as np
from dash import dcc
import plotly.express as px

def matrix_fig(matrix, title, ylabels=None):
    fig = px.imshow(
        matrix,
        labels = dict(x='data dimension (d)',
                    y='tokens (T)',
                    color='value'),
        y=ylabels,
        aspect='equal',
        title = title)
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(
        font_family="Lato",
        font_size=16,
        )
    graph = dcc.Graph(figure=fig,
        config={'displaylogo':False},
        responsive=True,
        )
    return graph 
