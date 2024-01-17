from flask import Blueprint, request, jsonify, current_app as c_app

from ..utils import get_dict_field, get_current_time
from ..task import process_webhook
from ..models import Run


webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.route('/parsehub-webhook', methods=['POST'])
def parsehub_webhook() -> tuple:
    try:
        form_data = request.form.to_dict()
        
        kwargs = dict()
        arg_list = [Run.run_token.key, Run.status.key, Run.md5sum.key]
        for arg in arg_list:
            value = get_dict_field(form_data, arg)
            if not value:
                raise ValueError(f"Missing required argument: {arg}")
            kwargs[arg] = value
            
        kwargs["new_run"] = get_dict_field(form_data, "new_run")
        kwargs["created_at"] = get_current_time(c_app.config['DEFAULT_TIMEZONE']).strftime("%Y-%m-%d %H:%M:%S")
        
        process_webhook.delay(**kwargs)
        
    except Exception as e:
        c_app.logger.error(f"Error during processing webhook notification: {e}")
        
    return jsonify({"message": "Notification received and processed"}), 200
