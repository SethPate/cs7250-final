from .attn import attn
from . import ff
from dash import html
from dash import dcc

from . import sidebar

"""
Experimental single scroll layout.
"""

def make_single_layout():
    loc = dcc.Location(id="url")
    sb = sidebar.sidebar_layout
    content = html.Div([
        attn.get_layout(),
        ff.get_layout(),
        ])
    return html.Div([loc, sb, content])
    
