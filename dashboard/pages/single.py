from dash import html
from dash import dcc

from . import sidebar
from .attn import attn
from . import ff
from . import embed

"""
Experimental single scroll layout.
"""

def make_single_layout():
    loc = dcc.Location(id="url")
    sb = sidebar.sidebar_layout
    content = html.Div([
        embed.make_layout(),
        attn.get_layout(),
        ff.get_layout(),
        ])
    return html.Div([loc, sb, content])
    
