from django.test import TestCase
from django.db import connection
from acad.models import Department, Section, Instructor, Student, Takes, Teaches
from uni.settings import DATABASES as config
from django.db.models import Q, Sum
import psycopg2
import os
# Create your tests here.

def db_exec(conn,sql):
	cursor = conn.cursor()
	cursor.execute(sql)
	header = [desc[0] for desc in cursor.description]
	rows = cursor.fetchall()
	return (header, rows)

class MyTestCases(TestCase):
	def setUp(self):
		os.system("pg_dump -h {} -p {} uni > dump.sql".format(config['default']['HOST'], config['default']['PORT']))
		# os.system("echo 'drop schema public cascade; create schema public' | psql -h {} -p {} -d test_uni >/dev/null 2>&1".format(config['default']['HOST'], config['default']['PORT']))
		os.system("psql -h {} -p {} -d test_uni -f dump.sql >/dev/null 2>&1".format(config['default']['HOST'], config['default']['PORT']))
	
	def test_student_count(self):
	
		query1 = '''Select count(*) from Student where dept_name='Physics'; '''
		query2 = '''Select count(*) from Student where dept_name='Physics' or dept_name='Comp. Sci.'; '''
		query3 = '''Select name from Student join Department using (dept_name) where building ilike 'taylor';'''
		query4 = '''Select dept_name,sum(salary) from Instructor group By dept_name order by dept_name; '''
		query5 = '''select distinct course_id from Student S join Takes T on (T.student_id=S.id) join Section SC on (T.section_id=SC.id)  where S.name='Tanaka';'''
		query6 = '''select distinct I.name from Instructor I join Teaches T on (I.id=T.instructor_id) join Takes  Tk on (T.section_id=Tk.section_id) join Student S on (Tk.student_id=S.id) where S.name='Brown';'''

		(header, rows) = db_exec(connection,query1)
		model_student_count = Student.objects.filter(dept_name="Physics").count() # 1
		# model_student_count = len(Phy)
		sql_student_count = rows[0][0]
		# print("Hifdfdf: ",model_student_count)
		self.assertEqual(sql_student_count, model_student_count)

		model_student_count = Student.objects.filter( Q(dept_name="Physics") | Q(dept_name="Comp. Sci.") ).count() # 2
		(header, rows) = db_exec(connection,query2)
		sql_student_count = rows[0][0]
		self.assertEqual(sql_student_count, model_student_count)

		Taylors = Student.objects.filter(dept_name__building__iexact='taylor').values_list('name') # 3
		Taylors = [a[0] for a in Taylors]
		(header, rows) = db_exec(connection,query3)
		rows = [r[0] for r in rows]
		self.assertEqual(Taylors, rows)
		
		Totsal = Department.objects.annotate(total_sal=Sum('instructors__salary')).order_by('dept_name').values_list('dept_name','total_sal')  # 4
		Totsal = list(Totsal)
		# print("Total Sal: ",Totsal)
		(header, rows) = db_exec(connection,query4)
		# sql_student_count = rows[0][0]
		self.assertEqual(Totsal, rows)

		TanakaCourses = Takes.objects.filter(student__name='Tanaka').values_list('section__course_id',flat=True) #5
		TanakaCourses = list(TanakaCourses)
		(header, rows) = db_exec(connection,query5)
		rows = [r[0] for r in rows]
		self.assertEqual(TanakaCourses, rows)


		# Sec_list = list(Student.objects.filter(name='Brown').values_list('takes__section__id',flat=True))
		# Inst_brown = Instructor.objects.filter(section__id__in=Sec_list).values_list('name').distinct()  # 6
		Inst_brown = Teaches.objects.filter(section__taken_by__name='Brown').values_list('instructor__name')
		Inst_brown = [a[0] for a in Inst_brown]
		(header, rows) = db_exec(connection,query6)
		rows = [r[0] for r in rows]
		# print(rows)
		self.assertEqual(Inst_brown, rows)
