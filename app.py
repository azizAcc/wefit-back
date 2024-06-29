from api import create_app
from api.extensions import db
from flask_migrate import Migrate


def init_app():
    app = create_app()
    app.app_context().push()
    return app


api = init_app()
migrate = Migrate(api, db)

if __name__ == "__main__":
    api.run()
