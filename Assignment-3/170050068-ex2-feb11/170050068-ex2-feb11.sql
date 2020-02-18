alter table takes add section_id integer;
alter table section add id serial;

update takes set section_id=(select s.id from section as s where s.course_id=takes.course_id and s.semester=takes.semester and s.sec_id=takes.sec_id and s.year=takes.year);

alter table takes drop constraint takes_course_id_fkey;

alter table teaches drop constraint teaches_course_id_fkey;

alter table section drop constraint section_pkey;

alter table section add constraint section_pkey primary key (ID);

alter table takes add  foreign key (section_id) references section (ID);

alter table takes drop column course_id;
alter table takes drop column sec_id;
alter table takes drop column semester;
alter table takes drop column year;

alter table section add unique (course_id,sec_id,year, semester);


alter table teaches add section_id integer;

update teaches set section_id=(select s.id from section as s where s.course_id=teaches.course_id and s.semester=teaches.semester and s.sec_id=teaches.sec_id and s.year=teaches.year);

alter table teaches add foreign key (section_id) references section(id);

alter table teaches drop column course_id;
alter table teaches drop column sec_id;
alter table teaches drop column semester;
alter table teaches drop column year;

alter table takes rename id to student_id;

alter table teaches rename id to instructor_id;
