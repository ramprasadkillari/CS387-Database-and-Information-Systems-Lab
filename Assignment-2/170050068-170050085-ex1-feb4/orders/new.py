from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
sys.excepthook = sys.__excepthook__
import psycopg2
from django.views.decorators.csrf import csrf_exempt
import datetime

fail = """<body><h1> Sorry Unable to Login, Retry</h1></body>"""
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
            </table>
            <h2>Order Items</h2>

            <form name="orderitems" method="post" action="/order">
            samosa:<br>
            <input type="text" name="samosa" >
            <br>
            idli:<br>
            <input type="text" name="idli" min=>
            <br>
            chai:<br>
            <input type="text" name="chai">
            <br><br>
            <input type="submit" value="Submit">
            </form>
            </body></html> 
          """


@csrf_exempt
def Login(request):
    if request.method == 'GET':
        return HttpResponse(html)
    if request.method == 'POST':
        pass
        

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

def user_verify(request):
    user_id = request.POST["userid"]
    passwd  = request.POST["pwd"]

    conn = psycopg2.connect("host=127.0.0.1 port=5850 dbname=postgres")
    query = "select loginname from addausers where loginName = " + "'"+ user_id + "'" +" and password = " + "'"+passwd+ "';"
    a, b = exec_query(conn,query)
    request.session['username'] = user_id
    request.session['passwd'] = passwd

    if b != []:
        conn = psycopg2.connect("host=127.0.0.1 port=5850 dbname=postgres")
        query2 = "select * from orderHistory"+" where"+" loginName="+" '"+user_id+"' "+" order by orderId desc limit 5;"
        _ ,rows = exec_query(conn,query2)
        order_details = """<tr>
                        <th>orderId</th>
                        <th>Name</th>
                        <th>dateTime</th>
                        <th>idli Quantity</th>
                        <th>samosa Quantity</th>
                        <th>chai Quantity</th>
                        </tr> """
        for i in range(0,len(rows)):
            a,b,c,d,e,f = rows[i]
            order_details = order_details + """<tr>""" + """<td>"""+ str(a) + """</td>""" + """<td>"""+ str(b) + """</td>"""+ """<td>"""+ str(c)+ """</td>"""+ """<td>"""+ str(d) + """</td>"""+ """<td>"""+ str(e) + """</td>"""+ """<td>"""+ str(f) + """</td>"""+"""</tr> """

        return HttpResponse(details+ order_details+ html1)

    else:
        return HttpResponse(html+fail)

@csrf_exempt
def user_direct(request):
    samosa = request.POST["samosa"]
    idli =  request.POST["idli"]
    chai = request.POST["chai"]
    username = request.session['username']
    date =  datetime.datetime.now()
    conn = psycopg2.connect("host=127.0.0.1 port=5850 dbname=postgres")
    query1 = "insert into orderHistory values (DEFAULT "+","+ "'" + username+"'"+","+"'" +str(date) +"'"+ ", " + "'"+ idli + "'"+ ", "+ "'"+ samosa + "'"+ ", "+ "'"+ chai + "'"+ ")"
    query2 = "select * from orderHistory"+" where"+" loginName="+" '"+username+"' "+" order by orderId desc limit 5;"
    cursor = conn.cursor()
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    _ ,rows = exec_query(conn,query2)
    order_details = """<tr>
                        <th>orderId</th>
                        <th>Name</th>
                        <th>dateTime</th>
                        <th>idli Quantity</th>
                        <th>samosa Quantity</th>
                        <th>chai Quantity</th>
                        </tr> """
    for i in range(0,len(rows)):
        a,b,c,d,e,f = rows[i]
        order_details = order_details + """<tr>""" + """<td>"""+ str(a) + """</td>""" + """<td>"""+ str(b) + """</td>"""+ """<td>"""+ str(c)+ """</td>"""+ """<td>"""+ str(d) + """</td>"""+ """<td>"""+ str(e) + """</td>"""+ """<td>"""+ str(f) + """</td>"""+"""</tr> """

    return HttpResponse(details+order_details+html1)


