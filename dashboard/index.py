from app import app
from environment.settings import APP_DEBUG
from environment.settings import APP_HOST
from environment.settings import APP_PORT
from environment.settings import DEV_TOOLS_PROPS_CHECK
from routes import render_page_content

if __name__ == "__main__":
    app.run_server(
        host=str(APP_HOST),
        port=str(APP_PORT),
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK,
    )
