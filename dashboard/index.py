from app import app
from app import server
from environment.settings import APP_DEBUG
from environment.settings import APP_HOST
from environment.settings import APP_PORT
from environment.settings import DEV_TOOLS_PROPS_CHECK
from layout.sidebar.callbacks import *
from pages.explorer.callbacks import *
from routes import render_page_content

# from pages.gdp.gdp_callbacks import update_figure
# from pages.iris.iris_callbacks import make_graph


if __name__ == "__main__":
    app.run_server(
        host=str(APP_HOST),
        port=str(APP_PORT),
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK,
    )
