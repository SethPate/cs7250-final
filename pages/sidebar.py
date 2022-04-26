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


def make_dropdown():
    samples = [0, 1]
    strs = ["negative :(", "positive :)"]
    sample_ids = [f"sample {samples[i]+1} - {strs[i]}" for i in range(len(samples))]
    return html.Div(
        [
            dcc.Dropdown(sample_ids, sample_ids[0], id="dropdown-samples", clearable=False),
        ],
    )


def get_sidebar():

    sidebar_header = dbc.Row([
        dcc.Link(
            html.H2([
                html.Span("Pretty\n", style={"color":"#cc4778"}),
                html.Span("Transformers", style={"color":"#7e03a8"}),
                ]),
            href='/', style={"text-decoration":"none"})
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
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Nav(
                [
                    dbc.NavLink("Intro", href="/#start"),
                    dbc.NavLink("Task", href="/#task-section", external_link=True),
                    dbc.NavLink("Embeddings", href="/#embed-section", external_link=True),
                    dbc.NavLink("Attention", href="/#attn-section", external_link=True),
                    dbc.NavLink("Nonlinearity", href="/#nln-section", external_link=True),
                    dbc.NavLink("Decoder", href="/#decoder-section", external_link=True),
                ],
                vertical=True,
                pills=True,
            ),
            html.Div(
                [
                    html.Hr(),
                    html.P("Switch between samples!"),
                    make_dropdown(),
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
