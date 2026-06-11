from pathlib import Path

DB_PATH = Path('RAP.db')

def get_db_path() -> str:
        return str(DB_PATH.absolute())

def set_db_path(path: str):
        global DB_PATH
        DB_PATH = Path(path)
