import re
from urllib.parse import unquote
 
def decode(text: str) -> str:
    decoded = unquote(text)
    return re.sub(r"\\u([0-9A-Fa-f]{4})", lambda m: chr(int(m.group(1), 16)), decoded) 