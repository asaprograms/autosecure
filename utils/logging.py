import sys, datetime

def log(message: str):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {message}', file=sys.stderr, flush=True) 