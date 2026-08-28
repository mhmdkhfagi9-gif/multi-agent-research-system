"""
Generic API client tool. Fetches data from an external REST API.
Used by the API sub-agent inside retrieval_agent.py.
"""

import requests


def fetch_from_api(url: str, params: dict = None, timeout: int = 15) -> dict:
    """
    Calls a GET endpoint and returns parsed JSON.

    Never raises on network/HTTP errors -- returns a dict with an 'error' key
    instead, so calling agents can handle failure gracefully rather than
    crashing the whole pipeline over one bad request.
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
