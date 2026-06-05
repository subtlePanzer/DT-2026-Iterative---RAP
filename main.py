import sys

def reset_db():
        pass

def main():
        pass

args = sys.argv[1:]

if __name__ == '__main__':
        if len(args) >= 1:
                match args[0]:
                        case '--reset_db':
                                reset_db()
        else:
                main()

        return 0
