#include <stdio.h>
#include <stdlib.h>

#include "generated/csr.h"

uint32_t value_sw, value_btn;

int main() {
  while(1) {
    //copy the value of sw on leds
    value_sw = switches_in_read();
    leds_out_write(value_sw);
    //btn
    value_btn = buttons_in_read();
    printf("valeur bouttons : %d\n",value_btn );
    switch(value_btn) {
      case 0:
      seven_seg_out_write(0x8387abf9ffA4);
        break;

      case 1:
      seven_seg_out_write(0x8387abf9ffff);
        break;

      case 2:
      seven_seg_out_write(0x8387abffffA4);
        break;

      default:
      seven_seg_out_write(0xC18888A18608);
        break;
    }
    //Gpio_out
    raspberry_out_write(0xffffffffffffffff);
  }
  return 0;
}
