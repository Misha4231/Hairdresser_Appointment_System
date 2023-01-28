import sqlite3 as sq

db = sq.connect('C:\\Users\\Misha.DESKTOP-49T8NCT\\code files\\django\\pet project try\\my_site\\sqlite3.db')
cur = db.cursor()

a=cur.execute("SELECT * FROM test").fetchall()
print(a)
db.commit()