import sqlite3

# make an arbitrary SQL query
def make_sql_query(cmd: str, path:str='RAP.db'):
        debug.log(f'SQL command: {cmd}')
        debug.log('Executing...')

        conn = sqlite3.connect(str)
        cursor = conn.cursor()

        cursor.execute(cmd)

        conn.commit()
        conn.close()

        debug.log('Finished.')

# initialise a fresh database
def init_db():
        debug.log('Beginning database initialisation...')

        make_sql_query('''
        CREATE TABLE IF NOT EXISTS rap (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        ''')

        debug.log('Finished database initialisation.')

# delete database
def del_db():
        debug.log('Beginning database deletion...')

        make_sql_query('''
        DROP TABLE IF EXISTS rap
        ''')

        debug.log('Finished database deletion.')
