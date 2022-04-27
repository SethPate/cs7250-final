from dash import html, dcc

layout = html.Div([
    dcc.Markdown(
    """
    # About Pretty Transformers

    This is a class project for cs7250 at Northeastern University.

    ## Demo
    """),
    html.Div(
    html.Iframe(width="560", height="315", src="https://www.youtube.com/embed/yRaJM0QmTjk", title="YouTube video player", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"),
        style={"text-align":"center"}),
    dcc.Markdown(
    """

    ## Motivation

    All of us on the team have used transformer networks,
    but didn't feel like we quite understood them. As those models have
    become quite popular (and successful), we wanted a tool to teach us
    how they work. We still don't *really* understand how they work,
    but at least we know more than we did -- and now you do, too!

    ## Data

    All of the data on this site is currently synthetic, mimicking the throughput
    of an actual transformer. The script to generate the data is located at
    [https://github.com/SethPate/cs7250-final/blob/master/data/make_fake_data.py]
    (https://github.com/SethPate/cs7250-final/blob/master/data/make_fake_data.py).

    Of course, this is not ideal! Hopefully we'll get our transformer working soon. When we do, it will contain
    about 10^6 parameters. The training data for this transformer is the IMDB
    dataset: [https://ai.stanford.edu/~amaas/data/sentiment/](https://ai.stanford.edu/~amaas/data/sentiment/).
    The samples you see on this site were taken from that dataset.

    ## Task Analysis

    We worked with a few colleagues, and drew from our own experience, to develop
    this list of tasks:

    * understand positional encoding,
    * interrogate the attention mechanism, and
    * generally understand the embedding process and the flow of data through the network

    We classified these using Brehmer and Munzner's typology; a detailed table
    is in our submitted paper.

    ## Design Process

    We initially designed this as a python extension for use by engineers, in order
    to understand their code better and investigate failure cases.

    After a few attempts and iterations of feedback with our audience,
    we decided to make a simpler introduction to how transformers work,
    aimed at people learning about these for the first time.

    ## Final Visualization

    We wrote this site using `dash` and `plotly`, with hosting through Heroku.

    The layout is a simple, single page with sidebar navigation to important
    bookmarks. As the user scrolls down, they follow a data sample as it is
    embedded, encoded with position data, run through network layers,
    and finally transformed into a single prediction value.

    The matrices are visualized using `imshow`. Hopefully this provides the user
    with a simple and intuitive understanding of how data is understood by neural
    networks. The color ramp, `viridis plasma`, is perceptually uniform, colorbind safe,
    and quite pretty -- so, Pretty Transformers.

    The attention visualization is the most involved. We used a graph viz package
    called `cytoscape`. Mouseover effects turned out to be pretty challenging,
    but the user can select different words to see the attention interaction.

    ## Data Analysis

    We were struck by how clearly the positional encoding affected the input embeddings.
    This is a unique part of transformers that can be hard to understand 
    until you see it visualized, when it becomes quite clear.

    Similarly, attention is defined with equations, but more easily understood when depicted.

    ## Conclusion

    This is a decent start. There's much more to transformers than is depicted here.
    Further topics could include:

    * multi head attention
    * cross attention
    * more complex decoder networks
    * some discussion of popular transformers like GPT

    We hope you enjoyed our work. Enjoyment, after all, is one of the purposes 
    of visualization, according to Brehmer and Munzner...

    """)
    ])
