from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from flask import request
from resources.service_shopping_schemas import CartSchema, CartUpdateSchema, CartItemSchema, CartItemAddSchema
import json
from datetime import date

SHOPPING_SERVICE_URL = "http://localhost:5002"

blp = Blueprint("Carts", __name__, description="Proxy operations for carts")


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date to string (YYYY-MM-DD)
        return super().default(obj)


def forward_request(method, endpoint, json_data=None):
    """Forward a request to the Shopping Service and handle serialization."""
    url = f"{SHOPPING_SERVICE_URL}{endpoint}"

    try:
        response = requests.request(method, url, json=json_data, timeout=10)
        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return "", 204
        
        return (
            json.loads(json.dumps(response.json(), cls=CustomJSONEncoder)),
            response.status_code,
        )
    except requests.RequestException as e:
        abort(500, message=f"Error forwarding request: {str(e)}")


@blp.route("/cart/<int:cart_id>")
class CartProxy(MethodView):
    @blp.response(200)
    def get(self, cart_id):
        return forward_request("GET", f"/cart/{cart_id}")

    @blp.arguments(CartUpdateSchema)
    @blp.response(200)
    def put(self, cart_data, cart_id):
        return forward_request("PUT", f"/cart/{cart_id}", cart_data)

    def delete(self, cart_id):
        return forward_request("DELETE", f"/cart/{cart_id}")


@blp.route("/cart")
class CartListProxy(MethodView):
    @blp.arguments(CartSchema(exclude=["items"]))
    @blp.response(201)
    def post(self, cart_data):
        return forward_request("POST", "/cart", cart_data)


@blp.route("/cart/<int:cart_id>/items")
class CartItemProxy(MethodView):
    @blp.arguments(CartItemAddSchema)
    @blp.response(201, CartItemSchema)
    def post(self, item_data, cart_id):
        return forward_request("POST", f"/cart/{cart_id}/items", item_data)


@blp.route("/cart/<int:cart_id>/items/<int:product_id>")
class CartItemManagerProxy(MethodView):
    def delete(self, cart_id, product_id):
        return forward_request("DELETE", f"/cart/{cart_id}/items/{product_id}")

    @blp.arguments(CartItemSchema(partial=True))
    @blp.response(200)
    def patch(self, item_data, cart_id, product_id):
        return forward_request("PATCH", f"/cart/{cart_id}/items/{product_id}", item_data)


@blp.route("/user/<int:user_id>/carts")
class UserCartsProxy(MethodView):
    @blp.response(200)
    def get(self, user_id):
        return forward_request("GET", f"/user/{user_id}/carts")