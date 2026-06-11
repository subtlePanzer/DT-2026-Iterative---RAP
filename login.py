from db_api import make_sql_query
import debug
import hashlib
import secrets
from time import time

BYTE_SIZE = 8

LOGIN_TIMEOUT_SEC = 300 #  5 min timeout 

def create_new_user(username: str, password: str) -> None: # TODO passworsd char restrictions
        save_password(username, password, 0)

def create_new_admin(username: str, password: str) -> None: # Check is current user is an admin first
        save_password(username, password, 1)

def login_attempt(username: str, password: str) -> bool:
        debug.log(f'Login attempt: {username=}')

        if not is_allowed_to_login(username):
                return False

        out = make_sql_query(f'''
                SELECT hashed_password, salt FROM login WHERE username = ? 
        ''', (username,))

        query_result = out[0]

        if not query_result:
                debug.log(f'No username \'{username}\'.')
                return

        hashed_pword, salt = query_result[0], query_result[1]

        success =  is_hash_match(password, hashed_pword, salt) # was the login successful?
        if success:
                debug.log(f'Login successful.')
        else:
                # increment login attempts
                make_sql_query(f'''
                UPDATE login SET login_attempts = login_attempts + 1, login_timeout = ? WHERE username = ?
                ''', (int(time()) + LOGIN_TIMEOUT_SEC, username))

                debug.log(f'Incorrect password.')

        return success

def check_timeout(username: str):
        pass

def is_allowed_to_login(username: str) -> bool:
        out = make_sql_query(f'''
                SELECT login_attempts, login_timeout FROM login WHERE username = ?
        ''', (username,))

        query_result = out[0]

        if not query_result:
                debug.log(f'User \'{username}\' not found.')
                return False

        if query_result[0] <= 3:
                return True

        if query_result[1] < time():
                make_sql_query(f'''
                        UPDATE login SET login_attempts = 0, login_timeout = 0 WHERE username = ?
                ''', (username,))
                return True

        debug.log(f'Too many failed login attempts for \'{username}\'')
        return False

def save_password(username: str, password: str, access_level = 0) -> bool:
        salt = get_salt()
        _hash = hash_password(password, salt)

        try:
                make_sql_query(f'''
                        INSERT INTO login (username, salt, hashed_password, access_level, login_attempts, login_timeout) 
                        VALUES (?, ?, ?, ?, 0, 0);
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

def is_hash_match(plaintext: str, hashed: str, salt: str) -> bool:
        return hash_password(plaintext, salt) == hashed
