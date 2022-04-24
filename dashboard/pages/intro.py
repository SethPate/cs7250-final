from dash import dcc, html

explain = dcc.Markdown('''
    Transformers are cool and they are used in a lot of places.

    They can do this and that. Here are some famous transformers.

    They have cool results in log-linear charts.

    Here is what we are going to do -- we are going to classify movie
    reviews.
''')

def make_layout():
    return html.Div([
        explain,
    ])
