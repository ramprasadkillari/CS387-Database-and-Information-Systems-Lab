from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
sys.excepthook = sys.__excepthook__
import psycopg2
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import redirect
from CS387_ass2.settings import DATABASES as config
conn_str = "host="+config['default']['HOST']+" port="+config['default']['PORT']+" dbname="+config['default']['NAME']

fail = """<body><h1> Sorry Unable to Login, Retry</h1></body>"""
fail1 = """<body><p> <font color ="red">values should be non-negative</font><p></body>"""
fail2 = """<body><p> <font color ="red">values shouldnot be a string or empty</font><p></body>"""
success = """<body><p> <font color ="green">Success</font><p></body>"""
details = """    <head>
					 <style>
					 table {
					 font-family: arial, sans-serif;
					 width: 100%;
					 }

					 td, th {
					 border: 1px solid #dddddd;
					 height= 34px;
					 text-align: left;
					 padding: 8px;
					 }

					tr:nth-child(even) {
					background-color: #dddddd;
					}
					</style>
					</head> 
					<title> Order Page </title>
					<body>
					<table>"""
html = """<html><head><title>Login Page</title></head>
	<body>
	<form name="loginForm" method="post">
	<table width="20%" bgcolor="0099CC" align="center">
	<tr>
	<td colspan=2><center><font size=4><b>HTML Login Page</b></font></center></td>
	</tr>
	<tr>
	<td>Username:</td>
	<td><input type="text" size=25 name="userid"></td>
	</tr>
	<tr>
	<td>Password:</td>
	<td><input type="Password" size=25 name="pwd"></td>
	</tr>
	<tr>
	<td><input type="submit" value="Login"></td>
	</tr>
	</table>
	</form></body></html>"""


html1 = """
			</table><br><br><br>
					<h style="text-align:center"><font color ="red"> Order</font></h>
					<div>
					<form name="Order" method="post">
					<table width="250" border="1" bgcolor="#ADD8E6" >

					<tr>

					<th height="34">Samosa:</th>

					<td><input  name="samosa"  /></td>

					</tr>

					<tr>

					<th height="33">Idli</th>

					<td><input  name= "idli" /></td>

					</tr>
					<tr>

					<th height="33">Chai</th>

					<td><input  name = "chai" /></td>

					</tr>

					<tr>

					<th height="39" colspan="2"><input type="submit" value="Order"/>

					</th>

					</tr>

					</table>
					</form>
					</div>
					</body> 
		  """


@csrf_exempt
def Login(request):
	if request.method == 'GET':
		return HttpResponse(html)
	if request.method == 'POST':
		user_id = request.POST["userid"]
		passwd  = request.POST["pwd"]

		conn = psycopg2.connect(conn_str)
		query = "select loginname from addausers where loginName = " + "'"+ user_id + "'" +" and password = " + "'"+passwd+ "';"
		a, b = exec_query(conn,query)
		request.session['username'] = user_id
		request.session['passwd'] = passwd
		if b!=[]:
			return redirect('/orders')
		else:
			return HttpResponse(html+fail)

def exec_query(conn, sql):
	"""Execute sql query. Return header and rows"""
	#TODO: create cursor, get header from cursor.description, and execute query to fetch rows.
	cursor = conn.cursor()
	cursor.execute(sql)
	header = [desc[0] for desc in cursor.description]
	rows = cursor.fetchall()
	conn.commit()
	cursor.close()
	return (header, rows)

@csrf_exempt
def user_direct(request):
	if request.method=='GET':
		user_id = request.session['username']
		conn = psycopg2.connect(conn_str)
		new_query = "with e as (select orderItem.orderId,loginName,dateTime,item,itemQuantity from orderItem inner join public.order on public.order.orderId = orderItem.orderId) select * from e where"+" loginName="+" '"+user_id+"' "+" order by orderId desc limit 15;"
		_ ,rows = exec_query(conn,new_query)
		order_details = """<tr>
						<th>orderId</th>
						<th>Name</th>
						<th>dateTime</th>
						<th>samosa Quantity</th>
						<th>idli Quantity</th>
						<th>chai Quantity</th>
						</tr> """
		for i in range(0,len(rows)//3):
			a,b,c,d,e = rows[3*i]
			_,_,_,_,f = rows[3*i+1]
			_,_,_,_,g = rows[3*i+2]
			order_details = order_details + """<tr>""" + """<td>"""+ str(a) + """</td>""" + """<td>"""+ str(b) + """</td>"""+ """<td>"""+ str(c)+ """</td>"""+ """<td>"""+ str(g) + """</td>"""+ """<td>"""+ str(f) + """</td>"""+ """<td>"""+ str(e) + """</td>"""+"""</tr> """
		return HttpResponse(details+ order_details+ html1)
	if request.method =='POST':
		samosa = request.POST["samosa"]
		idli =  request.POST["idli"]
		chai = request.POST["chai"]
		username = request.session['username']
		date =  datetime.datetime.now()
		conn = psycopg2.connect(conn_str)
		new_query = "with e as (select orderItem.orderId,loginName,dateTime,item,itemQuantity from orderItem inner join public.order on public.order.orderId = orderItem.orderId) select * from e where"+" loginName="+" '"+username+"' "+" order by orderId desc limit 15;"
		_ ,rows = exec_query(conn,new_query)
		order_details = """<tr>
						<th>orderId</th>
						<th>Name</th>
						<th>dateTime</th>
						<th>samosa Quantity</th>
						<th>idli Quantity</th>
						<th>chai Quantity</th>
						</tr> """
		for i in range(0,len(rows)//3):
			a,b,c,d,e = rows[3*i]
			_,_,_,_,f = rows[3*i+1]
			_,_,_,_,g = rows[3*i+2]
			order_details = order_details + """<tr>""" + """<td>"""+ str(a) + """</td>""" + """<td>"""+ str(b) + """</td>"""+ """<td>"""+ str(c)+ """</td>"""+ """<td>"""+ str(g) + """</td>"""+ """<td>"""+ str(f) + """</td>"""+ """<td>"""+ str(e) + """</td>"""+"""</tr> """
	   
		try:
			if int(samosa)<0 or int(idli)<0 or int(chai)<0:
				return HttpResponse(details + order_details+html1+fail1)
			else:
				conn = psycopg2.connect(conn_str)
				query4 = "insert into public.order values (DEFAULT "+","+"'"+username+"'"+ ", " + "'"+str(date) + "') returning orderId;"
				cursor = conn.cursor()
				_ ,rows1 = exec_query(conn,query4)
				conn.commit()
				val = rows1[0][0]
				print(val)
				query1 = "insert into orderItem values  ("+"'"+str(val)+"'"+",'"+"samosa"+ "', " + "'"+str(samosa) + "');"
				query2 = "insert into orderItem values  ("+"'"+str(val)+"'"+",'"+"idli"+ "', " + "'"+str(idli) + "');"
				query3 = "insert into orderItem values  ("+"'"+str(val)+"'"+",'"+"chai"+ "', " + "'"+str(chai) + "');"
				cursor.execute(query1)
				cursor.execute(query2)
				cursor.execute(query3)
				conn.commit()
				new_query = "with e as (select orderItem.orderId,loginName,dateTime,item,itemQuantity from orderItem inner join public.order on public.order.orderId = orderItem.orderId) select * from e where"+" loginName="+" '"+username+"' "+" order by orderId desc limit 15;"
				_ ,rows = exec_query(conn,new_query)
				order_details = """<tr>
									<th>orderId</th>
									<th>Name</th>
									<th>dateTime</th>
									<th>samosa Quantity</th>
									<th>idli Quantity</th>
									<th>chai Quantity</th>
									</tr> """
				for i in range(0,len(rows)//3):
					a,b,c,d,e = rows[3*i]
					_,_,_,_,f = rows[3*i+1]
					_,_,_,_,g = rows[3*i+2]
					order_details = order_details + """<tr>""" + """<td>"""+ str(a) + """</td>""" + """<td>"""+ str(b) + """</td>"""+ """<td>"""+ str(c)+ """</td>"""+ """<td>"""+ str(g) + """</td>"""+ """<td>"""+ str(f) + """</td>"""+ """<td>"""+ str(e) + """</td>"""+"""</tr> """
				conn.close()
				return HttpResponse(details+order_details+html1 + success)
		except:
			return HttpResponse(details + order_details+html1+fail2)            
