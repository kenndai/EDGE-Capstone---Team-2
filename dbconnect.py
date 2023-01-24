import psycopg2

#pyscopg2 - this is a library that helps me connect to a postgres database
#from Python

# if you see an error that says something like "bind error, port not available"
# to fix it you can do "sudo lsof -i:5432"  and then run "sudo kill -9 <process ID>"

# this connects to the Docker container running postgres:
conn = psycopg2.connect(
    host="localhost",  # this will change to point to our rds database
    database="postgres",
    user="postgres",
    password="test")

#we use cursor so that we can run some SQL
cursor = conn.cursor()

#this is a sanity check - to verfiy that we are indeed connected to postgres:
cursor.execute('SELECT * FROM information_schema.tables')


#now that you have a cursor, you can insert into your DB, retrieve, etc..


rows = cursor.fetchall()
for table in rows:
    print(table)
conn.close()