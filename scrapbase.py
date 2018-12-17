#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
import csv
import requests
import json, lxml
import argparse
import urllib
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')

class Dato:
	def __init__(self):
		self.id            = 0
		self.nombres       = ''
		self.apellidos     = ''
		self.direccion     = ''
		self.codigo_postal = ''
		self.ciudad        = ''
		self.provincia     = ''
		self.zona          = ''
		self.telefono      = ''

	def getNombreCampos(self):
		return ["Nombres", "Apellidos", "Direccion", "Codigo_postal", "Ciudad", "Provincia", "Zona", "Teléfono" ]

	def getRow(self):
		return[self.nombres, self.apellidos, self.direccion, self.codigo_postal, self.ciudad, self.provincia, self.zona, self.telefono ]

class CSVManager:
	def __init__(self,na,en):
		self.nombre_archivo = na
		self.encabezado     = en
		archivo_existe      = os.path.isfile(self.nombre_archivo)

		with open(self.nombre_archivo, 'a') as myfile:
			self.archivo = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			if not archivo_existe:
				self.archivo.writerow(self.encabezado)

	def write(self,r):
		self.archivo.writerow(r)

class SessionManager:
	def __init__(self):
		self.session = requests.session()

	def get(self,u):
		return self.session.get(u)

class Scrap:
	def __init__(self):
		self.busqueda_nombre   = ''
		self.busqueda_apellido = ''
		self.provincia         = ''
		self.ciudad            = ''
		self.CSV_manager       = ''
		self.errors            = ''

		self.provincias   = []
		self.url_busqueda = ''
		self.sesionMNG    = SessionManager()

		self.pagina         = 1
		self.cont_registros = 1

	def iniciar(self):
		if not self.datosValidos():
			print(self.errors)
			return False

		print('')
		print('Consultando en página: '+str(self.pagina) )
		resp = self.sesionMNG.get( '' ) # Peticion para obtener las cookies
		print(self.getUrlBusqueda())
		resp = self.sesionMNG.get( self.getUrlBusqueda() )

		print("respuesta estado: "+str(resp.status_code) )

		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content,"lxml")
			self.procesarPagina(soup)

	def procesarPagina(self,html):
		registros = html.find('div',{'id':'PPAL'})
		print(registros)
		for reg in registros:
			print('--> Obteniendo informacion persona id:  Pagina: '+str(self.pagina)+' | Registro número: '+str(self.cont_registros))
			self.cont_registros += 1

			dato = Dato()
			#dato.telefono =
			print(reg)

	def getUrlBusqueda(self):
		salida = self.url_busqueda + 'no='+urllib.quote(self.busqueda_nombre)
		if self.busqueda_apellido != '':
			salida += '&ap1=' + urllib.quote(self.busqueda_apellido)

		salida += '&sec='+urllib.quote(self.provincia)
		if self.ciudad != '':
			salida += 'lo='+urllib.quote(self.ciudad)
		salida += '&pgpv=1&tbus=0&nomprov='+urllib.quote(self.provincias.getText(self.provincia))+'&idioma=spa'

		return salida

	def datosValidos(self):
		if self.busqueda_nombre == '':
			self.errors = 'Es necesario especificar el nombre'
			return False

		if self.provincia == '':
			self.errors = 'Es necesario especificar una provincia'
			return False

		return True

# Carga de parametros
parser = argparse.ArgumentParser()

parser.add_argument("-n", "--nombre", help="Nombre de busqueda")
parser.add_argument("-a", "--apellido", help="Apellido de busqueda")
parser.add_argument("-p", "--provincia", help="Codigo de provincia busqueda")
parser.add_argument("-c", "--ciudad", help="Nombre de ciudad")
parser.add_argument("-w", "--archivo", help="Ruta del archivo .CSV para guardar resultados")

args = parser.parse_args()

# Inicializacion del scraper con los parametros cargados
scrap = Scrap()

if args.nombre:
	scrap.busqueda_nombre = args.nombre

if args.apellido:
	scrap.busqueda_apellido = args.apellido

if args.archivo:
	a_salida_CSV = args.archivo
else:
	print('Es necesario especificar un archivo de archivo de salida, con el parametro -w, o --archivo')

if args.provincia:
	scrap.provincia = args.provincia

if args.ciudad:
	scrap.ciudad = args.ciudad

class Provincias:
	def __init__(self):
		self.provincias = [
		
		]

	def getText(self,cod):
		for p in self.provincias:
			if p["cod"] == str(cod):
				return p["t"]

scrap.provincias  = Provincias()
scrap.CSV_manager = CSVManager(a_salida_CSV, Dato().getNombreCampos())

scrap.iniciar()
