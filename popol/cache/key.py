from hashlib import md5

from fastapi import FastAPI, Request

from popol.utils import get_settings


def get_cache_key(request: Request) -> str:
    """
    Generate cache keys using the concatenation of route paths, HTTP methods and query params.
    And also available `CACHE_INCLUDE_IP_ADDRESS` configuration to insert client ip address to key.

    Returns:
        str: The cache key (md5 hash).
    """

    path = request.url.path
    query_params = request.scope.get("query_string", b"").decode()
    part = path + request.method + query_params
    app: FastAPI = request.app
    settings = get_settings(app)
    if getattr(settings, "CACHE_INCLUDE_IP_ADDRESS", True):
        ip_address = request.client.host
        if ip_address:
            part += ip_address

    key = md5(part.encode()).hexdigest()
    return key
