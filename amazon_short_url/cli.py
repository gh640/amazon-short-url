import re
from urllib.parse import urlsplit, urlunsplit

import click


@click.command()
@click.argument('url')
def main(url: str):
    clean_url = shortener(url)
    print(clean_url)


def shortener(url: str) -> str:
    parsed = urlsplit(url)

    if not is_valid_scheme(parsed.scheme):
        raise ValueError(f'Invalid scheme: {parsed.scheme}')
    if not is_valid_netloc(parsed.netloc):
        raise ValueError(f'Invalid netloc: {parsed.netloc}')

    raw_path = parsed.path
    match = re.search(r'/dp/[A-Z0-9]+', raw_path)
    if match is None:
        raise ValueError(f'Invalid path: {raw_path}')

    clean_path = match.group(0)
    return urlunsplit((parsed.scheme, parsed.netloc, clean_path, '', ''))


def is_valid_scheme(scheme: str) -> bool:
    return scheme == 'https'


def is_valid_netloc(netloc: str) -> bool:
    return re.match(r'www\.amazon\.co(m|\.[a-z]+)', netloc) != None
