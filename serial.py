from time import sleep

def recibir(ser): #Recibe mensaje de ATmega por serial hasta recibir \r -retorno de carro-.
 data = ""
 while True:
  input = ser.getchar()
  if input == "\r":
   return (data)
  data += input
 sleep(0.2)

def printsln(menss,ser): #Manda mensaje por serial caracter por caracter
 for c in menss:
  ser.putchar(c)
  sleep(0.001)
 ser.putchar("\r")
 sleep(0.001)
