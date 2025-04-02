from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Users Service Base URL (running on Docker network)
USERS_SERVICE_URL = "http://pucapp_users:5000"

@app.route("/user/<string:user_id>", methods=["GET", "PUT", "DELETE"])
def proxy_user(user_id):
    """Proxy requests to Users Service"""
    url = f"{USERS_SERVICE_URL}/user/{user_id}"
    
    if request.method == "GET":
        response = requests.get(url)
    elif request.method == "PUT":
        response = requests.put(url, json=request.json)
    elif request.method == "DELETE":
        response = requests.delete(url)

    return jsonify(response.json()), response.status_code


@app.route("/user", methods=["GET", "POST"])
def proxy_users():
    """Proxy requests to Users Service"""
    url = f"{USERS_SERVICE_URL}/user"
    
    if request.method == "GET":
        response = requests.get(url)
    elif request.method == "POST":
        response = requests.post(url, json=request.json)

    return jsonify(response.json()), response.status_code


@app.route("/address/<int:address_id>", methods=["GET", "PUT", "DELETE"])
def proxy_address(address_id):
    """Proxy requests to Addresses in Users Service"""
    url = f"{USERS_SERVICE_URL}/address/{address_id}"
    
    if request.method == "GET":
        response = requests.get(url)
    elif request.method == "PUT":
        response = requests.put(url, json=request.json)
    elif request.method == "DELETE":
        response = requests.delete(url)

    return jsonify(response.json()), response.status_code


@app.route("/address", methods=["GET", "POST"])
def proxy_addresses():
    """Proxy requests to Addresses in Users Service"""
    url = f"{USERS_SERVICE_URL}/address"
    
    if request.method == "GET":
        response = requests.get(url)
    elif request.method == "POST":
        response = requests.post(url, json=request.json)

    return jsonify(response.json()), response.status_code


@app.route("/address/lookup/<string:zip_code>", methods=["GET"])
def proxy_address_lookup(zip_code):
    """Proxy request to address lookup"""
    url = f"{USERS_SERVICE_URL}/address/lookup/{zip_code}"
    response = requests.get(url)
    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
