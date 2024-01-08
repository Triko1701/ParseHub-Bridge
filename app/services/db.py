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





# import psycopg2
# from functools import wraps


# DB_IP = get_vm_metadata_field("db_ip")
# DB_USER = get_vm_metadata_field("db_user")
# DB_PASSWORD = get_vm_metadata_field("db_password")
# DB = get_vm_metadata_field("db")
# JOB_TABLE = get_vm_metadata_field("job_table")
# RUN_TABLE = get_vm_metadata_field("run_table")


# def db_connection(db: str=DB, user: str=DB_USER, password: str=DB_PASSWORD, host: str=DB_IP, port: int=5432):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             conn = psycopg2.connect(
#                 dbname=db,
#                 user=user,
#                 password=password,
#                 host=host,
#                 port=port
#             )
#             cur = conn.cursor()
            
#             # Pass the connection and cursor to the function
#             result = func(conn, cur, *args, **kwargs)
            
#             # Close cursor and connection
#             cur.close()
#             conn.close()
            
#             return result
#         return wrapper
#     return decorator


# @db_connection()
# def insert_data(conn, cur, data, table: str=JOB_TABLE):
#     for item in data:
#         columns = ', '.join(item.keys()) # columns
#         placeholders = ', '.join(['%s'] * len(item)) # placeholders
#         query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})" # query

#         cur.execute(query, list(item.values())) # execute query
#         conn.commit() # commit changes
#     pass


# @db_connection()
# def update_run(conn, cur, table, update_fields, conditions):

#     # Construct the dynamic part of the SQL query for updating fields
#     set_fields = ', '.join([f"{field} = '{value}'" for field, value in update_fields.items()])

#     # Construct the dynamic part of the SQL query for conditions
#     where_conditions = ' AND '.join([f"{field} = '{value}'" for field, value in conditions.items()])

#     # Construct the complete SQL query
#     update_query = f"""
#         UPDATE {table} 
#         SET {set_fields} 
#         WHERE {where_conditions}
#     """

#     # Execute the update query
#     cur.execute(update_query)

# @db_connection(db = "job", user = "postgres", password = "alex", host = "localhost")
# def get_db(conn, cur):
#     # Execute SQL query to list all databases
#     cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")

#     # Fetch all the rows
#     databases = cur.fetchall()

#     # Print the list of databases
#     for db in databases:
#         print(db[0])
