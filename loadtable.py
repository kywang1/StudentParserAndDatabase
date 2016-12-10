import psycopg2
import csv
import os
import glob

studentDictionary = {}
studentStatusDictionary = {}
meetsAtDictionary = {}

def convertGrade(grade):
    if grade == "A":
        value = 4.0
    elif grade == "A+" :
        value =  4.0
    elif grade == "A-":
        value =  3.7
    elif grade == "B+":
        value =  3.3
    elif grade == "B":
        value =  3.0
    elif grade == "B-":
        value =  2.7
    elif grade == "C+":
        value =  2.3
    elif grade == "C":
        value =  2.0
    elif grade == "C-":
        value =  1.7
    elif grade == "D+":
        value =  1.3
    elif grade == "D":
        value =  1.0
    elif grade == "D-":
        value =  .7
    elif grade == "":
        value = 0
    else:
        value =  0
    return value;

def load_student (data,conn,curr):
    flag1 = False #flag to determine that we have found a CLASS line
    flag2 = False #flag to determine that we have found a MEETING line
    flag3 = False #flag to determine we have found STUDENT line
    flag4 = True #flag to determine if line after CID is not corrupted
    flag5 = False #flag to determine if students are registered for the class
    count = 0
    INSTRUCTOR = ''
    TYPE = ''
    DAYS =''
    TIME = ''
    BUILD = ''
    ROOM = ''

    StudentSQL = ""
    StudentStatusSQL = ""
    EnrolledInSQL = ""
    CourseOfferedSQL = ""
    CourseSQL = ""
    MeetsAtSQL = ""
    TempMeetsAtSQL = ""
    LocationSQL = ""

    for row in data:
	if flag3 == True and count == 2 and len(row) != 1:
	    flag5 = True
        
        if count == 3:

            if flag5 == True: #if class has student enrolled in it 
        
                CourseSQL += "SELECT %d,'%s',%f,%f  WHERE NOT EXISTS (SELECT 1 FROM COURSE  WHERE CRSE = %d AND SUBJECT = '%s'))" %(int(CRSE),SUBJ, float(MAXUNITS), float(MINUNITS),int(CRSE), SUBJ) #works 
                #CourseSQL=CourseSQL[:-1]+";"
                CourseSQL = "INSERT INTO COURSE(CRSE,SUBJECT,MAXUNITS,MINUNITS) " + CourseSQL
                CourseSQL = CourseSQL[:-1]+";"
                curr.execute(CourseSQL)
                conn.commit()
                CourseSQL = ''
           
    
                #append courseOffered
                CourseOfferedSQL += "(%d,%d,%d,%d,'%s','%s'),"%(int(CID),int(TERM),int(SEC),int(CRSE),INSTRUCTOR,SUBJ)
                #append meetsAt
                MeetsAtSQL += TempMeetsAtSQL
    
            flag5 = False
            INSTRUCTOR = ''
            TYPE = ''
            DAYS =''
            TIME = ''
            BUILD = ''
            ROOM = ''
            TempMeetsAtSQL = ''

            flag3 = False 
            count = 0

        if len(row) == 1:
            count = count +1
 
        if flag1 == True and count == 0:
            flag4 = True
            for col in row:
                if col == '':
                    flag4 = False
            if flag4 == True:

                CID = row[0]
                TERM = row[1]
                SUBJ = row[2]
                CRSE = row[3]
                SEC = row[4]
                UNITS = row[5]

                unitSplitted = UNITS.split('-')
                if len(unitSplitted) == 2:
                    MAXUNITS = unitSplitted[1]
                    MINUNITS = unitSplitted[0]
                else:
                    MAXUNITS = UNITS
                    MINUNITS = UNITS

            flag1 = False
            #print CID
        
        if row[0] == 'CID':
            flag1 = True
        
        
        if count == 2:
            flag2 = False

        if flag2 == True and count ==1:
            if flag2 == True:
                #print row
                if row[0] != '':
                    INSTRUCTOR = row[0]
                    INSTRUCTOR = INSTRUCTOR.replace('\'','\"')   
                if row[1] != '':
                    TYPE = row[1] 
                if row[2] != '':
                    DAYS = row[2]
                if row[3] != '':
                    TIME = row[3]
                if row[4] != '':
                    BUILD = row[4]
                if row[5] != '':
                    ROOM = row[5]
                else:
                    ROOM = 'NULL'
            #print TYPE + "Meets At: " + ROOM + " " + BUILD + " On:  " + DAYS + " " + TIME # append queries here
                                                                                        # for different class types
                INSTRUCTORTOROOM = ('%s'+'%s'+'%s'+'%s'+'%s'+'%s')%(INSTRUCTOR,TYPE,DAYS,TIME,BUILD,ROOM)
                test3 = INSTRUCTORTOROOM in meetsAtDictionary
                if test3 == False:
                    TempMeetsAtSQL +="(%d,%d,'%s','%s','%s','%s','%s'),"%(int(CID),int(TERM),ROOM,BUILD,DAYS,TIME,TYPE) 
                    meetsAtDictionary[INSTRUCTORTOROOM] = 1 

    
        if row[0] == 'INSTRUCTOR(S)':
            flag2 = True

        if flag3 == True and count == 2:
            SEAT = row[0]
            SID = row[1]
            SURNAME = row[2]
            PREFNAME = row[3]
            LEVEL = row[4]
            UNITS = row[5]
            if(UNITS ==''):
                UNITS = '-1'
            CLASS = row[6]
            MAJOR = row[7]
            GRADE = row[8]
            STATUS = row[9]
            EMAIL = row[10]
            if GRADE == '':
                GRADE = 'NULL'

            NUMBERGRADE = convertGrade(GRADE)
            
            test =  SID in studentDictionary #http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
            #print 'Student: '+ SID + ' ' +  SURNAME + ' ' +  PREFNAME + ' ' + EMAIL
            #If student exist in dictionary
            if test == False:
                SURNAME = SURNAME.replace('\'','\"')
                EMAIL = EMAIL.replace('\'','\"')
                StudentSQL += "('%d', '%s','%s', '%s')," %(int(SID),SURNAME, PREFNAME, EMAIL)
                studentDictionary[SID] = 1
            #print 'Student Status: '+ SID+ ' '+ TERM+ ' '+MAJOR+ ' '+ CLASS+ ' '+LEVEL
        
            SIDTERM = ('%s'+'%s')%(SID,TERM)
            test2 = SIDTERM in studentStatusDictionary
            #if studenstatus is already recorded
            if test2 == False:
                StudentStatusSQL += "(%d, %d,'%s', '%s', '%s')," %(int(SID),int(TERM),MAJOR,CLASS, LEVEL)
                studentStatusDictionary[SIDTERM] = 1

            #print 'Enrolled In: ' + SID+' '+CID+' '+TERM+' '+SEAT+' '+UNITS+' '+GRADE+' '+STATUS
            EnrolledInSQL += "(%d, %d, %d, %d,%f,'%s','%s',%f)," %(int(SID),int(CID), int(TERM), int(SEAT),float(UNITS),GRADE,STATUS,NUMBERGRADE)
            
        if row[0] == 'SEAT':
            flag3 = True

    StudentSQL=StudentSQL[:-1]+";"
    StudentSQL = "INSERT INTO Student(SID,surname,prefername,email) VALUES " + StudentSQL
    curr.execute(StudentSQL) #works
    conn.commit()
    
    StudentStatusSQL = StudentStatusSQL[:-1]+";"
    StudentStatusSQL = "INSERT INTO StudentStatus(SID,TERM,MAJOR,CLASS,LEVEL) VALUES"+ StudentStatusSQL
    curr.execute(StudentStatusSQL) #works
    conn.commit()         

    EnrolledInSQL = EnrolledInSQL[:-1]+";"
    EnrolledInSQL = "INSERT INTO EnrolledIn(SID,CID,TERM,SEAT,UNITS,GRADE,STATUS,NUMBERGRADE) VALUES"+EnrolledInSQL
    curr.execute(EnrolledInSQL) #works
    conn.commit()

    CourseOfferedSQL = CourseOfferedSQL[:-1]+";"
    CourseOfferedSQL = "INSERT INTO CourseOffered(CID,TERM,SECTION,CRSE,INSTRUCTOR,SUBJECT) VALUES"+CourseOfferedSQL
    curr.execute(CourseOfferedSQL) #works
    conn.commit() 

    MeetsAtSQL = "INSERT INTO MeetsAt( CID,TERM,ROOM,BUILD,DAY,TIME,TYPE) VALUES "+ MeetsAtSQL
    MeetsAtSQL = MeetsAtSQL[:-1]+";"
    if MeetsAtSQL[-7:] != "VALUES;":
        curr.execute(MeetsAtSQL) #work
        conn.commit()
        
if __name__ == '__main__':
    conn = psycopg2.connect("dbname=postgres host=/home/"+os.environ['USER']+"/postgres")
    curr = conn.cursor()
    
    path =  '/home/kywang1/ECS165A/HW4/Grades/' # <---- specift this path to the grade folder

    for filename in glob.glob(os.path.join(path,"*.csv")): #http://bogdan.org.ua/2007/08/12/python-iterate-and-read-all-files-in-a-directory-folder.html
    
        CSVReader = csv.reader(open(filename))
        next(CSVReader)
        load_student(CSVReader,conn, curr)
    #yearData =  open('/home/kywang1/ECS165A/HW4/Grades/1989_Q3.csv') 
    #CSVReader = csv.reader(yearData)
    #next(CSVReader)
    #load_student(CSVReader,conn, curr)
