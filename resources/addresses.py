import requests
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask import request

blp = Blueprint("Addresses", __name__, description="Operations on addresses")

# Users Service Base URL (running on Docker)
USERS_SERVICE_URL = "localhost:5001"

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

    def put(self, address_id):
        return forward_request("PUT", f"/address/{address_id}", request.json)


@blp.route("/address")
class AddressList(MethodView):
    def get(self):
        return forward_request("GET", "/address")

    def post(self):
        return forward_request("POST", "/address", request.json)


@blp.route("/address/lookup/<string:zip_code>")
class AddressLookup(MethodView):
    def get(self, zip_code):
        return forward_request("GET", f"/address/lookup/{zip_code}")
