import requests
import json


class TolaApiConnection:
    """
    
    """
    endpoint = None
    token = None
    headers = None

    PROJECTAGREEMENTS = "api/projectagreements/"

    def __init__(self, endpoint, token):

        if endpoint[-1] is not '/':
            endpoint = endpoint + '/'

        self.endpoint = endpoint
        self.token = token
        self.headers = {
            'user-agent': 'TolaApiConnection',
            'Authorization': 'Token ' + token
        }
        # test connection
        try:
            self.get("api")
        except:
            raise Exception("Connection failed")

    def get(self, route):
        url = self.endpoint + route
        return self.request_get(url)

    def request_get(self, url):
        response = requests.get(url, headers=self.headers)
        content = response.content.decode('utf-8')

        if response.status_code != 200:
            raise Exception("Wrong status code (%d)" % response.status_code)

        try:
            results = json.loads(content)
        except:
            # Catch the cryptic parse error and throw our own exception if something goes wrong
            raise Exception("No valid JSON Response")

        return results

