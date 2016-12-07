#!/usr/bin/python
#Dionnys Bonalde.
#email=dionnysb@gmail.com
#venezuela 2016.

import urllib, urlparse, string, time
import hashlib,binascii
import MySQLdb
#Datos de base de datos
DB_HOST = 'localhost' 
DB_USER = 'radius' 
DB_PASS = '3NsqxTUNcp@2'
DB_NAME = 'radius' 

# Open database connection
db = MySQLdb.connect(DB_HOST,DB_USER,DB_PASS,DB_NAME)

# prepare a cursor object using cursor() method
cursor = db.cursor()



#codigo de interacion

user= raw_input ("Usuario: ")
passwordhash= raw_input ("Password: ")

hash = hashlib.new('md4', (passwordhash).encode('utf-16le')).digest()
hash_convert=binascii.hexlify(hash)

print hash_convert

# Prepare SQL query to UPDATE required records

#sql = ("SELECT * FROM radcheck")

sql = ("UPDATE radcheck SET value=%s WHERE username=%s")



cursor.execute(sql,(hash_convert,user))



# print all the first cell of all the rows
#for row in cursor.fetchall():
 #   print row[1]

# disconnect from server
db.close()








