import requests, json, logging

class APIUtils:
    def __init__(self, session):
        self.session = session
    
    def get_request(self, **kwargs):
        return self._request('get', **kwargs)

    def post_request(self, **kwargs):
        return self._request('post', **kwargs)
    
    def delete_request(self, **kwargs):
        return self._request('delete', **kwargs)

    def _request(self, method, **kwargs):
        logging.info(f'Request method: {method}')
        logging.info(f'Request URL: {self.url}')
        
        json_body = kwargs.get("json", None)
        logging.info(f'Request Json body: {json.dumps(json_body, indent=4, ensure_ascii=False)}')
        logging.info(f'Request params: {self.session.params}')
        
        self.response = self.session.request(method, self.url, **kwargs)
        logging.info(f'Response headers: {self.response.headers}')
        logging.info(f'Response code: {self.response.status_code}')
        
        return self.response