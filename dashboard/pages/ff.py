from dash import html

def get_layout():
    layout = html.Div([
        html.H1("Feedforward", id="ff-section"),
        html.Hr(),
        html.P("And how about those MLPs, huh?"),
        html.Hr(),
        html.P("whole buncha science"),
        ])
    return layout
