import time
import requests

SESSION = requests.Session()
SESSION.max_redirects = 3
class Requester:
    def __init__(self, url, host=None, delay=0, headers=None, cookies=None, timeout=10, user_agent=None):
        self.url = url
        self.host = host
        self.headers = headers
        self.delay = delay
        self.cookies = cookies
        self.timeout = timeout
        self.user_agent = user_agent or "Custom user agent"

    def make_request(self, failed=None):
        if failed is None:
            failed = []
        final_headers = self.headers or {
            'Host': self.host,
            # Selecting a random user-agent
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        time.sleep(self.delay)

        try:
            response = SESSION.get(
                self.url,
                cookies=self.cookies,
                headers=final_headers,
                verify=False,
                timeout=self.timeout,
                stream=True,

            )
        except requests.exceptions.TooManyRedirects:
            return "dummy"
        except requests.exceptions.HTTPError:
            return "dummy"
        if 'text/html' in response.headers['content-type'] or \
                'text/plain' in response.headers['content-type']:
            if response.status_code != '404':
                return response.text
            else:
                response.close()
                failed.append(self.url)
                return 'dummy'
        else:
            response.close()
            failed.append(self.url)
            print(failed)
            return 'dummy'
