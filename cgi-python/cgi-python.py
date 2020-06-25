#!/usr/bin/env python3

import os
import re


default_name = 'NoName'


def get_name_from_query_string():
    try:
        query = os.environ['QUERY_STRING']
    except Exception:
        return default_name

    name = re.match(r'name=([^&]+)', query)

    if name:
        return name.group(1)

    return default_name


if __name__ == '__main__':
    name = get_name_from_query_string()

    response = f'''
<html>
    <head>
        <title>Hello Page</title>
    </head>
    <body>
        <h1>Hello, {name}</h1>
    </body>
</html>'''

    headers = f'''HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(response)}'''

    print(headers, end='\n\n')
    print(response)

