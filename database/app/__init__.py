from flask import Flask
from database import db, migrate
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # SQLAlchemy configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/arb_calculator'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # database initialization
    db.init_app(app)
    migrate.init_app(app, db)

    # registering blueprints
    from .controllers.sport_controller import sport_blueprint
    app.register_blueprint(sport_blueprint)
    from .controllers.arb_opportunity_controller import arb_opportunity_blueprint
    app.register_blueprint(arb_opportunity_blueprint)

    # Swagger configuration
    from .swagger_config import swaggerui_blueprint, SWAGGER_URL
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
