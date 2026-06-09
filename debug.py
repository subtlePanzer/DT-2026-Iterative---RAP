from os.path import isfile
import time

verbosity_level: int = 2
start_time: float
is_debug: bool = True
debug_path: str

def init_debug(debug_override:str=''):
        global start_time, debug_path
        start_time = time.time()

        i: int = 0

        if debug_override:
                debug_path = debug_override
        else:
                while 1:
                        debug_path = f'log{i}.debug'
                        if (isfile(debug_path)):
                                i += 1
                                continue
                        else:
                                break

        with open(debug_path, 'w') as f:
                f.write(f'Debug file initialised at {start_time}\n')

def log(msg: str):
        # verbosity 0 - nothing
        # verbosity 1 - log to file
        # verbosity 2 - log to terminal

        if not is_debug: return

        global start_time

        match verbosity_level:
                case 0:
                        return
                case 1:
                        log_to_file(msg)
                case 2:
                        log_to_file(msg)
                        print(f'TIME: {(time.time() - start_time):.2f} | {msg}')

                case _:
                        log_to_file
                        print(f'Internal error: incorrect value for \'verbosity_level\'; actual value {verbosity_level=}')

def log_to_file(msg: str):
        global start_time

        with open(debug_path, 'a') as f:
                f.write(f'TIME: {(time.time() - start_time):.2f} | {verbosity_level} | {msg}\n')
