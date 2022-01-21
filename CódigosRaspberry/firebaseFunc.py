from firebase import firebase
import json

def registroDatos(firebase,RFD1, RFD2): #Registro de estudiante en base de datos
   firebase.put("/estudiante", RFD2, RFD2) 


def consultaProfesor(firebase,RFID1): #Verifica si tarjeta ingresada se encuentra en lista de "profesor" en Firebase para permitir registro.
   leer = firebase.get('/profesor', RFID1)
   return leer

def consultaAlumno(firebase,RFID1):#Verifica si tarjeta ingresada se encuentra en lista de "estudiante" en Firebase para permitir acceso.
   leer_alum = firebase.get('/estudiante', RFID1)
   return  leer_alum
