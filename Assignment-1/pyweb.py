from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec

page ="""
<html>
 <body>
  <pre>
{}
  </pre>
</body>
</html>
"""

class PGMetaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/meta":
            # TODO: Use pgmeta.to_graph() (in pgmeta.py) to get a nomnoml graph in string form.
            conn = dbexec.connect()
            meta = pgmeta.get_meta_data(conn) # returns dbmeta 'Meta'
            conn.close()
            graph_code = pgmeta.to_graph(meta)
            # TODO: Embed this string in the 'page' above.
             
            # TODO: Send this page using the following methods of BaseHTTPRequestHandler
            #       self.send_response, self.send_header, self.end_headers, self.wfile.write
            #       See: https://docs.python.org/2/library/basehttpserver.html
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(page.format(graph_code).encode())
        else:
            SimpleHTTPRequestHandler.do_GET(self)  # Fallback to built-in request handler

    def do_POST(self):
        SimpleHTTPRequestHandler.do_GET(self)        

httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()
