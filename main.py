from db_api import del_db, make_sql_query, reset_db
import debug
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
        pass

# process console flags
args = sys.argv[1:]
if __name__ == '__main__': # todo: iterate over all args
        debug.log('Starting program...')
        if len(args) >= 1:
                match args[0]:
                        case '--reset-db':
                                del_db()
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
