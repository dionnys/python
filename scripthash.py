#!/usr/bin/python
#Dionnys Bonalde
#coding: utf-8
import urllib, urlparse, string, time
import hashlib,binascii
import os, sys,random,itertools
import MySQLdb

#Datos de base de datos
DB_HOST = 'localhost'
DB_USER = 'radius'
DB_PASS = '3NsqxTUNcp@2'
DB_NAME = 'radius'

#Establecemos la conexion con la base de datos
db = MySQLdb.connect(DB_HOST,DB_USER,DB_PASS,DB_NAME)

#Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cursor = db.cursor()

#Funciones:

def ingreso():
	print "***VPN- Ingreso de Usuario-***"
	user= raw_input ("Usuario: ")
	passwordhash= raw_input ("Password: ")
	hash=hashlib.new('md4', (passwordhash).encode('utf-16le')).digest()
	hashntlm=binascii.hexlify(hash)
	attributo="NT-Password"
	estatus=":="
	sql = ("INSERT radcheck SET username=%s,attribute=%s,op=%s,value=%s")
	cursor.execute(sql,(user,attributo,estatus,hashntlm))
	# disconnect from server
	db.close()
	print "Usuario Ingresado ....!!!"
	return

def updateclave():
	print "***VPN- Cambio De Clave -***"
	user= raw_input ("Usuario: ")
	passwordhash= raw_input ("Password: ")
	hash=hashlib.new('md4', (passwordhash).encode('utf-16le')).digest()
	hashntlm=binascii.hexlify(hash)
	sql = ("UPDATE radcheck SET value=%s WHERE username=%s")
	cursor.execute(sql,(hashntlm,user))
	# disconnect from server
	db.close()
	print "Clave Actualizada ....!!!"
	return


def borrar():
	print "***VPN- Borrar Usuario-***"
	user= raw_input ("Usuario: ")
	sql = ("DELETE FROM radcheck WHERE username=%s")
	cursor.execute(sql,(user))
	
	# disconnect from server
	db.close()

	print "Usuario Borrado....!!!"
	return

def listar():
	sql = ("SELECT * FROM radcheck")
	cursor.execute(sql)
	# print all the first cell of all the rows
	for row in cursor.fetchall():
		print row
	# disconnect from server
	db.close()
	return

print"***VPN- Gestion de Usuarios"

x=raw_input ("Opcion: (n) Nuevo, (c) Cambio de Clave (b) Borrar (l)listar: ")
if x == 'n':
	ingreso()
elif x == 'c':
	updateclave()
elif x == 'b':
	borrar()
elif x == 'l':
	listar()
else:
	print 'Opcion Invalida'


