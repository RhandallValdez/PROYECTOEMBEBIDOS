#include "funciones.h" 
//RHANDALL VALDEZ - P102
//Modos a manejarse: Registro y acceso
//Desde Raspberry se mandan 2 n�meros hacia el ATMega en formato "xy"
// x representa el modo de operaci�n: 1 es registro y 2 es acceso
// y representa el estado de la operaci�n previamente realizada asociada al modo
// si y es 1 representa registro exitoso o acceso concedido
// si y es 0 representa registro fallido o acceso denegado
char *codigoTarjeta = "";
char *codigoAdicionalRegistro = "";
char *instruccionesRaspberry = "";
char *comandos = "";
 
void configuracionesIniciales(){
   //Configuraci�n de puertos.
   DDRC = 0b00011111;
   //Configuraci�n comunicaci�n serial con Raspberry.   
   //Configuraci�n para lectura de c�digo.
   serial_begin(); 
}

void recibirComandosAccionarSalidas(char* comando){
   if ((strcmp(comando,"11")) == 0){
      //Modo registro
      //Registro exitoso, se enciende led correspondiente.
      PORTC |= (1<<PC4);
      _delay_ms(1800);
      PORTC &= ~(1<<PC4); //Apagado de led. 
      //No se incluye caso de registro fallido ya que no existe un led asociado.
      //Led de registro permite al usuario saber si el registro fue exitoso.
      //Es un registro fallido si el dato de la primera tarjeta ingresada no tiene permisos.
   }
   else if ((strcmp(comando,"01")) == 0){
      //Modo acceso
      //Acceso concendido, se enciende led correspondiente y cerradura se energiza.
      //Tiempo de retardo es mayor a otros casos para permitir que se abra la puerta.
      PORTC |= (1<<PC0) | (1<<PC3);
      _delay_ms(3600);
      PORTC &= ~(1<<PC0) & ~(1<<PC3); //Apagado de led y cerradura desenergizada.
      }
   else if ((strcmp(comando,"00")) == 0){
      //Acceso denegado, se enciende led correspondiente.
      PORTC |= (1<<PC2);
      _delay_ms(1800);
      PORTC &= ~(1<<PC2); //Apagado de led. 
     }
}

void enviarComandosARaspberry (){
   //Leyendo estado de switch: presionado 1 - registro, sin presionar 0 - acceso.
   if(PINC & (1<<PC5)){ //Registro - 1
      //Receptar primero identificaci�n de administrador, luego tiempo de espera y luego se
      // recepta identificaci�n nueva a ingresar.
      //Se env�a c�digo de registro a Raspberry -0-, identificador administrador e identificador nuevo.
      //SE QUEMAN VALORES POR LIMITACIONES DE SIMULACI�N.
      PORTC |= (1<<PC1);
      instruccionesRaspberry = "1,QWERTY,RHAN";
      _delay_ms(3000);
      PORTC &= ~(1<<PC1);
     //C�DIGO ABAJO SE IMPLEMENTA EN PROTOTIPO, MAS NO EN SIMULACI�N
      /* while(!(is_data_ready())){} //Si no se lee alguna tarjeta se espera.Lectura tarjeta profesor.
      codigoTarjeta = get_RX_buffer();
      _delay_ms(250);
      strcat(instruccionesRaspberry, codigoTarjeta);
      strcat(instruccionesRaspberry, ",");
      while(!(is_data_ready())){} //Si no se lee alguna tarjeta se espera.Lectura tarjeta alumno.
      codigoAdicionalRegistro = get_RX_buffer();
      strcat(instruccionesRaspberry, codigoAdicionalRegistro);
      strcat(instruccionesRaspberry, ",");*/
   }
   else{//Acceso - 0
      //Receptar identificaci�n a verificar acceso.
      //Se env�a c�digo de acceso a Raspberry -1- e identificador le�do.
      //SE QUEMAN VALORES POR LIMITACIONES DE SIMULACI�N.
      instruccionesRaspberry = "0,PRUEBA1,";
      //C�DIGO ABAJO SE IMPLEMENTA EN PROTOTIPO, MAS NO EN SIMULACI�N
      /*while(!(is_data_ready())){} //Si no se lee alguna tarjeta se espera.Lectura tarjeta profesor.
      codigoTarjeta = get_RX_buffer();
      _delay_ms(250);
      strcat(instruccionesRaspberry, codigoTarjeta);
      strcat(instruccionesRaspberry, ",");*/
   }
}

void raspberry_comunicacion(char* instruccionesRaspberry){
   serial_println_str(instruccionesRaspberry);
   while (!(is_data_ready())){}
   comandos = get_RX_buffer();
}

void funcionamientoATMega(){
   enviarComandosARaspberry ();
   raspberry_comunicacion(instruccionesRaspberry);
   recibirComandosAccionarSalidas(comandos);
}