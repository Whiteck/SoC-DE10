#include <stdio.h>
#include <stdlib.h>
#include <irq.h>
#include <uart.h>
#include "delay.h"

#include "generated/csr.h"

uint32_t value_sw, value_btn;
void square_signal(double duty_cycle);


int main() {
  //Initialisation
  #ifdef CONFIG_CPU_HAS_INTERRUPT
	irq_setmask(0);
	irq_setie(1);
  #endif

  uart_init(); //uart_init() -> allways after init interrupt !!!
  //printf("Initialization Done\n");




  while(1) {
    value_sw = switches_in_read();
    leds_out_write(value_sw);

    square_signal(0.5);


    //btn
    value_btn = keys_in_read();
   
    switch(value_btn) {
      case 0:
      //both keys
      //display "btn1_2"
      seven_seg_out_write(0x8387abf9ffA4);
        break;

      case 1:
      //key 1 push
      //display "btn1__"
      seven_seg_out_write(0x8387abf9ffff);
        break;

      case 2:
      //key 0 push
      //display "btn__2"
      seven_seg_out_write(0x8387abffffA4);
        break;

      default:
      //no key push
      //display VAADER
      seven_seg_out_write(0xC18888A18608);
        break;
    }

    
  }
  return 0;
}


void square_signal(double duty_cycle) {
//Create a square signal
//Input is the duty cycle and time is the period in ms
//duty_cycle need to be between 0 and 1 
  uint8_t time = 40;
  uint8_t t_high = time * duty_cycle;
  uint8_t t_low = time * (1 - duty_cycle);
  port_RA_out_write(0x3);
  delay_ms(t_high);
  port_RA_out_write(0x0);
  delay_ms(t_low);
}
