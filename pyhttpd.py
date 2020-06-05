from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json


class HandleThings(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'applicaiton/json')
        self.end_headers()

    def do_GET(self):
        print("GET request,\nPath: {}\nHeaders:\n{}\n".format(str(self.path), str(self.headers)))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("POST request,\nPath: {}\nHeaders:\n{}\n\nBody:\n{}\n".format((self.path), str(self.headers), post_data.decode('utf-8')))

        self._set_response()
        # self.wfile.write("POST request for ".format(self.path).encode('utf-8'))
        self.wfile.write("{}".format('{"errors":[{"type":"fatal","message":"oopsie poopsie","code":"500"}]}').encode('utf-8'))
        
httpd = HTTPServer(('0.0.0.0', 8089), HandleThings)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="privkey.pem", 
        certfile='fullchain.pem', server_side=True)

print('started')
httpd.serve_forever()

