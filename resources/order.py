from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas.service_shopping_schemas import OrderSchema, OrderUpdateSchema
from datetime import date
import json
import requests
from flask import request

from resources.utils.constants import SHOPPING_SERVICE_URL


blp = Blueprint("Orders", __name__, description="Proxy for order operations")


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
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


@blp.route("/order/<int:order_id>")
class OrderProxy(MethodView):
    @blp.response(200)
    def get(self, order_id):
        return forward_request("GET", f"/order/{order_id}")

    @blp.arguments(OrderUpdateSchema)
    @blp.response(200)
    def put(self, order_data, order_id):
        return forward_request("PUT", f"/order/{order_id}", order_data)

    @blp.response(204)
    def delete(self, order_id):
        return forward_request("DELETE", f"/order/{order_id}")


@blp.route("/order")
class OrderListProxy(MethodView):
    @blp.response(200)
    def get(self):
        return forward_request("GET", "/order")

    @blp.arguments(OrderSchema(exclude=["status", "payment_status"]))
    @blp.response(201)
    def post(self, order_data):
        return forward_request("POST", "/order", order_data)


@blp.route("/user/<int:user_id>/orders")
class UserOrdersProxy(MethodView):
    @blp.response(200)
    def get(self, user_id):
        return forward_request("GET", f"/user/{user_id}/orders")
