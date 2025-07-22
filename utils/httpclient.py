from requests import Session

# mimic a real browser with these agent tags
class HttpClient:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"

    def __init__(self, headers=None, proxies=None, timeout=30, verify_ssl=True):
        self._session = Session()
        base_headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        if headers:
            base_headers.update(headers)
        self._session.headers.update(base_headers)
        if proxies:
            self._session.proxies.update(proxies)
        self._timeout = timeout
        self._verify_ssl = verify_ssl

    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self._timeout)
        kwargs.setdefault("verify", self._verify_ssl)
        resp = self._session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def patch(self, url, **kwargs):
        return self.request("PATCH", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def close(self):
        self._session.close()

    @property
    def cookies(self):
        return self._session.cookies

    def set_cookie(self, key: str, value: str):
        self._session.cookies.set(key, value) 