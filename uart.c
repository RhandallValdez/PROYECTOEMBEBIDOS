#include "uart.h"
#define MAX_STR 50
#define BAUD 9600

//RHANDALL VALDEZ-P102
volatile unsigned char rx_buffer[MAX_STR] = {0};
volatile unsigned char current_size = 0;
bool isReady = false;

ISR(USART_RX_vect){
   unsigned char ch = UDR0;
   if( ch == '\r' || ch == '\n'){
     rx_buffer[current_size] = 0;
     isReady = true;
   }
   else if( ch == '\b' && current_size>0){
     rx_buffer[--current_size] = 0;
   }
   else{
     rx_buffer[current_size++] = ch;
   }
}

//Inicialización del módulo USART AVR modo asíncrono
//RHANDALL VALDEZ - P102
void serial_begin(){
	cli();
	float valor_UBBR0 = 0;
	UCSR0A=0b00000010;	//Bit 1 (U2X0) se pone en uno para duplicar la velocidad y poder utilizar frecuencias desde 1MHz.
	UCSR0B=0b10011000;	//Habilitar interrupcion por recepción / transmisión y recepción habilitados a 8 bits.
	UCSR0C=0b00000110;	//Así­ncrono, sin bit de paridad, 1 bit de parada a 8 bits.
	valor_UBBR0 = F_CPU/(16.0*BAUD);	
        if(UCSR0A & (1<<U2X0)) valor_UBBR0 *= 2;
	UBRR0=valor_UBBR0 - 1;
        sei();
}

//Recepción de datos 
unsigned char serial_read_char(){
	if(UCSR0A&(1<<7)){  //Si el bit7 del registro UCSR0A se ha puesto a 1.
		return UDR0;    //Devuelve el dato almacenado en el registro UDR0.
	}
	else
	return 0;//retorna 0
}

char* get_RX_buffer(){
   current_size = 0;
   isReady = false;
   return (char*)rx_buffer;
}

bool is_data_ready(){//informaci'on lista para recibir
   return isReady;
}

void serial_print_char(unsigned char caracter){
        if(caracter==0) return;
	while(!(UCSR0A&(1<<5)));    // mientras el registro UDR0 esté lleno espera
	UDR0 = caracter;            //cuando el el registro UDR0 está vacio se envia el caracter
}

void serial_print_str(char *cadena){	//cadena de caracteres de tipo char
	while(*cadena !=0x00){			//mientras el último valor de la cadena sea diferente
							        //al caracter nulo
		serial_print_char(*cadena);	//transmite los caracteres de cadena
		cadena++;				//incrementa la ubicación de los caracteres en cadena
								//para enviar el siguiente caracter de cadena
	}
}
void serial_println_str(char *cadena){
	serial_print_str(cadena);
	serial_print_char('\r');
	serial_print_char('\n');
}