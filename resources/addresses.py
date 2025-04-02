from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from flask import request
from resources.schemas import AddressSchema, AddressUpdateSchema
from datetime import date
import json

blp = Blueprint("Addresses", __name__, description="Operations on addresses")

USERS_SERVICE_URL = "http://localhost:5001"


def forward_request(method, endpoint, json_data=None):
    """Forward a request to the Users Service."""
    url = f"{USERS_SERVICE_URL}{endpoint}"

    try:
        response = requests.request(method, url, json=json_data, timeout=10)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.RequestException as e:
        abort(500, message=f"Error forwarding request: {str(e)}")


@blp.route("/address/<int:address_id>")
class Address(MethodView):
    def get(self, address_id):
        return forward_request("GET", f"/address/{address_id}")

    def delete(self, address_id):
        return forward_request("DELETE", f"/address/{address_id}")

    @blp.arguments(AddressUpdateSchema)
    def put(self, address_data, address_id):
        address_data = request.get_json()
        return forward_request("PUT", f"/address/{address_id}", address_data)


@blp.route("/address")
class AddressList(MethodView):
    def get(self):
        return forward_request("GET", "/address")

    @blp.response(201)
    @blp.arguments(AddressSchema)
    def post(self, user_data):
        user_data = request.get_json()
        return forward_request("POST", "/address", user_data)


@blp.route("/address/lookup/<string:zip_code>")
class AddressLookup(MethodView):
    def get(self, zip_code):
        return forward_request("GET", f"/address/lookup/{zip_code}")
