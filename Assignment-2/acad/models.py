# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Department(models.Model):
    dept_name = models.CharField(primary_key=True, max_length=20)
    building = models.CharField(max_length=15, blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'department'


class Section(models.Model):
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=8)
    semester = models.CharField(max_length=6)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    building = models.CharField(max_length=15, blank=True, null=True)
    room_number = models.CharField(max_length=7, blank=True, null=True)
    time_slot_id = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'section'
        unique_together = (('course_id', 'sec_id', 'year', 'semester'),)

class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=20)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True,related_name='instructors')
    salary = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    section = models.ManyToManyField(Section,
                through='Teaches',
                through_fields=('instructor','section'),
                related_name="taught_by")
    class Meta:
        # managed = False
        db_table = 'instructor'




class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=20)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True,related_name='students')
    tot_cred = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    section = models.ManyToManyField(Section,
                    through='Takes',
                    through_fields=('student','section'),
                    related_name="taken_by")
    class Meta:
        # managed = False
        db_table = 'student'


class Takes(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING,related_name='takes')
    grade = models.CharField(max_length=2, blank=True, null=True)
    section = models.ForeignKey(Section, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'takes'


class Teaches(models.Model):
    instructor = models.ForeignKey(Instructor, models.DO_NOTHING,related_name='teaches')
    section = models.ForeignKey(Section, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'teaches'
