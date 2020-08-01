import argparse

import morepath
from dectate.tool import parse_app_class
from ekklesia_common.request import EkklesiaRequest
from webob.exc import HTTPException

from ekklesia_portal.app import make_wsgi_app


def why_tool():
    """
    Taken from more.whytool and adapted.

    Command-line query tool to see what code handles a request.
    """
    parser = argparse.ArgumentParser(description="Query Morepath paths")
    parser.add_argument('path', help="Path to request.")
    parser.add_argument('-r', '--request_method', default='GET', help='Request method such as GET, POST, PUT, DELETE.')
    parser.add_argument('-f', '--file', help='File with request body data.')
    parser.add_argument('-b', '--body', help='Request body data.')
    parser.add_argument('-H', '--header', help='Request header ("Foo-header: Blah")', action='append')

    args, filters = parser.parse_known_args()

    app = make_wsgi_app()

    if args.body is not None:
        body = args.body
    elif args.file is not None:
        with open(args.file, 'rb') as f:
            body = f.read()
    else:
        body = None
    if args.header:
        headers = {}
        for header in args.header:
            key, value = header.split(':', 1)
            headers[key] = value
    else:
        headers = None
    request = EkklesiaRequest.blank(args.path, method=args.request_method.upper(), headers=headers, body=body, app=app)
    response = app.publish(request)
    print("\n\n" + "=" * 80)
    print("\nPath:")
    if request.path_code_info is not None:
        print("   ", request.path_code_info.filelineno())
        print("   ", request.path_code_info.sourceline)
    else:
        print("   ", "No path matched")
    print("View:")
    print("   ", request.view_code_info.filelineno())
    print("   ", request.view_code_info.sourceline)
    if isinstance(response, HTTPException):
        print("HTTP Exception:", response.status)


if __name__ == '__main__':
    why_tool()
