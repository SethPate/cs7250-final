import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from app import app
from pages.explorer import attn as attn_layer


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return attn_layer.get_layout()
    #elif pathname == gdp_page_location:
    #    return gdp.layout
    #elif pathname == iris_page_location:
    #    return iris.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
