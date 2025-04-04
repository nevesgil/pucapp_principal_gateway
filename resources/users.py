from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from flask import request
from resources.schemas.service_users_schemas import UserSchema, UserUpdateSchema
from datetime import date
import json
from resources.utils.constants import USERS_SERVICE_URL


blp = Blueprint("Users", __name__, description="Proxy operations for users")


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def forward_request(method, endpoint, json_data=None):
    """Forward a request to the Users Service and handle date serialization."""
    url = f"{USERS_SERVICE_URL}{endpoint}"

    try:
        response = requests.request(method, url, json=json_data, timeout=10)
        response.raise_for_status()

        return (
            json.loads(json.dumps(response.json(), cls=CustomJSONEncoder)),
            response.status_code,
        )

    except requests.RequestException as e:
        abort(500, message=f"Error forwarding request: {str(e)}")


@blp.route("/user/<string:user_id>")
class UserProxy(MethodView):
    @blp.response(200)
    def get(self, user_id):
        return forward_request("GET", f"/user/{user_id}")

    @blp.arguments(UserUpdateSchema)
    @blp.response(200)
    def put(self, user_data, user_id):
        return forward_request("PUT", f"/user/{user_id}", user_data)

    def delete(self, user_id):
        return forward_request("DELETE", f"/user/{user_id}")


@blp.route("/user")
class UserListProxy(MethodView):
    @blp.response(200)
    def get(self):
        return forward_request("GET", "/user")

    @blp.arguments(UserSchema)
    @blp.response(201)
    def post(self, user_data):
        user_data = request.get_json()
        return forward_request("POST", "/user", user_data)
