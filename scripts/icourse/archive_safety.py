"""Offline helpers for archiving course metadata without session/signature values.

These helpers do not authenticate or fetch anything. They do not clean Git history.
"""
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import re

SENSITIVE_QUERY_KEYS = frozenset({
    'signature', 'x-nos-signature', 'nosaccesskeyid', 'accesskeyid',
    'token', 'access_token', 'csrfkey', 'sessionid', 'httpsessionid',
    'x-amz-signature', 'x-amz-credential', 'x-amz-security-token',
})
BODY_KEYS = frozenset({'body', 'req_body', 'resp_text', 'headers', 'cookies'})
URL_PATTERN = re.compile(r'https?://[^\s<>"\'\\]+')


def archive_url(url):
    """Remove authentication/signature query fields while retaining source identity."""
    try:
        parts = urlsplit(url)
        if parts.scheme not in ('http', 'https'):
            return url
        pairs = parse_qsl(parts.query, keep_blank_values=True)
        if '@' not in parts.netloc and not any(k.lower() in SENSITIVE_QUERY_KEYS for k, _ in pairs):
            return url  # Do not normalize unrelated historical evidence.
        pairs = [(k, v) for k, v in pairs if k.lower() not in SENSITIVE_QUERY_KEYS]
        # Signed URLs with credentials in userinfo must not be archived either.
        host = parts.netloc.rsplit('@', 1)[-1]
        return urlunsplit((parts.scheme, host, parts.path, urlencode(pairs), ''))
    except ValueError:
        return '[invalid URL omitted]'


def archive_text(text):
    return URL_PATTERN.sub(lambda m: archive_url(m.group(0)), text)


def safe_record(value):
    """Do not retain opaque request/response bodies in browser debugging logs."""
    if isinstance(value, dict):
        return {k: safe_record(v) for k, v in value.items()
                if k.lower() not in BODY_KEYS}
    if isinstance(value, list):
        return [safe_record(v) for v in value]
    if isinstance(value, tuple):
        return tuple(safe_record(v) for v in value)
    if isinstance(value, str):
        return archive_text(value)
    return value
