# SoC-DE10

A repo to test and implement Lite X on a DE10 lite. 

## What you need : 

The board : a DE 10 lite in this example

A USB to UART (tx = IO8 | rx = IO9)

(optional) An Oscilloscope to look the square signal from the firmware

## Installation 

Copy soc_vaader.py into litex-boards/litex_boards/targets/

Copy terasic_de10lite.py into litex-boards/litex_boards/platforms/

then make it executable :

> chmod a+x soc_vaader.py

Then in soc_vaader.py, search the line "integrated_main_ram_size" and switch the value between : 0x2000 (for 8KiB ram) and 0x20000 (128KiB)

## Compute

> cd litex-boards/litex_boards/targets/

> ./soc_vaader.py --build --load 

(don't forget to do a ./soc_vaader.py --help to check all possibilities)

## Export PATHs

You need to export these paths : 

>export SOC_DIRECTORY="/home/username/litex/litex/litex/soc"

>export BUILD_DIR="/home/username/litex/litex-boards/litex_boards/targets/build/terasic_de10lite"
>
## The firmware

The firmware given will : 

-> display "VAADER" or which buttons you are pushing

-> Recopy switchs value to leds

-> Create a square signal on the first pin to raspberry GPIOs

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

