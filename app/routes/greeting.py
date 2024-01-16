from flask import Blueprint, request, jsonify, current_app as c_app


greeting_blueprint = Blueprint('greeting', __name__)

@greeting_blueprint.route('/')
def parsehub_webhook() -> tuple:
    return jsonify({"message": "Hello world!"}), 200
