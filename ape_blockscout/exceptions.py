import os

from ape.exceptions import ApeException
from requests import Response

from ape_blockscout.utils import API_KEY_ENV_VAR_NAME


class ApeBlockscoutException(ApeException):
    """
    A base exception in the ape-blockscout plugin.
    """

class UnsupportedEcosystemError(ApeBlockscoutException):
    """
    Raised when there is no Blockscout buildout for ecosystem.
    """

    def __init__(self, ecosystem: str):
        super().__init__(f"Unsupported Ecosystem: {ecosystem}")


class BlockscoutResponseError(ApeBlockscoutException):
    """
    Raised when the response is not correct.
    """

    def __init__(self, response: Response, message: str):
        self.response = response
        super().__init__(f"Response indicated failure: {message}")


class BlockscoutTooManyRequestsError(BlockscoutResponseError):
    """
    Raised after being rate-limited by Blockscout.
    """

    def __init__(self, response: Response):
        message = "Blockscout API server rate limit exceeded."
        if not os.environ.get(API_KEY_ENV_VAR_NAME):
            message = f"{message}. Try setting environment variable '{API_KEY_ENV_VAR_NAME}'."

        super().__init__(response, message)


def get_request_error(response: Response) ->BlockscoutResponseError:
    response_data = response.json()
    if "result" in response_data and response_data["result"]:
        message = response_data["result"]
    elif "message" in response_data:
        message = response_data["message"]
    else:
        message = response.text

    if "max rate limit reached" in response.text.lower():
        return BlockscoutTooManyRequestsError(response)

    return BlockscoutResponseError(response, message)