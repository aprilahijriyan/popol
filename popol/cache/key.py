from hashlib import md5

from fastapi import FastAPI, Request

from popol.utils import get_settings


def get_cache_key(request: Request) -> str:
    path = request.url.path
    query_params = request.scope.get("query_string", b"").decode()
    part = path + query_params
    app: FastAPI = request.app
    settings = get_settings(app)
    if getattr(settings, "CACHE_INCLUDE_IP_ADDRESS", True):
        ip_address = request.client.host
        if ip_address:
            part += ip_address

    key = md5(part.encode()).hexdigest()
    return key
