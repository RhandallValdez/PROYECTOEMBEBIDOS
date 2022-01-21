import firebase
import cv2 as cv
import os
from datetime import datetime
import PrintList
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

from ubidotsFunc import*
from serial import *
from firebaseFunc import*

def tomarImagen(): #FUNCION A IMPLEMENTAR EN PROTOTIPO, NO UTILIZADA EN SIMULACIÓN
 video_capture = cv.VideoCapture(0) #Captura imagen
 ret, frame = video_capture.read()
 now = datetime.now() #Fecha y hora
 dt_string = now.strftime("%d/%m/%Y %H:%M:%S")#Formato de string fecha y hora
 direccion = r'C:\FotosProyectoEmbebidos'
 os.chdir(direccion) #Acceso a dirección establecida
 filename = "fotoEnviar" +dt_string+".png" #Nombre archivo
 cv.imwrite(filename, frame) #Escritura en ruta de imagen
# Close device
 video_capture.release()
 return rutaImagen
 
def enviarCorreo(): 
  img_data = open('C:/7mo semestre/espol.png', 'rb').read()
  #video_capture = cv.VideoCapture(0) #Captura imagen, NO USADO EN SIMULACION
  #ret, frame = video_capture.read()
 # video_capture.release()
  mailServer = smtplib.SMTP('smtp.gmail.com',587)
  print(mailServer.ehlo())
  print(mailServer.starttls())
  print(mailServer.ehlo())
  now = datetime.now()
  date = now.strftime("%m/%d/%Y")#Se obtiene día.
  time = now.strftime("%H:%M:%S")#Se obtiene hora.
  mailServer.login("embebidosproyecto@gmail.com","proyecEmbebidos1")
  # Construimos el mensaje simple para el correo
  mensaje = MIMEMultipart()
  texto = MIMEText("""Una persona no autorizada esta intentando ingresar al laboratorio el dia """ + date+""" a las """ + time)
  mensaje.attach(texto) 
  mensaje['From']="embebidosproyecto@gmail.com"#Correo emisor
  mensaje['To']="rhakvald@espol.edu.ec"#Correo receptor
  mensaje['Subject']="Persona no autorizada intenta acceder al laboratorio"#Asunto del correo
  image = MIMEImage(img_data, name=os.path.basename("C:/7mo semestre/espol.png"))
  mensaje.attach(image)#Se añade imagen al correo
  # Envio del mensaje
  mailServer.sendmail("embebidosproyecto@gmail.com", "rhakvald@espol.edu.ec", mensaje.as_string()) 
		
		
def atMEGA_Raspberry(cadenaInstrucciones,firebase,TOKEN,DEVICE_LABEL,VARIABLE_LABEL_1,VARIABLE_LABEL_2):
   listString = cadenaInstrucciones.split(",") #Mensaje desde ATMega se envía en formato MODOENVIO, RFID1, RFID2
   #RFID2 NO SE UTILIZA PARA MODO DE ACCESO PERO SE CONFIGURÓ PARA QUE IGUAL ADMITA UN VALOR NULO LA TRANSMISIÓN DEL MENSAJE
   modoEnvio = listString[0] 
   codigoRFID1 = listString[1] 
   codigoRFID2 = listString[2] 
   stringRetorno = modoEnvio
   if (modoEnvio == "0"):
      #Consulta a base de datos; se activa cámara y se envía correo si se niega acceso.
      accesoPermitido = True
      if((consultaAlumno(firebase,codigoRFID1) == None) and (consultaProfesor(firebase,codigoRFID1) == None)): #Si no está en registro de estudiantes o profesores se niega el acceso.
       enviarCorreo()
       accesoPermitido = False

      if accesoPermitido:#Solo se debe notificar a atMEGA que se admite acceso para que realice acciones pertinentes.
       stringRetorno+="1"
      else:
       stringRetorno+="0"
      send_Ubidots(TOKEN,DEVICE_LABEL,VARIABLE_LABEL_1, VARIABLE_LABEL_2,accesoPermitido) #Envío de datos a Ubidots
   elif (modoEnvio == "1"):
    registroExitoso = False
    if(consultaProfesor(firebase,codigoRFID1) == codigoRFID1):#Si código RFID1 tiene permisos de profesor
     registroDatos(firebase,codigoRFID1, codigoRFID2) #Se registra al estudiante
     registroExitoso = True

    stringRetorno += "1" if registroExitoso else "0"
   print(stringRetorno)
   return stringRetorno

def funcionamientoContinuo(ser,firebase,TOKEN,DEVICE_LABEL,VARIABLE_LABEL_1,VARIABLE_LABEL_2):
   while (ser.dataAvail() <= 0):
      pass
   informacionRecibida = recibir(ser)
   informacionEnviada = atMEGA_Raspberry(informacionRecibida,firebase,TOKEN,DEVICE_LABEL,VARIABLE_LABEL_1,VARIABLE_LABEL_2)
   printsln(informacionEnviada,ser)
   
