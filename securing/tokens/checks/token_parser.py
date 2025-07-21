import re

TOKEN_RE = re.compile(r'<input\s+type=["\"]hidden["\"]\s+name=["\"]t["\"]\s+id=["\"]t["\"]\s+value=["\"]([^"\']+)["\"]')
 
def token_parser(html: str):
    m = TOKEN_RE.search(html)
    return m.group(1) if m else None 