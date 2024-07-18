"""

"""

import typing_extensions as typing

class Email(typing.TypedDict):
    email_id: str
    sender: str
    recipient: str
    subject: str
    content: str

class Emails(typing.TypedDict):
    emails: typing.List[Email]

class EmailIds(typing.TypedDict):
    email_id: str