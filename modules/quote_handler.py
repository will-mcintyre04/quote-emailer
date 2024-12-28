import requests

class QuoteHandler():
    '''
    Handler that works with the api to fetch_quotes a motivational quote.

    Attributes
    ----------
    api_url : str
        url of the zenquotes api receiving quotes
    
    Methods
    -------
    fetch_quotes()
        makes a request to api, returns a list containing quotes and author strings
    '''

    def __init__ (self):
        self.api_url = "https://zenquotes.io/api/quotes"
    def fetch_quotes(self):
        '''
        Makes a request to the ZenQuotes API, returning a list of quotes with the following format:

        [{
            "quote": "quote_text",
            "author": "quote_author"
        }]

        If there are no quotes or an error occurs, returns an empty list.

        Returns
        -------
        list
            A list of dictionaries containing quote text and author name, or an empty list if no quotes are found or an error occurs.

        Exceptions
        ----------
        requests.exceptions.RequestException
            Raised if there is an error during the HTTP request (e.g., network issues, invalid URL, non-2xx status codes).
            
        KeyError
            Raised if the expected keys (`'q'` or `'a'`) are missing in the API response data.
        '''

        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raises an HTTPError if the status is 4xx or 5xx

            # Assuming the response is a list of quotes
            quotes = [
                {"quote": quote['q'], "author": quote['a']}
                for quote in response.json()
            ]
            return quotes

        except requests.exceptions.RequestException as e:
            # Handle any request-related exceptions (network issues, invalid URLs, etc.)
            print(f"Error fetch_quotesing data: {e}")
            return []

        except KeyError as e:
            # Handle missing keys in the response data
            print(f"Missing key in the response data: {e}")
            return []