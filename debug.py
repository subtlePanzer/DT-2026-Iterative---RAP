import time

verbosity_level = 0

def log(msg: str):
        if verbosity_level >= 2:
                print(f'TIME: {round(time.time(), 2)} | {msg}')

        # verbosity 0 - nothing
        # verbosity 1 - log to file
        # verbosity 2 - log to terminal
