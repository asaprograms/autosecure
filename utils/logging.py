# to log how long it takes to reach each milestone

import sys, datetime

def log(message: str):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {message}', file=sys.stderr, flush=True) 