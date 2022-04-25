import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from pages.maindash import app
from pages.attn import attn as attn_layer
from pages import single

"""
Flask uses this. The callback to the Dash app will reactively load page content.
"""

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return single.get_layout() # experimental single scroll
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
