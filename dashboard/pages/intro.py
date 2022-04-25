from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app


def make_dropdown(params):
    ix = params["current_sample_ix"]
    samples = [0, 1]
    sample_ids = [f"Sample {i+1}" for i in samples]
    return html.Div(
        [
            dcc.Dropdown(sample_ids, sample_ids[0], id="dropdown-samples"),
        ],
    )


def make_layout(params):

    return html.Div(
        [
            dcc.Markdown('''
            Transformer networks are the basic technology enabling modern
            large language models, including:
            * the [Google Pathways Language Model](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html), which explain bad jokes about TPU 'pods', and
            * [OpenAI's DALL-E 2](https://openai.com/blog/dall-e/), which uses Transformers to learn the relationship between text and images.

            Transformers are much more successful than the recurrent
            neural networks they replaced. For one, they are much easier 
            to train because they are highly parallelizable,
            enabling larger model size and dataset size.
            In Google's case, PaLM is 540bn parameters large -- the largest
            model yet -- but there is still a log-linear relationship
            between model size and performance at the margin.

            ![loglinear](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgz-gW-L-HTRNa4FFX_HrnUnoQhXc2b7tjd-NFV_3KqG0n2pDrPzAhP-3Zx70jtygkDZV_VeE6u-XCjRWgY3ec_Ise8lK02iRuv6VzhJcayGnze6fv65oc3TgZ6JvfRso_xCW56-xI4xnScI0-oVsOu2kH3mBoU1CvtBVD99twdUtqsxyJj1DlAt3m1nQ/s16000/Screenshot%202022-04-01%205.25.47%20PM.png)

            Put simply,

            '''),
            html.Div(id='show-sample'),
        ],
        id="home",
    )


@app.callback(Output("show-sample", "children"), Input("datastore", "data"))
def update_sample(params):
    if not params:
        return
    else:
        ix = params["current_sample_ix"]
        sample = params["layerdata"][ix]["sample"]
        return html.P(" ".join(sample))
