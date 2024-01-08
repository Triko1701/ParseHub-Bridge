# from utils.vm_metadata_extraction import get_vm_metadata_field
from ..models.Run import Run
from ..models.Post import Post
from ..extensions import db
from utils.time import get_time


def insert_data(data):
    timestamp = get_time()
    for i in len(data["job_post"]):
        data["job_post"][i]["updated"] = timestamp # add timestamp
        data["job_post"][i]["employer_questions"] = data["job_post"][i]["employer_questions"].split("||") # Convert string to list of strings
    db.session.bulk_insert_mappings(Post, data["job_post"])
    db.session.commit()


def update_run(filters, updates):
    updates["updated"] = get_time() # add timestamp
    # Query to find the records based on multiple fields
    filter_args = {getattr(Run, field): value for field, value in filters.items()}
    query = Run.query.filter_by(**filter_args)

    # Fetch all matching records
    records_to_update = query.all()

    # Update the specified fields in all fetched records
    for record in records_to_update:
        for field, value in updates.items():
            setattr(record, field, value)

    # Commit changes to the database
    db.session.commit()

