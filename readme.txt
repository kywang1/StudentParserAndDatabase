Kyle Wang 998969415
Tue Doan 998143231

Connection is opened to database called postgres.
Specify the path to the directory that the grade csvs are going to be located. I did it with my loadtable.py in the same directory as the
 grade folder. 
Loading all the data into the database should take around a minute. Queries would take around 2 minutes to process. 
Program was done one Python on the CSIF computer. Assuming that the python vesion on the CSIF is 3.5.1 or whatever version is installed on csif machines. 

Directions:
To first create the tables run the maketable.py script. Than run the loadtable.py script. Next run the queries.py script to get the results for the queries. maketable.py and loadtable.py should only be ran once. If you want to re-run these two, you have have to drop all thetables or delete all the data from the database if you just want to re-run loadtable.py

Resources Used:
https://www.tutorialspoint.com/postgresql/postgresql_python.htm
https://pyformat.info/
http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
http://bogdan.org.ua/2007/08/12/python-iterate-and-read-all-files-in-a-directory-folder.html
http://piazza.com
