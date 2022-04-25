import numpy as np
from dash import dcc, html
import plotly.express as px

def matrix_fig(matrix, title, ylabels=None):
    fig = px.imshow(
        matrix,
        labels = dict(x='data dimension (d)',
                    y='tokens (T)',
                    color='value'),
        y=ylabels,
        #zmin=-3,
        #zmax=3,
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
    div = html.Div(graph)
    return div 
