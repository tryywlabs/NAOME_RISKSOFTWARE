# This is the boilerplate for database connections and configuration for the application

import psycopg2

try:
  connection = psycopg2.connect(database="naome_risk_db", user="postgres", password="password", host="localhost")
  print("Database connection successful")
except:
  print("DB connection failed")

curr = connection.cursor()

curr.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, num integer, data VARCHAR);")
curr.execute("INSERT INTO test (num, data) VALUES (%s, %s);", (100, "abc'def"))

connection.commit()
curr.close()
connection.close()
