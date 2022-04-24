import numpy as np
from dash import dcc
import plotly.express as px

def matrix_fig(matrix, title):
    fig = px.imshow(
        matrix,
        labels = dict(x='data dimension (d)',
                    y='tokens (T)',
                    color='value'),
        title = title)
    return dcc.Graph(figure=fig,
        config={'displaylogo':False}
        )
