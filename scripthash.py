#!/usr/bin/python
# -*- coding: iso-8859-1-*-
###########################################################
#
# Este script de python  es usado para destinonar una base 
# de datos Radius de un servicio VPN
# 
#
# Written by : Dionnys Bonalde.
# Created date: Dec 12, 2016
# Last modified: Dec 13, 2016
# Tested with : Python 2.6.6
# Script Revision: 1.1
#
##########################################################


import urllib, urlparse,string,time,datetime
import hashlib,binascii,getopt,tabulate
import os, sys,random,itertools
import MySQLdb

#Datos de base de datos
execfile("/root/python/.config.py")





#Establecemos la conexion con la base de datos
db = MySQLdb.connect(DB_HOST,DB_USER,DB_USER_PASSWORD,DB_NAME)

#Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cursor = db.cursor()

#Funciones:

def ingreso():
	print "***VPN- Ingreso de Usuario-***"
	user= raw_input ("Usuario: ")
	

	sqlu = ("SELECT username FROM radcheck WHERE username=%s")
	cursor.execute(sqlu,user)
	data=cursor.fetchall()
	if len(data)==1:
		print "El Usuario ya Existe."
	else:
		passwordhash= raw_input ("Password: ")
		hash=hashlib.new('md4', (passwordhash).encode('utf-16le')).digest()
		hashntlm=binascii.hexlify(hash)
		attributo="NT-Password"
		estatus=":="
		sql = ("INSERT radcheck SET username=%s,attribute=%s,op=%s,value=%s")
		cursor.execute(sql,(user,attributo,estatus,hashntlm))
		# disconnect from server
		db.close()
		print "El usuario ha sido creado. !!!"
	return
	

def updateclave():
	print "***VPN- Cambio De Contraseña -***"
	user= raw_input ("Usuario: ")
	sqlu = ("SELECT username FROM radcheck WHERE username=%s")
	cursor.execute(sqlu,user)
	data=cursor.fetchall()
	if len(data)==0:
		print "El Usuario no existe."
	else:
		passwordhash= raw_input ("Password: ")
		hash=hashlib.new('md4', (passwordhash).encode('utf-16le')).digest()
		hashntlm=binascii.hexlify(hash)
		sqlu = ("SELECT value FROM radcheck WHERE value=%s")
		cursor.execute(sqlu,hashntlm)
		data=cursor.fetchall()
	if len(data)==1:
		print "La Contraseña ya estaba registrada "
	else:
		sql = ("UPDATE radcheck SET value=%s WHERE username=%s")
		cursor.execute(sql,(hashntlm,user))
		# disconnect from server
		db.close()
		print "La contraseña ha sido actualizada.	!!!"
	return


def borrar():
	print "***VPN- Borrar Usuario -***"
	user= raw_input ("Usuario: ")
	sqlu = ("SELECT username FROM radcheck WHERE username=%s")
	cursor.execute(sqlu,user)
	data=cursor.fetchall()
	if len(data)==0:
		print "El usuario no existe."
	else:
		sql = ("DELETE FROM radcheck WHERE username=%s")
		cursor.execute(sql,(user))
		
		# disconnect from server
		db.close()

		print "El usuario ha sido borrado. !!!"
	return


def despurar():
	sql = ("SELECT * FROM radcheck")
	cursor.execute(sql)
	# print all the first cell of all the rows
	row=cursor.fetchall()
	from tabulate import tabulate
	print tabulate ((row),("id","username","attribute","op","value"))
	# disconnect from server
	db.close()
	return


def backup():

	execfile("/root/python/backup.py")

	return


print"***VPN- Gestión de Usuarios -***"

x=raw_input ("Opción: Crear Usuario(n) Cambiar Contraseña(c) Borrar Usuario(b) Depurar(D): ")
if x == 'n' or x == 'N':
	ingreso()
elif x == 'c' or x == 'C':
	updateclave()
elif x == 'b' or x == 'B':
	borrar()
elif x == 'D':
	despurar()
elif x == 'k':
	backup()
	
else:
	print 'La opción es invalida.'
