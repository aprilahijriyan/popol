from fastapi import FastAPI
from pydantic import BaseSettings

from ..utils import get_settings, import_attr
from .backend import EmailBackend


def setup(app: FastAPI, settings: BaseSettings = None) -> EmailBackend:
    """
    Install the email plugin to the app.
    This will attach 1 attribute to `app.state` i.e:

    * `email` - `popol.email.backend.EmailBackend` instance object for sending email.

    Args:
        app: FastAPI app.
        settings: The settings (can be pydantic.BaseSettings).

    Returns:
        popol.email.backend.EmailBackend: The email backend.
    """

    settings = get_settings(app, settings)
    params = {}
    prefix = "EMAIL_"
    email_backend_setting = prefix + "BACKEND"
    for setting_name in dir(settings):
        if not setting_name.startswith(prefix) or setting_name == email_backend_setting:
            continue

        value = getattr(settings, setting_name)
        setting_name = setting_name[len(prefix) :].lower()
        params[setting_name] = value

    klass = getattr(settings, email_backend_setting)
    try:
        email_backend_class = import_attr(klass)
    except Exception as e:
        raise RuntimeError(f"Unable to import email backend {klass}") from e

    email_backend: EmailBackend = email_backend_class(**params)
    app.state.email = email_backend
    return email_backend
