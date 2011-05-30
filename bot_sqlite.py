import sqlite3

def create(database):
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("create table LOG (id INTEGER PRIMARY KEY, time TEXT, sort TEXT, user TEXT, msg TEXT)")
	con.commit()
	cur.close()
	
def add(database, order, who, message):
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("insert into LOG values (NULL, datetime('now', 'localtime'), ?, ?, ?)", (order.decode('utf-8'), who.decode('utf-8'), message.decode('utf-8')))
	con.commit()
	cur.close()
	
def seen(database, person):
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("select * from LOG where user=? ORDER BY time DESC" , [person.decode('utf-8')])
	con.commit()
	
	watch = cur.fetchall()
	
	cur.close()
	
	if watch:
		return watch[0][1]
	else:
		return "never"