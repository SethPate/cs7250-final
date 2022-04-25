from dash import dcc, html

explain = dcc.Markdown('''
    Transformers are cool and they are used in a lot of places.

    They can do this and that. Here are some famous transformers.

    They have cool results in log-linear charts.

    Here is what we are going to do -- we are going to classify movie
    reviews.

    This is the sample we have right now. You can change it if you want,
    and the rest of this page will update to show the new data.
''')

def make_layout(params):
    ix = params['current_sample_ix']
    sample = params['layerdata'][ix]['sample']

    return html.Div([
        explain,
        html.P(" ".join(sample)),
    ])
