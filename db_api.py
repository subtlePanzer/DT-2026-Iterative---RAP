import debug
from global_funcs import get_db_path
import sqlite3

# make an arbitrary SQL query
def make_sql_query(cmd: str, params:tuple=()):
        debug.log(f'SQL command: {cmd}')
        debug.log('Executing...')

        with sqlite3.connect(get_db_path()) as conn:
                cursor = conn.cursor()

                cursor.execute(cmd, params) # prevents SQL injection

                out = cursor.fetchall()
                conn.commit()
        debug.log('Finished.')

        return out

# initialise a fresh database
def init_db():
        debug.log('Beginning rap database initialisation...')

        make_sql_query('''
        CREATE TABLE IF NOT EXISTS rap (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        ''')

        debug.log('Finished rap database initialisation.')
        debug.log('Beginning login system initialisation...')

        make_sql_query('''
                CREATE TABLE IF NOT EXISTS login (
                        username STRING PRIMARY KEY,
                        id INTEGER,
                        salt STRING,
                        hashed_password STRING,
                        access_level INTEGER,
                        login_attempts INTEGER,
                        login_timeout INTEGER
                )
        ''')

        make_sql_query('''
        CREATE TRIGGER IF NOT EXISTS ts_auto_inc_non_pk
                AFTER INSERT ON login
                FOR EACH ROW
                WHEN NEW.id IS NULL
                BEGIN
                UPDATE login
                SET id = COALESCE((SELECT MAX(id) FROM login), 0) + 1
                WHERE username = NEW.username;
        END;
        ''')

        make_sql_query('''
                CREATE TABLE IF NOT EXISTS actions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name STRING,
                        description STRING
                )
        ''')

        make_sql_query('''
                CREATE TABLE IF NOT EXISTS deliverables (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name STRING,
                        description STRING,
                        assigned_id INTEGER,
                        start_date INTEGER,
                        due_date INTEGER,
                        action_id INTEGER
                )
        ''')

        make_sql_query('''
                CREATE TABLE IF NOT EXISTS comments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        author_id INTEGER,
                        preceding_id INTEGER,
                        deliverables_id INTEGER
                )
        ''') # singularly-linked list

        debug.log('Finished login system initialisation.')


# delete database
def del_db(table_name: str):
        debug.log('Beginning database deletion...')

        make_sql_query(f'''
        DROP TABLE IF EXISTS {table_name}
        ''')

        debug.log('Finished database deletion.')
