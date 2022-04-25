import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


def make_dropdown(params):
    samples = [0, 1]
    sample_ids = [f"Sample {i+1}" for i in samples]
    return html.Div(
        [
            dcc.Dropdown(sample_ids, sample_ids[0], id="dropdown-samples"),
        ],
    )


def get_sidebar(params):

    # we use the Row and Col components to construct the sidebar header
    # it consists of a title, and a toggle, the latter is hidden on large screens
    sidebar_header = dbc.Row(
        [
            dbc.Col(html.H2("Visualizing transformers"), className="text-center"),
            html.Br(),
            dbc.Col(
                [
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="navbar-toggle",
                    ),
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="sidebar-toggle",
                    ),
                ],
                # the column containing the toggle will be only as wide as the
                # toggle, resulting in the toggle being right aligned
                width="auto",
                # vertically align the toggle in the center
                align="center",
            ),
        ]
    )

    sidebar_layout = html.Div(
        [
            sidebar_header,
            # we wrap the horizontal rule and short blurb in a div that can be
            # hidden on a small screen
            html.Div(
                [
                    html.Hr(),
                    html.P(
                        "A tool for visualizing input data as it advances through a Transformer architecture.",
                        className="lead",
                    ),
                ],
                id="blurb",
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavLink(html.A("Home", href="#home"), active="exact"),
                        dbc.NavLink(
                            html.A("Embeddings", href="#embed-section"), active="exact"
                        ),
                        dbc.NavLink(
                            html.A("Attention", href="#attn-section"), active="exact"
                        ),
                        dbc.NavLink(
                            html.A("Nonlinearity", href="#nln-section"), active="exact"
                        ),
                        dbc.NavLink(
                            html.A("Decoder", href="#decoder-section"), active="exact"
                        ),
                    ],
                    vertical=True,
                    pills=True,
                ),
                id="collapse",
            ),
            make_dropdown(params),
        ],
        id="sidebar",
    )
    return sidebar_layout
