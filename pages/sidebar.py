import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
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
    sidebar_header = dbc.Row([
        dcc.Link(
            html.H2([
                html.Span("Pretty\n", style={"color":"#cc4778"}),
                html.Span("Transformers", style={"color":"#7e03a8"}),
                ]),
            href='/app', style={"text-decoration":"none"})
        ])

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
                #style={'text-align':'center'},
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Nav(
                [
                    dbc.NavLink("Intro", href="/"),
                    dbc.NavLink("Task", href="#task-section"),
                    dbc.NavLink("Embeddings", href="#embed-section"),
                    dbc.NavLink("Attention", href="#attn-section"),
                    dbc.NavLink("Nonlinearity", href="#nln-section"),
                    dbc.NavLink("Decoder", href="#decoder-section"),
                ],
                vertical=True,
                pills=True,
            ),
            html.Div(
                [
                    html.Hr(),
                    html.P("Switch between samples!"),
                    make_dropdown(params),
                ],
                style={"text-align": "center"},
            ),
            html.Div([
                html.Hr(),
                dcc.Link("about pretty transformers", href="/about"),
                ], style={'text-align':'center'}),
        ],
        id="sidebar",
    )
    return sidebar_layout
