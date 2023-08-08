import requests

class Quote():
    '''
    Handler that works with the api to fetch a motivational quote.
    '''
    def __init__ (self):
        self.api_url = "https://zenquotes.io/api/random"
    def fetch(self):
        '''
        Makes a request to the zenquotes api, returning a list with the following format:

        ["quote_text", "author_name"]
        '''
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            if data and len(data) > 0:
                quote_text = data[0]['q']
                author_name = data[0]['a']
                return quote_text, author_name
        except requests.exceptions.RequestException as e:
            print(f"Error when fetching quotes: {e}")
        return None, None