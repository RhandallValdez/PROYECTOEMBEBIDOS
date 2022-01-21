# include <avr/io.h>
# include <stdio.h>
# include <stdlib.h>
#include <string.h>
#include "uart.h"
void configuracionesIniciales();
void recibirComandosAccionarSalidas(char* comando);
void enviarComandosARaspberry ();
void raspberry_comunicacion(char* instruccionesRaspberry);
void funcionamientoATMega();
