from flask import Flask, redirect
from flask_smorest import Api
from flask_cors import CORS
from resources.users import blp as UsersBlueprint
from resources.addresses import blp as AddressesBlueprint
from resources.products import blp as ProductsBlueprint
from resources.carts import blp as CartsBlueprint
from resources.order import blp as OrderBlueprint


def create_app():
    app = Flask(__name__)

    # Basic API configurations
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "API Gateway"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # Initialize API & CORS
    api = Api(app)
    CORS(app)

    # Redirecting the route for the Swagger docs
    @app.route("/")
    def home():
        return redirect("/docs")

    # Register the Blueprints
    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(AddressesBlueprint)
    api.register_blueprint(ProductsBlueprint)
    api.register_blueprint(CartsBlueprint)
    api.register_blueprint(OrderBlueprint)

    return app
