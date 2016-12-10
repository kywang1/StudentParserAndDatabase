import psycopg2
import csv
import os

conn = psycopg2.connect("dbname=postgres host = /home/"+os.environ['USER']+"/postgres")
print "Database opened successfully"

curr = conn.cursor()

#curr.execute('DROP TABLE Student')
#curr.execute('DROP TABLE StudentStatus')
#curr.execute('DROP TABLE EnrolledIn' )
#curr.execute('DROP TABLE CourseOffered')
#curr.execute('DROP TABLE Course')
#curr.execute('DROP TABLE MeetsAt')
#conn.commit()

createStudent = ('''CREATE TABLE Student
                (SID INT NOT NULL,
                surname TEXT NOT NULL,
                prefername TEXT NOT NULL,
                email TEXT  NOT NULL,
                PRIMARY KEY(SID));''')

createStudentStatus = ('''CREATE TABLE StudentStatus
                (SID INT ,
                TERM INT,
                MAJOR  TEXT,
                CLASS TEXT,
                LEVEL TEXT,
                PRIMARY KEY(SID,TERM));''')

createEnrolledIn = ('''CREATE TABLE EnrolledIn
                (SID INT ,
                CID INT,
                TERM INT,
                SEAT INT,
                UNITS FLOAT,
                GRADE TEXT,
                STATUS TEXT,
                NUMBERGRADE FLOAT,
                PRIMARY KEY(SID,CID,TERM));''')

createCourseOffered = ('''CREATE TABLE CourseOffered
		(CID INT ,
                TERM INT,
                SECTION INT,
                CRSE INT,
                INSTRUCTOR TEXT,
                SUBJECT TEXT,
                PRIMARY KEY(CID,TERM,SUBJECT,CRSE));''')

createCourse = ('''CREATE TABLE Course
                (CRSE INT,
                SUBJECT TEXT,
                MAXUNITS INT,
                MINUNITS INT,
                PRIMARY KEY(CRSE,SUBJECT));''')

createMeetsAt = ('''CREATE TABLE MeetsAt
                (CID INT,
                TERM INT,
                ROOM TEXT,
                BUILD TEXT,
                DAY TEXT,
                TIME TEXT,
                TYPE TEXT,
                PRIMARY KEY(CID,TERM,ROOM,BUILD,TYPE,DAY,TIME));''')

               
curr.execute(createStudent)
curr.execute(createStudentStatus)
curr.execute(createEnrolledIn)
curr.execute(createCourseOffered)
curr.execute(createCourse)
curr.execute(createMeetsAt)
conn.commit()

