from typing import Awaitable, Iterable, Optional, Sequence, Union

try:
    from aiosmtplib import SMTP
    from aiosmtplib.connection import DEFAULT_TIMEOUT
except ImportError:
    raise RuntimeError(
        "aiosmtplib is not installed. Please install it with `pip install aiosmtplib`"
    )

from ..utils import run_sync
from .message import Message


class EmailBackend:
    def __init__(
        self,
        *,
        hostname: Optional[str] = "localhost",
        port: Optional[int] = None,
        username: Optional[Union[str, bytes]] = None,
        password: Optional[Union[str, bytes]] = None,
        timeout: Optional[float] = DEFAULT_TIMEOUT,
        use_tls: bool = False,
        start_tls: bool = False,
        validate_certs: bool = True,
        client_cert: Optional[str] = None,
        client_key: Optional[str] = None,
        cert_bundle: Optional[str] = None,
        async_mode: bool = True,
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.use_tls = use_tls
        self.start_tls = start_tls
        self.validate_certs = validate_certs
        self.client_cert = client_cert
        self.client_key = client_key
        self.cert_bundle = cert_bundle
        self._client: Optional[SMTP] = None
        self._async_mode = async_mode

    @property
    def client(self) -> SMTP:
        if self._client is None:
            self._client = SMTP(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                use_tls=self.use_tls,
                start_tls=self.start_tls,
                validate_certs=self.validate_certs,
                client_cert=self.client_cert,
                client_key=self.client_key,
                cert_bundle=self.cert_bundle,
            )
        return self._client

    def send(
        self,
        message: Message,
        *,
        sender: Optional[str] = None,
        recipients: Optional[Union[str, Sequence[str]]] = None,
        mail_options: Optional[Iterable[str]] = None,
        rcpt_options: Optional[Iterable[str]] = None,
    ) -> Optional[Awaitable]:
        """
        Send an email message.
        If `_async_mode` is `True` the function will return a coroutine object.
        otherwise, it will send the message immediately.

        Note:
            if `async_mode` is `False`, you need to change the endpoint function to **sync** NOT **async**
        """
        assert isinstance(
            message, Message
        ), "Message must be an instance of popol.email.message.Message"
        msg = message.build()
        params = {
            "sender": sender,
            "recipients": recipients,
            "mail_options": mail_options,
            "rcpt_options": rcpt_options,
        }

        async def func():
            async with self.client:
                return await self.client.send_message(msg, **params)

        if self._async_mode:
            return func()

        return run_sync(func)
