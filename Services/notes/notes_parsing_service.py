import base64
import binascii

from bs4 import BeautifulSoup
from fastapi import HTTPException
from icecream import ic

from error_constants import BadRequest


def html_to_text(data):
    soup = BeautifulSoup(data, features="html5lib")
    return soup.get_text(strip=True, separator=" ")


def b64_to_html(html):
    try:
        binary_html = base64.b64decode(html)
        html = binary_html.decode('utf8')
        print(len(html))
        return html
    except (binascii.Error, UnicodeDecodeError, Exception) as e:
        ic()
        ic(e)
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )