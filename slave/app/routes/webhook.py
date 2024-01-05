from flask import Blueprint, request, jsonify
import json

from app.task.webhook_processing import process_webhook

webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.route('/parsehub-webhook', methods=['POST'])
def parsehub_webhook():
    process_webhook.delay(request)
    return jsonify({"message": "Notification received and processed"}), 200
