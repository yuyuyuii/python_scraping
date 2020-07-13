import mysql.connector as db

# db接続
def db_connect():
  conn = db.connect(
      host='localhost',
      port='3306',
      user='root',
      password='',
      database='python_sample'
  )
  return conn

# insert
def db_insert(sql, value):
  db = db_connect()
  cur = db.cursor()
  cur.executemany(sql, value)
  cur.close()
  db.commit()
  db.close()
