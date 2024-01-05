from flask import Blueprint, request, jsonify

from app import db
from app.models.parsehub_data import Run
from sqlalchemy.sql import func

run_blueprint = Blueprint('run', __name__)

@run_blueprint.route('/trigger-run', methods=['POST'])
def trigger_run():
    # Parse API key and project token from request
    api_key = request.json.get('api_key')
    project_token = request.json.get('project_token')

    # Logic to trigger ParseHub run using API key and project token
    # ...

    # Return response from ParseHub to the client
    test_run = Run(slave = "slave", project_token = "project_token", run_token = "run_token", status = "status", md5sum = "md5sum", start_url = "start_url")
    
    # Add the new user to the session
    db.session.add(test_run)

    # Commit the session to insert the new user into the database
    db.session.commit()
    
    random_run = Run.query.order_by(func.random()).first()

    
    return jsonify({"message": "Run triggered successfully", "random title": random_run.status}), 200
