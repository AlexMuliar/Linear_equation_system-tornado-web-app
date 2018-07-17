from tornado import httpserver, ioloop
from app import Application
import sys
import os

if __name__ == "__main__":
    os.system('cls')
    http_server = httpserver.HTTPServer(Application())
    try:
        port = int(sys.argv[1])
    except Exception:
        port = 8000

    http_server.listen(port, address='0.0.0.0')
    print(f'server listen on: localhost:{ port }')
    ioloop.IOLoop.instance().start()
