from flask import Blueprint, request, jsonify

from ..task.webhook_processing import process_webhook


webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.route('/parsehub-webhook', methods=['POST'])
def parsehub_webhook():
    form_data = request.form.to_dict()
    
    process_webhook.delay(form_data)
    
    return jsonify({"message": "Notification received and processed"}), 200
