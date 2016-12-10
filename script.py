import psycopg2
import csv 
import os

conn = psycopg2.connect("dbname=postgres host = /home/"+os.environ['USER']+"/postgres")
print "Database opened successfully"

curr = conn.cursor()

curr.execute('DELETE FROM student')
curr.execute('DELETE FROM studentstatus')
curr.execute('DELETE FROM enrolledin')
curr.execute('DELETE FROM courseoffered')
curr.execute('DELETE FROM course')
curr.execute('DELETE FROM meetsat')

conn.commit()
