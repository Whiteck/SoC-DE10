# SoC-DE10

A repo to test and implement Lite X on a DE10 lite. 

## Installation 

Copy soc_vaader.py into litex-boards/litex_boards/targets/

then make it executable :

> chmod a+x soc_vaader.py

Go to soc_cores, you find it in "litex/litex/soc/integration"
In this file, search the line "integrated_main_ram_size" and switch the value to 0x8000 (for 32KiB ram), 0x10000 (64KiB) or 0x20000 (128KiB)

## Compute

> cd litex-boards/litex_boards/targets/

> ./soc_vaader.py --build --load 

(don't forget to do a ./soc_vaader.py to check all possibilities)

## Export PATHs

You need to export these paths : 

>export SOC_DIRECTORY="/home/username/litex/litex/litex/soc"

>export BUILD_DIR="/home/username/litex/litex-boards/litex_boards/targets/build/terasic_de10lite"

## Upload firmware
Go to the firmware folder and use :

> make 

then you should find new files and "firmware.bin", to upload it, use lxterm :

> lxterm /dev/ttyUSB0 --kernel firmware.bin

and 

> reboot

Note : if you have an permition denied problem, use this command to give it and reboot : 

> usermod -a -G dialout username

## Play with IOs

After that, you will find the file "csr.h" in "build/terasic_de10lite/software/include/generated". It's an API to let you plays with IOs. 
At the begining, you can add some line in the main.c, like "leds_out_write(0x3ff);" to make IOs works
