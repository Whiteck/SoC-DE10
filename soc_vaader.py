#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019 msloniewski <marcin.sloniewski@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

#Modified 2021 by Erwann Sourdin <sourdin.erwann@gmail.com>

import os
import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.build.io import DDROutput

from litex_boards.platforms import de10lite

from litex.soc.cores.clock import Max10PLL
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.video import VideoVGAPHY
from litex.soc.cores.led import LedChaser
from litex.soc.cores.timer import Timer 


from litedram.modules import IS42S16320
from litedram.phy import GENSDRPHY

from litex.soc.cores import gpio
from litex.soc.cores.spi import SPIMaster
from litex.soc.cores.bitbang import I2CMaster
from litex.soc.cores.pwm import PWM
from litex.soc.cores.timer import Timer
#import here new cores, if you want to add new hardware block


# CRG ----------------------------------------------------------------------------------------------
#This class create the clock use for the system
class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.rst = Signal()
        self.clock_domains.cd_sys    = ClockDomain()
        self.clock_domains.cd_sys_ps = ClockDomain(reset_less=True)
        self.clock_domains.cd_vga    = ClockDomain(reset_less=True)

        # # #

        # Clk / Rst
        clk50 = platform.request("clk50")

        # PLL
        self.submodules.pll = pll = Max10PLL(speedgrade="-7")
        self.comb += pll.reset.eq(self.rst)
        pll.register_clkin(clk50, 50e6)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        pll.create_clkout(self.cd_sys_ps, sys_clk_freq, phase=90)
        pll.create_clkout(self.cd_vga,    40e6)

        # SDRAM clock
        self.specials += DDROutput(1, 0, platform.request("sdram_clock"), ClockSignal("sys_ps"))

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(50e6), with_video_terminal=False, **kwargs):
        platform = de10lite.Platform()

        # SoCCore ----------------------------------------------------------------------------------
        #These kwargs overwrite the value find on soc / soc_core
        #So you can here the value of the different memory size
        kwargs["integrated_rom_size"] = 0x8000 # chose rom size (min = 0x6000)
        kwargs["integrated_sram_size"] = 0x2000 # chose sram size (min = 0x6000)
        kwargs["integrated_main_ram_size"] = 0 # chose Main ram size (min = depend of your personal firmware)




        SoCCore.__init__(self, platform, sys_clk_freq,
            ident          = "LiteX SoC on DE10-Lite",
            ident_version  = True,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)

        # SDR SDRAM --------------------------------------------------------------------------------
        #ADD the SDRAM if integrated_main_ram_size = 0
        if not self.integrated_main_ram_size:
            self.submodules.sdrphy = GENSDRPHY(platform.request("sdram"), sys_clk_freq)
            self.add_sdram("sdram",
                phy           = self.sdrphy,
                module        = IS42S16320(sys_clk_freq, "1:1"),
                l2_cache_size = kwargs.get("l2_size", 8192)
            )

        # Video Terminal ---------------------------------------------------------------------------
        #Add the VGA connector if enter --with-video-terminal argument during compilation (other arguments are --build --load)
        if with_video_terminal:
            self.submodules.videophy = VideoVGAPHY(platform.request("vga"), clock_domain="vga")
            self.add_video_terminal(phy=self.videophy, timings="800x600@60Hz", clock_domain="vga")

        # -------------------------------------------------------------------------------------
        #Inputs IO :

        # Switches
        user_switches = Cat(*[platform.request("user_sw", i) for i in range(10)])
        self.submodules.switches = gpio.GPIOIn(user_switches)
        self.add_csr("switches")

        # Buttons
        keys = Cat(*[platform.request("user_btn", i) for i in range(2)])
        self.submodules.keys = gpio.GPIOIn(keys)
        self.add_csr("keys")

        # -------------------------------------------------------------------------------------

        #Output IO : 

        # Leds
        user_leds = Cat(*[platform.request("user_led", i) for i in range(10)])
        self.submodules.leds = gpio.GPIOOut(user_leds)
        self.add_csr("user_leds")

        # seven_seg
        seven_seg = Cat(*[platform.request("seven_seg", i) for i in range(6)])
        self.submodules.seven_seg = gpio.GPIOOut(seven_seg)
        self.add_csr("seven segment")

        # -------------------------------------------------------------------------------------

        #Input/Output

        
        # GPIO type RASPBERRY
        
        #for making an input port : GPIOIn 
        #for making an output port : GPIOOut
          
        self.submodules.port_RA = gpio.GPIOOut(platform.request("port_RA"))
        self.add_csr("raspberry port A")
        
        self.submodules.port_RB = gpio.GPIOIn(platform.request("port_RB"))
        self.add_csr("raspberry port B")

        self.submodules.port_RC = gpio.GPIOIn(platform.request("port_RC"))
        self.add_csr("raspberry port C")

        # GPIO type ARDUINO
              
        self.submodules.port_A = gpio.GPIOIn(platform.request("port_A"))
        self.add_csr("arduino port A")

        self.submodules.port_B = gpio.GPIOOut(platform.request("port_B"))
        self.add_csr("arduino port B")
        
        # -------------------------------------------------------------------------------------

        #Communication buses

        # SPI
        def __init__(self, pads, data_width, sys_clk_freq, spi_clk_freq, with_csr=True, mode="raw"):
            self.submodules.spi0 = SPIMaster(platform.request("spi0"), 8, 50e6, 8e6)
            self.spi0.add_clk_divider()
            self.add_csr("spi0")

        # I2C
        self.submodules.i2c = I2CMaster(platform.request("i2c"))
        self.add_csr("i2c")

        # -------------------------------------------------------------------------------------

        #Oscillo 
        #ch 1 : system clock
        self.specials += DDROutput(1, 0, platform.request("oscillo_probe_1"), ClockSignal("sys"))
        #ch 2 : system clock send in a IO
        self.specials += DDROutput(1, 0, platform.request("oscillo_probe_2"), ClockSignal("sys_ps"))



        



# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on DE10-Lite")
    parser.add_argument("--build",               action="store_true", help="Build bitstream")
    parser.add_argument("--load",                action="store_true", help="Load bitstream")
    parser.add_argument("--sys-clk-freq",        default=50e6,        help="System clock frequency (default: 50MHz)")
    parser.add_argument("--with-video-terminal", action="store_true", help="Enable Video Terminal (VGA)")
    builder_args(parser)
    soc_core_args(parser)
    args = parser.parse_args()

    soc = BaseSoC(
        sys_clk_freq        = int(float(args.sys_clk_freq)),
        with_video_terminal = args.with_video_terminal,
        **soc_core_argdict(args)
    )
    builder = Builder(soc, **builder_argdict(args))
    builder.build(run=args.build)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".sof"))

if __name__ == "__main__":
    main()
