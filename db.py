import mysql.connector as db
from contextlib import closing

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
  with closing(db_connect()) as conn:
    with closing(conn.cursor()) as cur:
      cur.executemany(sql, value)
      conn.commit()    
