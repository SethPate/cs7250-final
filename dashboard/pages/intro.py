import dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app


def make_layout(params):

    return html.Div(
        [
            #html.H1("Transformers and You"),
            #html.Hr(),
            dcc.Markdown(
                """
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
            """
            ),
            html.Div(
                html.Img(
                    src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgz-gW-L-HTRNa4FFX_HrnUnoQhXc2b7tjd-NFV_3KqG0n2pDrPzAhP-3Zx70jtygkDZV_VeE6u-XCjRWgY3ec_Ise8lK02iRuv6VzhJcayGnze6fv65oc3TgZ6JvfRso_xCW56-xI4xnScI0-oVsOu2kH3mBoU1CvtBVD99twdUtqsxyJj1DlAt3m1nQ/s1172/Screenshot%202022-04-01%205.25.47%20PM.png",
                    alt="log linear relationship graph",
                    style={"width": 500, "height": "auto"},
                ),
                style={"text-align": "center"},
            ),
            dcc.Markdown(
                """
                This implies that we haven't yet reached the technical limit of what Transformers can do for us.
                Sounds like something we should know about. Let's take a look at a toy Transformer!
            """
            ),
            html.H1("Sentiment Classification",id="task-section"),
            html.Hr(),
            dcc.Markdown("""
                We will build a network to predict whether a movie review is positive or negative.
                This is called **sentiment classification**, and it's a common NLP task.
                To train the network, we'll use the IMDB movie review [dataset](https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews).

                Although the dataset has 50k samples total, we'll only show two of them here:
            """),
            html.Div([
                html.Img(src="https://m.media-amazon.com/images/M/MV5BNGYyN2M0YmQtYWY5Ni00YjE4LWIzNDktMDJiMjgzZjg4OGNlXkEyXkFqcGdeQXVyMTQ3Njg3MQ@@._V1_.jpg",
                    alt="movie poster for across the moon",
                    style={'width':200, 'height':'auto'},
                    ),
                html.Img(src="https://upload.wikimedia.org/wikipedia/en/a/a6/The_Guardian_%282006_film%29_promotional_poster.jpg?20171215231323",
                    alt="movie poster for the guardian",
                    style={'width':200, 'height':'auto'},
                    ),
                ], style={'display':'flex',
                            'text-align':'center',
                            'justify-content':'space-evenly'}),
            dcc.Markdown("""
                Sample #1 was written from the seminal 1994 film *Across the Moon* starring Christina Applegate
                and another person. I am afraid that it is negative.
                Sample #2, on the other hand, is for the Kutcher/Costner pic *The Guardian*. Swoon! It's positive.

                ### your selected sample:
                """),
            html.Div(id="show-sample", className="sample-text"),
            dcc.Markdown("""
                The way we've built our Transformer, it'll take in this **sample text** and return a **single number**:
                a percentage representing its likelihood that the review is a positive one.
                In the next sections, we'll see how the network gets that number.
                """),
        ],
        id="home",
    )


@app.callback(Output("show-sample", "children"), Input("datastore", "data"))
def update_sample(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        ix = params["current_sample_ix"]
        sample = params["layerdata"][ix]["sample"]
        return html.P(" ".join(sample))
