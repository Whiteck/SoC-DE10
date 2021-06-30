# SoC-DE10

A repo to test and implement Lite X on a DE10 lite. 

## Installation 

Copy soc_vaader.py into litex-boards/litex_boards/targets/

then make it executable :

chmod a+x soc_vaader.py

## Compute

cd litex-boards/litex_boards/targets/
./soc_vaader.py --build --load 

(don't forget to do a ./soc_vaader.py to check all possibilities)

## Play with IO

After that, you will find the file "csr.h" in "build/terasic_de10lite/software/include/generated". It's an API to let you plays with IOs. 
