from db_api import make_sql_query
import debug
import hashlib
import secrets

BYTE_SIZE = 8

def create_new_user(username: str, password: str): # TODO passworsd char restrictions
        save_password(username, password, 0)

def create_new_admin(username: str, password: str): # Check is current user is an admin first
        save_password(username, password, 1)

def login_attempt(username: str, password: str) -> bool:
        debug.log(f'Login attempt: {username=}') # TODO limit attempts

        out = make_sql_query(f'''
                SELECT hashed_password, salt FROM login WHERE username = ? 
        ''', (username,))

        result = out[0]

        if not out[0]:
                debug.log(f'No username \'{username}\'.')
                return

        hashed_pword, salt = out[0][0], out[0][1]

        success =  match_hash(password, hashed_pword, salt) # was the login successful?
        if success:
                debug.log(f'Login successful.')
        else:
                debug.log(f'Incorrect password.')

        return success

def save_password(username: str, password: str, access_level = 0) -> bool:
        salt = get_salt()
        _hash = hash_password(password, salt)

        try:
                make_sql_query(f'''
                        INSERT INTO login (username, salt, hashed_password, access_level)
                        VALUES (?, ?, ?, ?);
                ''', (username, salt, _hash, access_level))
                return True
        except:
                debug.log(f'User {username} already exists')
                return False

def get_salt():
        SALT_BYTES = 32
        return secrets.token_hex(SALT_BYTES)

def hash_password(plaintext: str, salt: str) -> (str):
        plaintext += salt
        hashed_pword = hashlib.sha256(plaintext.encode()).hexdigest()
        return hashed_pword

def match_hash(plaintext: str, hashed: str, salt: str) -> bool:
        return hash_password(plaintext, salt) == hashed
