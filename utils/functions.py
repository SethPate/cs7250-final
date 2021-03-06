import plotly.express as px
from dash import dcc, html


def update_fig(params, key, title,
        labels=dict(x="data dimension (d)", y="tokens (T)", color="value")):
    ix = params["current_sample_ix"]
    data = params["layerdata"][ix][key]  # np.array(t,d)
    return matrix_fig(data, title, key, labels=labels)


def matrix_fig(matrix, title, key=None, ylabels=None, 
        labels=dict(x="data dimension (d)", y="tokens (T)", color="value")):

    if key == "final":
        valmin = 0
        valmax = 1
    else:
        valmin = valmax = None

    fig = px.imshow(
        matrix,
        labels=labels,
        y=ylabels,
        zmin=valmin,
        zmax=valmax,
        aspect="equal",
        title=title,
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(
        font_family="Lato",
        font_size=16,
    )
    # graph = dcc.Graph(
    #    figure=fig,
    #    config={"displaylogo": False},
    #    responsive=True,
    # )
    # div = html.Div(graph)
    return fig
