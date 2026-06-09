import debug
import sqlite3

# make an arbitrary SQL query
def make_sql_query(cmd: str, params:tuple=(), path:str='RAP.db'):
        debug.log(f'SQL command: {cmd}')
        debug.log('Executing...')

        with sqlite3.connect(path) as conn:
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
                salt STRING,
                hashed_password STRING,
                access_level INTEGER
                )
        ''')

        debug.log('Finished login system initialisation.')


# delete database
def del_db(table_name: str):
        debug.log('Beginning database deletion...')

        make_sql_query(f'''
        DROP TABLE IF EXISTS {table_name}
        ''')

        debug.log('Finished database deletion.')
