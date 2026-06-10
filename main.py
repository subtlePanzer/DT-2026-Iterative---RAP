from db_api import del_db, init_db, make_sql_query
import debug
from login import create_new_user, create_new_admin, login_attempt
import sys

def print_help():
        print('''
        NAME: main.py

        SYNOPSIS: main.py [--options]

        DESCRIPTION: 
                TODO:

        OPTIONS:
                -db <database>:
                        Use a specific database file address rather than the default.

                --del-db:
                        Deletes the database file.

                --help:
                        Prints help information.

                --reset-db:
                        Clears the database by deleting and re-creating the file.

        EXIT STATUS:
                Standard UNIX exit codes.

        EXAMPLES:
                TODO:
        ''')

# main execution pathway; launch the app
def main():
        create_new_user('Alice', 'password')
        create_new_user('Bob69420', 's3cur3P4ssw0rd')
        create_new_admin('admin_charlie', '4iK^2K9A5hae$ka@1lg')

        print(f'Login attempt: Alice, PASSWORD: {login_attempt('Alice', 'PASSWORD')}')
        print(f'Login attempt: Alice, password: {login_attempt('Alice', 'password')}')
        print(f'Login attempt: admin_charlie, 4iK^2K9A5hae$ka@1lg: {login_attempt('admin_charlie', '4iK^2K9A5hae$ka@1lg')}')

# process console flags
args = sys.argv[1:]
if __name__ == '__main__': # todo: iterate over all args
        debug.init_debug()
        debug.log('Starting program...')
        if len(args) >= 1:
                match args[0]:
                        case '--reset-db':
                                del_db('rap')
                                del_db('login')
                                init_db()
                        case '--del-db':
                                del_db()
                        case '--help':
                                print_help()
                        case '-h':
                                print_help()
                        case _:
                                print('Wrong command-line options. Use \'python3 main.py --help\' for detailed usage instructions')
                                sys.exit(1)
        else:
                main()

        debug.log('Finished execution.')
