import dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app
from utils.functions import matrix_fig
from utils.functions import update_fig


def get_layout():
    return html.Div(
        [
            html.H1("Decoder", id="decoder-section"),
            html.Hr(),
            dcc.Markdown(
                """
            Now that we have encoded the information from the sample,
            we have to **decode** it to answer our original question:
            was this a positive or negative movie review?

            In this simple **binary classification** task, we only need a linear
            transformation to determine a single number. That number
            represents the model's confidence that the sample is positive.

            Transformer models with more complicated tasks, like language modeling,
            have more complicated decoders.

            In this last layer, we multiply our most recent output of size **(T,d)**
            with a matrix of size **(d,1)**. This gives us a single number, displayed below:
        """
            ),
            html.Div(dcc.Graph(id="decoder")),
            dcc.Markdown(
                """
            That's the raw output of our model, which we call a **logit**.
            
            To turn it into a probability, we just pass it through the **sigmoid** function,
            which squashes all real numbers to a range of **(0,1)**.
            """
            ),
            html.Div(dcc.Graph(id="final")),
            dcc.Markdown(
                """
                Well done! You started with a bunch of words, and you
                wound up with a single number. That's how confident the model is
                that this review is positive (and, inversely, how confident the model is that
                it's negative).

                ## further reading

                We haven't covered quite everything here. There is still:
                * multi-head attention,
                * many layers of attention, and
                * more complex decoders (with cross attention!)

                But that's good enough for now. Enjoy a snack!
            """
            ),
        ]
    )


@app.callback(Output("decoder", "figure"), Input("datastore", "data"))
def update_decoder(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        labels = dict(color='value')
        fig = update_fig(params, "decoder", "decoder",labels=labels)
        fig.update_yaxes(showticklabels=False)
        return fig


@app.callback(Output("final", "figure"), Input("datastore", "data"))
def update_final(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        labels = dict(color='value')
        fig = update_fig(params, "final", "probability of positive review",labels=labels)
        fig.update_yaxes(showticklabels=False)
        return fig
