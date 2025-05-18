import requests
from loguru import logger


def catch_request_exception(func):
    """
    Decorator returns the response if the request has been made, in case of exception - None
    """
    def wrapper(*args):
        response = None
        try:
            response = func(*args)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None
    return wrapper
