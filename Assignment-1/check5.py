# CS387 Assignment 5, Jan 27
# This uses the requests library to simulate a user filling in a form on the browser.
# The checks below assume that the format of the returned html is identical to that of ex5-sample.html

from subprocess import Popen, DEVNULL
import requests
import re
import time
import sys
import traceback
import dbexec

HTTP_OK = 200

def check():
    try:
       # launch pyweb3.py as a separate process. It'll be killed in the finally block
       p = Popen(['python3', 'pyweb3.py'], stdout=DEVNULL, stderr=DEVNULL)
       time.sleep(1) # allow time for it to settle down and start listening to socket
       (points, err) = check_editable_form()
       if err:
           return (points, err)
        
       (points2, err) = fill_form_and_check_db()
       points += points2
       return (points, err)
    except Exception as e:
        traceback.print_exc()
        return (0, str(e))
    finally: #cleanup
        try:
            p.kill() 
        except:
            pass

def check_editable_form():
    # Simulate a click on 'student' on the dropdown list and hitting submit. It should return
    # a form tailored to the student table, with editable fields for each attribute
    NUM_TABLES = 11 # in university schema.
    NUM_ATTRS_IN_STUDENT = 4
    resp = requests.post("http://localhost:8000/add", {'table_select': 'student'})
    if resp.status_code == HTTP_OK and \
      len(re.findall('option value', resp.text)) >= NUM_TABLES and \
      len(re.findall('input type *= *"text"', resp.text)) == NUM_ATTRS_IN_STUDENT:
        return (5, None)
    else:
        return (0, "Selected 'student' table. Expected a dropdown list with {} tables, and a form with {} editable fields".format(NUM_TABLES, NUM_ATTRS_IN_STUDENT))

def fill_form_and_check_db():
    # Simulate filling the form and hitting submit
    resp = requests.post("http://localhost:8000/add",
                             {  'table_name': 'student',
                                'id': '77777',  
                                'name': 'thor',
                                'dept_name': 'Biology',
                                'tot_cred' : '100'
                             })
    if resp.status_code == HTTP_OK:
        return check_record_in_db()
    else:
        return (0, "Attempted insert of record in student, but http post did not succeed\n" + resp)

def check_record_in_db():
    try:
        err = None
        points = 0
        conn = dbexec.connect()
        (header, rows) = dbexec.exec_query(conn, "select count(*) from student where id = '77777'")
        if len(rows) == 1 and rows[0][0] == 1:
            c  = conn.cursor()
            c.execute("delete from student where id = '77777'")
            c.close()
            points = 5
        else:
            err = "Could not find student id '77777' in the database\n" + str(rows)
        conn.commit()
        conn.close()
        return (points, err)
    except Exception as e:
        # Unrecoverable error. 
        traceback.print_exc()
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    try:
        (points, err) = check()
        print (points, err)
    except:
        traceback.print_exc()
