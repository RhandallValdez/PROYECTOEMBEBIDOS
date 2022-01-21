#PILCO-VALDEZ-P102
#Librerías requeridas

from wiringpi import Serial
import RPi.GPIO as GPIO
import ports

from firebase import firebase
import json

from funcionamiento import *

firebase = firebase.FirebaseApplication('https://proyectoembebidos-136aa-default-rtdb.firebaseio.com/', None)

baud = 9600
ser  = Serial("/dev/serial0",baud) 

TOKEN = "BBFF-dmmM41g9VgDX8QULDDjdKvnaMfR9mU"  # Token personal
DEVICE_LABEL = "Proyecto-Embebidos"  # Dispositivo registrado en Ubidots
VARIABLE_LABEL_1 = "AccesoPermitido"  # Nombre de variable de accesos permitidos
VARIABLE_LABEL_2 = "AccesoDenegado"  # Nombre de variable de accesos denegados
informacionRecibida = ""
informacionEnviada = ""
   
def main():
 funcionamientoContinuo(ser,firebase,TOKEN,DEVICE_LABEL,VARIABLE_LABEL_1,VARIABLE_LABEL_2)
 while (True):
  pass
  #funcionamientoContinuo() implementado en prototipo, simulación solo se necesita un envio para modificar desde atmega el código rfid a enviar
 
if __name__ == '__main__' :
   main()
