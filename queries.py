from __future__ import division
import psycopg2
import os
import array

conn = psycopg2.connect("dbname=postgres host = /home/"+os.environ['USER']+"/postgres")
print "Database opened successfully"
curr = conn.cursor()

#########################################################################################################################
#3a
unitCounter = [1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
curr.execute("SELECT DISTINCT ON(term) term FROM courseoffered;")
terms = curr.fetchall()

print ("3a")
numberOfStudents = 0
totalStudents = 0
a = array.array('i',(0 for i in range(0,20))) #http://stackoverflow.com/questions/1859864/how-to-create-an-integer-array-in-python

for i in unitCounter:
	for x in terms:
		query = ("""SELECT COUNT(sid) 
				FROM (SELECT SUM(units) AS totalunits, SID 
					FROM (SELECT sid,units FROM enrolledin WHERE term = %d) AS sub GROUP BY SID) as sub2 
				WHERE totalunits = %d;""")%(x[0],i)
		curr.execute(query)
		conn.commit()
		numberOfStudents = str(curr.fetchone())	
		numberOfStudents = numberOfStudents.replace("L","")
		numberOfStudents = numberOfStudents.replace(",","")
		numberOfStudents = numberOfStudents.replace("(","")
		numberOfStudents = numberOfStudents.replace(")","")
		numberOfStudents = int(numberOfStudents)
		a[i-1] += numberOfStudents
		#print a[i-1]
		totalStudents += numberOfStudents

for x in range(0,20):
	percent = (a[x])/totalStudents
	print("%f percent of students took %d units")%(percent, x+1)

#########################################################################################################################
#3b
print ("3b")
b = array.array('i',(0 for i in range(0,20)))

for i in unitCounter:
	gpaCounter = 0
	totalGPA = 0
	for x in terms:
		query2 = ("""SELECT AVG(GPA) 
					FROM (SELECT SUM(units) AS totalunits, AVG(numbergrade) AS gpa, SID 
						FROM (SELECT sid, units,numbergrade FROM enrolledin WHERE 
							term = %d AND grade != 'NULL' AND grade != 'I' AND grade != 'IP' AND grade != 'NG' AND grade != 'NP'
							AND grade != 'NS' AND grade != 'P' AND grade != 'S' AND grade != 'U' AND grade != 'W04'
							AND grade != 'W10' AND grade != 'WD1' AND grade != 'WD2' AND grade != 'WD4'	) AS sub GROUP BY SID) 
							as sub2 WHERE totalunits = %d;
						""")%(x[0],i)
		curr.execute(query2)
		conn.commit()
		avgGPA = str(curr.fetchone())	
		avgGPA = avgGPA.replace(",","")
		avgGPA = avgGPA.replace("(","")
		avgGPA = avgGPA.replace(")","")
		if avgGPA != ("None"):
			avgGPA = float(avgGPA)
			gpaCounter = gpaCounter+1
			totalGPA = totalGPA + avgGPA

	avgGPAForTerm = totalGPA/gpaCounter
	print ("%f is the average gpa for people taking %i units")%(avgGPAForTerm,i)
		#a[i-1] += avgGPA
		#print a[i-1]


#########################################################################################################################
#3c
print("3c")

query3 =  ("""SELECT INSTRUCTOR, AVG(numbergrade) 
			FROM enrolledin NATURAL JOIN courseoffered 
			WHERE grade != 'NULL' AND grade != 'I' AND grade != 'IP' AND grade != 'NG' AND grade != 'NP'
			AND grade != 'NS' AND grade != 'P' AND grade != 'S' AND grade != 'U' AND grade != 'W04'
			AND grade != 'W10' AND grade != 'WD1' AND grade != 'WD2' AND grade != 'WD4' AND grade != 'WDC'
			AND grade != 'WI' AND grade != 'WN' AND grade != 'WI' AND grade != 'XR' AND grade != 'Y' 
			GROUP BY instructor 
			ORDER BY AVG(numbergrade) DESC;
""")
curr.execute(query3)
answer3c = curr.fetchall()
print ("Easiest Instructors")
for i in range(0,5):
	print answer3c[i] 

print("Hardest Teachers")
print answer3c[-1]
print answer3c[-2]
print answer3c[-3]
print answer3c[-4]
print answer3c[-5]

#########################################################################################################################
#3d
print("3d")

query4 =  ("""SELECT INSTRUCTOR, AVG(numbergrade)
			FROM (SELECT * FROM courseoffered NATURAL JOIN enrolledin) as sub NATURAL JOIN course 
			WHERE grade != 'NULL' AND grade != 'I' AND grade != 'IP' AND grade != 'NG' AND grade != 'NP'
			AND grade != 'NS' AND grade != 'P' AND grade != 'S' AND grade != 'U' AND grade != 'W04'
			AND grade != 'W10' AND grade != 'WD1' AND grade != 'WD2' AND grade != 'WD4' AND grade != 'WDC'
			AND grade != 'WI' AND grade != 'WN' AND grade != 'WI' AND grade != 'XR' AND grade != 'Y' AND subject = 'ABC'
			AND crse >= 100 AND crse < 200
			GROUP BY instructor 
			ORDER BY AVG(numbergrade) DESC;
""")

curr.execute(query4)
answer3d = curr.fetchall()
print ("Easiest Instructors")
for i in range(0,5):
	print answer3d[i] 


print("Hardest Teachers")
print answer3d[-1]
print answer3d[-2]
print answer3d[-3]
print answer3d[-4]
print answer3d[-5]

#########################################################################################################################
#3e
print("3e")
print("\n")

#########################################################################################################################
#3f
print("3f")

query5 =  ("""SELECT AVG(numbergrade),major 
			FROM  (SELECT * FROM courseoffered NATURAL JOIN enrolledin) as sub NATURAL JOIN studentstatus 
			WHERE subject = 'ABC' AND grade != 'NULL' AND grade != 'I' AND grade != 'IP' AND grade != 'NG' AND grade != 'NP'
			AND grade != 'NS' AND grade != 'P' AND grade != 'S' AND grade != 'U' AND grade != 'W04'
			AND grade != 'W10' AND grade != 'WD1' AND grade != 'WD2' AND grade != 'WD4' AND grade != 'WDC'
			AND grade != 'WI' AND grade != 'WN' AND grade != 'WI' AND grade != 'XR' AND grade != 'Y' 
			GROUP BY major ORDER BY AVG(numbergrade) DESC;
""")

curr.execute(query5)
answer3f = curr.fetchall()
print("Major that performs the best for ABC courses")
print answer3f[0]
print("Major that performs the worst for ABC courses")
print answer3f[-1]