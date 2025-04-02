from flask import Flask, redirect
from flask_smorest import Api
from flask_cors import CORS
from resources.users import blp as UsersBlueprint
from resources.addresses import blp as AddressesBlueprint


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
    # api.register_blueprint(AddressesBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)  # Running API Gateway on port 5000
