from psycopg2 import connect, extensions, Error
from psycopg2.extras import execute_values
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
import pytz

@dataclass
class ResultFilter:
    channel: str = None
    title: str = None
    pass



class PostgresqlClient:
    def __init__(self, password: str, user: str="postgres", db: str="postgres", tb: str=None, host: str="localhost"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.tb = tb
        
    def exec_query(self, query: str, db: str=None, params=None, insert_many: bool=False, ret: bool=False):
        if db is None:
            db = self.db
        conn = None
        cur = None
        try:
            # connect to the PostgreSQL server
            conn = connect(
                host=self.host,
                database=db,
                user=self.user,
                password=self.password
            )
            # conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            
            # execute the query
            if insert_many:
                execute_values(cur, query, params)
                return True
            else:
                if params is None:
                    cur.execute(query)
                else:
                    cur.execute(query, params)
            
            # Return result
            if ret == True:
                data = cur.fetchall()
                cols = [desc[0] for desc in cur.description]
                df = pd.DataFrame(data, columns=cols)
                return df
            else: 
                return True
            
        except (Exception, Error) as error:
            print("Error: ", error)
            return False
        finally:
            if cur is not None: cur.close()
            if conn is not None: conn.close()
    
    def list_db(self):
        dbs = self.exec_query("SELECT datname FROM pg_database;", db = "postgres", ret = True)
        print(dbs)
    
    def list_tb(self, db: str=None, show_backup: bool=False):
        if db is None: db = self.db
        tbs = self.exec_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';", db = db, ret = True)
        if show_backup == False:
            tbs = tbs[~tbs['table_name'].str.contains('backup')]
            tbs = tbs[~tbs['table_name'].str.contains('_bk')]
        print(tbs)
    
    def create_db(self, db: str=None):
        if db is None: db = self.db
        if self.exec_query(f"CREATE DATABASE {db};", db = "postgres"):
            print(f"Database {db} created successfully")
            
    def create_tb(self, cols: str="", db: str=None, tb: str=None, inherit: str=None):
        if db is None: db = self.db
        if tb is None: tb = self.tb
        if inherit:
            inherit = f" INHERITS ({inherit})"
        else:
            inherit = ""
        if self.exec_query(f"CREATE TABLE IF NOT EXISTS {tb} ({cols}){inherit};", db = db):
            print(f"Table {tb} created successfully")
        
    def insert_data(self, cols, vals, db: str=None, tb: str=None):
        if db is None: db = self.db
        if tb is None: tb = self.tb
        if self.exec_query(f"INSERT INTO {tb} ({cols}) VALUES ({vals});", db = db):
            print(f"Data inserted into {tb} successfully")
        
    def insert_data_many(self, cols: list[str], vals: list[tuple], db: str=None, tb: str=None):
        if db is None: db = self.db
        if tb is None: tb = self.tb
        if self.exec_query(f"INSERT INTO {tb} ({', '.join(cols)}) VALUES %s;", params = vals, db = db, insert_many = True):
            print(f"Data inserted into {tb} successfully")
            return True
        return False
            
    def delete_db(self, db: str=None):
        if db is None: db = self.db
        if self.exec_query(f"DROP DATABASE IF EXISTS {db};", db = "postgres"):
            print(f"Database {db} deleted successfully")
    
    def delete_tb(self, tb: str=None, db: str=None):
        if db is None: db = self.db
        if tb is None: tb = self.tb
        if self.exec_query(f"DROP TABLE IF EXISTS {tb};", db = db):
            print(f"Table {tb} deleted successfully")
    
    def query(self, query: str, params = None, db: str=None, ret: bool=True):
        if db is None: db = self.db
        return self.exec_query(query, params=params, db=db, ret=ret)

    # def execute_query(self, query, db = None, params = None, insert_many = False):
    #     if db is None: db = self.db
    #     try:
    #         with connect(
    #             host=self.host,
    #             db=db,
    #             user=self.user,
    #             password=self.password
    #         ) as conn:
    #             conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    #             with conn.cursor() as cur:
    #                 conn.set_session(autocommit=True)
    #                 if insert_many:
    #                     execute_values(cur, query, params)
    #                 if params is None:
    #                     cur.execute(query)
    #                 cur.execute(query, parameters=params)
    #                 return cur.fetchall()
    #     except (Exception, Error) as error:
    #         print("Error: ", error)
    #     finally:
    #         if cur is not None:
    #             cur.close()
    #         if conn is not None:
    #             conn.close()
    

def delete_duplicate(pg_client: PostgresqlClient, auto: bool = True):
    if auto == False:
        while True:
            input_delete_duplicate = input("Do you want to delete duplicated videos? (y/n)")
            if input_delete_duplicate.lower() == 'y':
                break
            elif input_delete_duplicate.lower() == 'n':
                return
            print("Invalid input. Please try again.")
    
    print("Deleting duplicated videos...")
    cmd_delete_duplicate = f"DELETE FROM {pg_client.tb} a USING {pg_client.tb} b WHERE a.ctid < b.ctid AND a.video_id = b.video_id;"
    pg_client.exec_query(cmd_delete_duplicate)
    
def create_backup_table(pg_client: PostgresqlClient, auto: bool = True):
    if auto == False:
        while True:
            input_create_backup = input("Do you want to create a backup table? (y/n)")
            if input_create_backup.lower() == 'y':
                break
            elif input_create_backup.lower() == 'n':
                return
            print("Invalid input. Please try again.")
        
    print("Creating backup table...")
    
    cmd_drop_backup_table = f"DROP TABLE IF EXISTS {pg_client.tb}_bk;"
    pg_client.exec_query(cmd_drop_backup_table)
    
    cmd_create_backup_table = f"CREATE TABLE {pg_client.tb}_bk AS TABLE {pg_client.tb};"
    pg_client.exec_query(cmd_create_backup_table)
    
def update_search_metadata(pg_client: PostgresqlClient, search_phrase: str, last_date: str, status: str):
    cmd_create_metadata_table = f"CREATE TABLE IF NOT EXISTS {pg_client.tb}_md (SEARCH_PHRASE CHAR(255), LAST_DATE TIMESTAMP, STATUS CHAR(50));"
    pg_client.exec_query(cmd_create_metadata_table)
    cmd_update = f"INSERT INTO {pg_client.tb}_md (SEARCH_PHRASE, LAST_DATE, STATUS) VALUES ('{search_phrase}', '{last_date}', '{status}');"
    pg_client.exec_query(cmd_update)
    
    # cmd_create_metadata_table = f"CREATE TABLE IF NOT EXISTS {pg_client.tb}_md (UPDATE_TIME TIMESTAMP, SEARCH_PHRASE CHAR(255), LAST_DATE CHAR(50), VIDEO_ENRICH BOOL, COMPLETE BOOL);"
    # pg_client.exec_query(cmd_create_metadata_table)
    # current_time = datetime.now(pytz.timezone('Australia/Sydney')).strftime("%Y-%m-%dT%H:%M:%SZ")
    # cmd_update = f"INSERT INTO {pg_client.tb}_md (UPDATE_TIME, SEARCH_PHRASE, LAST_DATE, VIDEO_ENRICH, COMPLETE) VALUES ({current_time}, {search_phrase}, '{last_date}', FALSE, FALSE);"
    # pg_client.exec_query(cmd_update)
    