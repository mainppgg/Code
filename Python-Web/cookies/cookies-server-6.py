#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Simple HTTP Server
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# January 2019
#
# Important: Run with Python 3.6 or higher
#
# Server sending a cookie when the content of the text form
# is received, and showing in the screen the text in the
# cookie (if any).

import argparse
import http.server
import http.cookies
import socketserver
import urllib

PORT = 1234

PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Hello!</p>
    <form action="/" method="GET">
      Say something: <input name="something" type="text" />
    <input type="submit" value="Submit" />
    <p>{}</p> 
    <p>{}</p>
    </form>
  </body>
</html>
"""

def parse_args ():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('-p', '--port', type=int, default=PORT,
                        help="TCP port for the server")
    args = parser.parse_args()
    return args

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        print("Received: GET " + self.path)
        parsed_resource = urllib.parse.urlparse(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")

        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))

        in_cookie = ""
        if 'yousaid' in cookies:
            in_cookie = "In cookie: " + cookies['yousaid'].value

        you_said = ""
        if parsed_resource.query:
            qs = urllib.parse.parse_qs(parsed_resource.query)
            if 'something' in qs:
                you_said = "You said: " + qs['something'][0]
                cookie = http.cookies.SimpleCookie()
                cookie['yousaid'] = qs['something'][0]
                self.send_header("Set-Cookie", cookie.output(header='', sep=''))

        self.end_headers()
        self.wfile.write(bytes(PAGE.format(you_said, in_cookie), 'utf-8'))

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()
