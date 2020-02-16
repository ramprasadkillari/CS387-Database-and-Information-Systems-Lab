from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec
# nomnoml = require(‘nomnoml’)
# page ="""
# <html>
#  <body>
# {}
#  </body>
# </html>
# """

class PGMetaHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/meta":
			# TODO:  Same code as pyweb.py. Only page needs a change
			conn = dbexec.connect()
			meta = pgmeta.get_meta_data(conn) # returns dbmeta 'Meta'
			conn.close()
			graph_code = pgmeta.to_graph(meta)

			src_code = """
			<html>
 			<body>
 			<script src="view/dist/main.js"></script>
			<canvas id='target-canvas'></canvas>
			<script>
				var canvas = document.getElementById('target-canvas');
				var source = `{}`;
				nomnoml.draw(canvas, source);
			</script>
			</body>
			</html>
			"""
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(src_code.format(graph_code).encode())
			# self.wfile.write(src_code.format(graph_code).encode())
			# self.wfile.write(page.src_code.format(graph_code).encode())
		else:
			SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		SimpleHTTPRequestHandler.do_GET(self)        

httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()
