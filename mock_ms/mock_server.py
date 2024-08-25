from flask import Flask, jsonify, request
from faker import Faker
import random
from datetime import datetime, timedelta

app = Flask(__name__)
faker = Faker()


# Helper function to generate random product data
def generate_product(user_id):
    product_types = [
        "mobile",
        "landline",
        "internet",
        "iptv",
        "bundle",
        "value_added_service",
    ]
    status_types = ["active", "activating", "suspended", "cancelled"]
    subscription_types = ["prepaid", "postpaid", "control"]

    return {
        "id": user_id,
        "product_name": faker.word(),
        "product_type": random.choice(product_types),
        "status": random.choice(status_types),
        "start_date": faker.date_time_this_decade().isoformat(),
        "subscription_type": random.choice(subscription_types),
        "identifiers": [faker.phone_number()],
        "descriptions": [{"text": faker.sentence()}],
        "sub_products": (
            [generate_product(user_id)] if random.choice([True, False]) else []
        ),
    }


@app.route("/users/<string:user_id>/products", methods=["GET"])
def list_user_products(user_id):
    # Simulate different responses based on query parameters or random
    if "status" in request.args and request.args["status"] not in [
        "active",
        "activating",
        "suspended",
        "cancelled",
    ]:
        return (
            jsonify(
                {
                    "code": "INVALID_ARGUMENT",
                    "message": "Client specified an invalid argument, request body or query param",
                }
            ),
            400,
        )

    return jsonify([generate_product(user_id), generate_product(user_id)])


# Error responses
@app.errorhandler(404)
def not_found(e):
    return (
        jsonify({"code": "NOT_FOUND", "message": "A specified resource is not found"}),
        404,
    )


@app.errorhandler(403)
def forbidden(e):
    return (
        jsonify(
            {
                "code": "PERMISSION_DENIED",
                "message": "Authenticated user has no permission to access the requested resource",
            }
        ),
        403,
    )


@app.errorhandler(504)
def timeout(e):
    return (
        jsonify(
            {"code": "TIMEOUT", "message": "Request timeout exceeded. Try it later"}
        ),
        504,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5100)
