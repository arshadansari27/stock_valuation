from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from services import UserTransactionsListing
from repositories import RepositoryFactory


class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_error(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        print query, type(query)
        if 'user_id' not in query or len(query['user_id']) is 0:
            self._set_error(400)
            self.wfile.write("<html><body><h1>Invalid Parameter: "
                             "missing user_id</h1></body></html>")
            return
        try:
            user_id = int(query['user_id'][0])
            print("Getting transactions for user", user_id)
            string_values = UserTransactionsListing().handle(load_context(), 
                                                             user_id)
            response = '\n'.join(string_values)
            self._set_headers()
            self.wfile.write("<html><body><h1>User Listing!</h1>"
                             "<pre>{}</pre></body></html>".format(response))
        except Exception as e:
            self._set_error(500)
            self.wfile.write("<html><body><h1>Server Error: "
                             "{}</h1></body></html>".format(str(e)))


def load_context():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'db': 'stocks'
    }
    context = RepositoryFactory.factory(config, 'mysql')
    print("Using Context", config, context)
    return context


def run(server_class=HTTPServer, handler_class=MyHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
