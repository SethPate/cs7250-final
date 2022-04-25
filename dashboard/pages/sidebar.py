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
    strs = ["negative :(", "positive :)"]
    sample_ids = [f"Sample {samples[i]+1} - {strs[i]}" for i in range(len(samples))]
    return html.Div(
        [
            dcc.Dropdown(sample_ids, sample_ids[0], id="dropdown-samples", clearable=False),
        ],
    )


def get_sidebar(params):

    # we use the Row and Col components to construct the sidebar header
    # it consists of a title, and a toggle, the latter is hidden on large screens
    sidebar_header = dbc.Row(
        [
            dbc.Col(html.H2("Pretty Transformers"), className="text-center"),
        ]
    )

    sidebar_layout = html.Div(
        [
            sidebar_header,
            # we wrap the horizontal rule and short blurb in a div that can be
            # hidden on a small screen
            html.Div(
                [
                    html.Br(),
                    html.P(
                        "An exceedingly gentle introduction to the Transformer network.",
                        className="lead",
                    ),
                ],
                id="blurb",
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Nav(
                [
                    dbc.NavLink(html.A("Intro", href="#home"), active="exact"),
                    dbc.NavLink(html.A("Task", href="#task-section"), active="exact"),
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
            html.Div(
                [
                    html.Hr(),
                    html.P("Use the dropdown to switch between sample texts!"),
                    make_dropdown(params),
                ],
                style={"text-align": "center"},
            ),
        ],
        id="sidebar",
    )
    return sidebar_layout
