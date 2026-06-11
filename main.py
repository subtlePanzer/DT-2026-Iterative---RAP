from db_api import del_db, init_db, make_sql_query
import debug
from global_funcs import set_db_path
from host import launch
from login import create_new_user, create_new_admin, login_attempt
import sys

def print_help():
        print('''
        NAME: main.py

        SYNOPSIS: main.py [--options]

        DESCRIPTION: 
                Launch the reconcilliation action plan web app

        OPTIONS:
                --db-path <database> | -p <database>:
                        Use a specific database file address rather than the default.

                --del-db | -d:
                        Deletes the database file.

                --help | -h:
                        Prints help information.

                --reset-db | -r:
                        Clears the database by deleting and re-creating the file.

        EXIT STATUS:
                Standard UNIX exit codes.

        EXAMPLES:
                main.py --reset-db -db "C:/alternate_database_dir/database.db"
        ''')

# main execution pathway; launch the app
def main():
        # launch() 

        create_new_user('Alice', 'password')
        create_new_user('Bob69420', 's3cur3P4ssw0rd')
        create_new_admin('admin_charlie', '4iK^2K9A5hae$ka@1lg')
        create_new_user('Dina', 'password')

        print(f'Login attempt: Alice, PASSWORD: {login_attempt('Alice', 'PASSWORD')}')
        print(f'Login attempt: Alice, password: {login_attempt('Alice', 'password')}')
        print(f'Login attempt: admin_charlie, 4iK^2K9A5hae$ka@1lg: {login_attempt('admin_charlie', '4iK^2K9A5hae$ka@1lg')}')

# process console flags
args = sys.argv[1:]
if __name__ == '__main__': # todo: iterate over all args
        debug.init_debug()
        debug.log('Starting program...')

        do_reset_db, do_del_db = False, False
        db_path: str = ""

        if len(args) >= 1:
                match args[0]:
                        case '--reset-db':
                                do_reset_db = True
                        case '--del-db':
                                do_del_db = True
                        case '--help':
                                print_help()
                                sys.exit(0)
                        case '-h':
                                print_help()
                                sys.exit(0)
                        case '-p':
                                if len(args) >= 2:
                                        set_db_path(args[1].strip(' "\' \t\r\n')) # TODO: Check
                                else:
                                        print('-p: No file path provided.')
                                        sys.exit(1)
                        case '--db-path':
                                if len(args) >= 2:
                                        set_db_path(args[1].strip(' "\' \t\r\n')) # TODO: see above
                                else:
                                        print('--db-path: No file path provided.')
                                        sys.exit(1)

                        case _:
                                print('Wrong command-line options. Use \'python3 main.py --help\' for detailed usage instructions')
                                sys.exit(1)

        else:
                main()

        if do_reset_db:
                del_db('rap')
                del_db('login')
                init_db()

        if do_del_db:
                del_db()

        debug.log('Finished execution.')
