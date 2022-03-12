import os
from asyncio import iscoroutinefunction
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from mimetypes import guess_type
from typing import List, Optional, TextIO

from pydantic import EmailStr, validate_arguments

from ..utils import run_sync


class Message:
    @validate_arguments
    def __init__(
        self,
        *,
        from_email: str,
        subject: str,
        recipients: List[EmailStr],
        text: Optional[str] = None,
        html: Optional[str] = None,
        cc: List[EmailStr] = [],
        bcc: List[EmailStr] = [],
        reply_to: List[EmailStr] = [],
    ) -> None:
        self.subject = subject
        self.recipients = recipients
        self.text = text
        self.html = html
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to
        self.from_email = from_email
        self.id = make_msgid()
        self._message: MIMEMultipart = MIMEMultipart("alternative")

    def attach_file(
        self,
        file: TextIO,
        *,
        filename: str = None,
        mimetype: str = None,
        headers: dict = {},
    ) -> None:
        """Attach a file to the message.

        The file will be attached with the default MIME type application/octet-stream.
        """

        filename = filename or os.path.basename(file.name)
        mimetype = mimetype or guess_type(filename)[0] or "application/octet-stream"
        main_type, sub_type = mimetype.split("/", 1)
        part = MIMEBase(main_type, sub_type)
        if iscoroutinefunction(file.read):
            payload = run_sync(file.read)
        else:
            payload = file.read()
        part.set_payload(payload)
        encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=filename)
        for k, v in headers.items():
            part.add_header(k, v)
        self._message.attach(part)

    def build(self) -> MIMEMultipart:
        self._message["From"] = self.from_email
        self._message["Subject"] = self.subject
        self._message["To"] = ", ".join(self.recipients)

        if self.cc:
            self._message["Cc"] = ", ".join(self.cc)
        if self.bcc:
            self._message["Bcc"] = ", ".join(self.bcc)
        if self.reply_to:
            self._message["Reply-To"] = ", ".join(self.reply_to)
        if self.text:
            self._message.attach(MIMEText(self.text, "plain"))
        if self.html:
            self._message.attach(MIMEText(self.html, "html"))

        self._message["Message-ID"] = self.id
        self._message["Date"] = formatdate(localtime=True)
        return self._message
