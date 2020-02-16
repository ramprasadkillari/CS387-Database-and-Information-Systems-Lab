from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec
import cgi
# nomnoml = require(‘nomnoml’)
page = """<!DOCTYPE html>
			<html>
			<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
			<head>
			<style>
			body {
			background-color: linen;
			margin: 10px; 
			}
			hr {
				display: block;
				width: 400px;
				margin-before: 0.5em;
				margin-after: 0.5em;
				margin-start: auto;
				margin-end: auto;
				overflow: hidden;
				border-style: inset;
				border-width: 1px;
			}

			.row {
			}

			.left {
			display: inline-block;
			text-align: right;
			width: 100px;
			padding: 10px;
			}


			.right {
			display: inline-block;
			padding: 10px;
			}

			</style>
			</head>
			<body>

			<form action="/add" method="post">
			<div>Tables:</div>
			<select name="table_select">
				{{table_dropdown_options}}
			</select>
			<input type="submit" value="Select table" >
			</form>
			<hr>
			{{insert_form}}
			<div class="error"></div>
			</body>
			</html>"""  

class PGMetaHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/meta":
			# TODO:  Same code as pyweb.py. Only page needs a change
			conn = dbexec.connect()
			meta = pgmeta.get_meta_data(conn)
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
		elif self.path == "/add":
			conn = dbexec.connect()
			meta = pgmeta.get_meta_data(conn)
			conn.close()
			table_options = ""
			for key in meta.tables:
				table_options += '<option value="{0}">{1}</option>\n'.format(key, key)
			page1 = page.replace("{{table_dropdown_options}}", table_options)
			page1 = page1.replace("{{insert_form}}", "")

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			print(page1)

			# output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'> "
			# output += "<input type='submit' value='Add Restaurant'>"
			# output += "</form></html></body>"
			self.wfile.write(page1.encode())

			# self.send_response(200)
			# self.send_header('Content-type','text/html')
			# self.end_headers()
			# self.wfile.write(src_code.format(graph_code).encode())

		# else:
		# 	if self.path == "/insert":

				# SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		try:
			if self.path == "/add":

				# print(self.rfile)
				print("hi 1")
				# console.log("hi")
				# ctype, pdict = cgi.parse_header(self.headers['content-type'])
				# print("hi 2")
				# pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
				# print("hi 3")
				# if ctype == 'multipart/form-data':
				# 	print("hi 4")

				form = cgi.FieldStorage(
					fp=self.rfile,
					headers=self.headers,
					environ={'REQUEST_METHOD': 'POST'}
				)
				print("test")
				print(form.keys())
				if("table_select" in form.keys()):
					# print("Entered 1")
					selected_table = form.getvalue("table_select")
					conn = dbexec.connect()
					meta = pgmeta.get_meta_data(conn)
					conn.close()

					table_options = ""
					for key in meta.tables:
						if key == selected_table:
							table_options += '<option value="{0}" selected>{1}</option>\n'.format(key, key)
						else:
							table_options += '<option value="{0}">{1}</option>\n'.format(key, key)
					page1 = page.replace("{{table_dropdown_options}}", table_options)
					table = meta.tables[selected_table]
					insert_form_html = '<form action="/add" method="post">\n   <div>{0}:</div>\n    <input type="hidden" name="table_name" value="{1}">\n'.format(table.name, table.name)
					for column in table.columns:
						insert_form_html += '<div class="row">\n    <div class="left">{0}</div>\n    <div class="right">\n      <input type="text" name="{1}">\n    </div>\n  </div>\n'.format(column.name, column.name)
					insert_form_html += '<div class="row">\n    <div class="left"></div>\n    <div class="right">\n      <input type="submit" value="Add">\n    </div>\n  </div>   </form>\n'
					page1 = page1.replace("{{insert_form}}", insert_form_html)

					# print(form.keys())
				else:
					# print(form.keys())
					# print("Len of form : ",len(form))
					# selected_table = form.getvalue("table_select")

					selected_table = form.getvalue('table_name')
					conn = dbexec.connect()
					meta = pgmeta.get_meta_data(conn) 
					conn.close()
					table_options = ""
					for key in meta.tables:
						if key == selected_table:
							table_options += '<option value="{0}" selected>{1}</option>\n'.format(key, key)
						else:
							table_options += '<option value="{0}">{1}</option>\n'.format(key, key)
					page1 = page.replace("{{table_dropdown_options}}", table_options)
					table = meta.tables[selected_table]
					l = form.keys()
					l.remove('table_name')
					conn = dbexec.connect()
					query = "insert into {0} ({1}) values ('{2}');".format(selected_table, ",".join(l), "','".join([form.getvalue(key) for key in l]))
					print(query)
					c = conn.cursor()
					try:
						c.execute(query)
						conn.commit()
						insert_form_html = '<form action="/add" method="post">\n   <div>{0}:</div>\n    <input type="hidden" name="table_name" value="{1}">\n'.format(table.name, table.name)
						for column in table.columns:
							insert_form_html += '<div class="row">\n    <div class="left">{0}</div>\n    <div class="right">\n      <input type="text" name="{1}">\n    </div>\n  </div>\n'.format(column.name, column.name)
						insert_form_html += '<div class="row">\n    <div class="left"></div>\n    <div class="right">\n      <input type="submit" value="Add">\n    </div>\n  </div>   </form>\n'
						page1 = page1.replace("{{insert_form}}", insert_form_html)
						
					except Exception as e:
						insert_form_html = '<form action="/add" method="post">\n   <div>{0}:</div>\n    <input type="hidden" name="table_name" value="{1}">\n'.format(table.name, table.name)
						for column in table.columns:
							insert_form_html += '<div class="row">\n    <div class="left">{0}</div>\n    <div class="right">\n      <input type="text" name="{1}" value="{2}">\n    </div>\n  </div>\n'.format(column.name, column.name, form.getvalue(column.name))
						insert_form_html += '<div class="row">\n    <div class="left"></div>\n    <div class="right">\n      <input type="submit" value="Add">\n    </div>\n  </div>   </form>\n'
						page1 = page1.replace("{{insert_form}}", insert_form_html)
						page1 = page1.replace('<div class="error"></div>', '<div class="error">{}</div>'.format("ERROR: "+str(e)))
						
					conn.close()


				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				# self.send_header('Location', '/restaurant')
				self.end_headers()
				self.wfile.write(page1.encode())
		except:
			print("Inside the exception block")
		# SimpleHTTPRequestHandler.do_GET(self)        

httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()
