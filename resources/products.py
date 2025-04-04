import requests
from flask import Response, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
import json
from datetime import date

SHOPPING_SERVICE_URL = "http://localhost:5002"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def forward_request(method, endpoint, json_data=None):
    """Forward a request to the Users Service and handle date serialization."""
    url = f"{SHOPPING_SERVICE_URL}{endpoint}"

    try:
        response = requests.request(method, url, json=json_data, timeout=10)
        response.raise_for_status()

        return (
            json.loads(json.dumps(response.json(), cls=CustomJSONEncoder)),
            response.status_code,
        )

    except requests.RequestException as e:
        abort(500, message=f"Error forwarding request: {str(e)}")


blp = Blueprint("Products", __name__, description="Proxy for product operations")


@blp.route("/products")
class ProductListProxy(MethodView):
    def get(self):
        """Forward request to shopping service to fetch all products"""
        return forward_request("GET", "/products")
