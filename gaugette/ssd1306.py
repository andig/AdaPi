#----------------------------------------------------------------------
# ssd1306.py from https://github.com/guyc/py-gaugette
# ported by Guy Carpenter, Clearwater Software
#
# This library is for the Adafruit 128x32 SPI monochrome OLED 
# based on the SSD1306 driver.
#   http://www.adafruit.com/products/661
#
# This library does not directly support the larger 128x64 module,
# but could with minor changes.
#
# The code is based heavily on Adafruit's Arduino library
#   https://github.com/adafruit/Adafruit_SSD1306
# written by Limor Fried/Ladyada for Adafruit Industries.
#
# The datasheet for the SSD1306 is available
#   http://www.adafruit.com/datasheets/SSD1306.pdf
#
# WiringPi pinout reference
#   https://projects.drogon.net/raspberry-pi/wiringpi/pins/
#
# Some important things to know about this device and SPI:
#
# - The SPI interface has no MISO connection.  It is write-only.
#
# - The spidev xfer and xfer2 calls overwrite the output buffer
#   with the bytes read back in during the SPI transfer.
#   Use writebytes instead of xfer to avoid having your buffer overwritten.
#
# - The D/C (Data/Command) line is used to distinguish data writes
#   and command writes - HIGH for data, LOW for commands.  To be clear,
#   the attribute bytes following a command opcode are NOT considered data,
#   data in this case refers only to the display memory buffer.
#   keep D/C LOW for the command byte including any following argument bytes.
#   Pull D/C HIGH only when writting to the display memory buffer.
#   
# - The pin connections between the Raspberry Pi and OLED module are:
#
#      RPi     SSD1306
#      CE0   -> CS
#      GPIO2 -> RST   (to use a different GPIO set reset_pin to wiringPi pin no)
#      GPIO1 -> D/C   (to use a different GPIO set dc_pin to wiringPi pin no)
#      SCLK  -> CLK
#      MOSI  -> DATA
#      3.3V  -> VIN
#            -> 3.3Vo
#      GND   -> GND
#----------------------------------------------------------------------

#import spidev
#import wiringpi
#import time
#import sys

import font5x8
import adafruit.adafruitgfx as adafruitgfx

class SSD1306(adafruitgfx.AdafruitGFX):

    # Class constants are externally accessible as gaugette.ssd1306.SSD1306.CONST
    # or my_instance.CONST

    # TODO - insert underscores to rationalize constant names

    EXTERNAL_VCC   = 0x1
    SWITCH_CAP_VCC = 0x2
        
    SET_LOW_COLUMN        = 0x00
    SET_HIGH_COLUMN       = 0x10
    SET_MEMORY_MODE       = 0x20
    SET_COL_ADDRESS       = 0x21
    SET_PAGE_ADDRESS      = 0x22
    RIGHT_HORIZ_SCROLL    = 0x26
    LEFT_HORIZ_SCROLL     = 0x27
    VERT_AND_RIGHT_HORIZ_SCROLL = 0x29
    VERT_AND_LEFT_HORIZ_SCROLL = 0x2A
    DEACTIVATE_SCROLL     = 0x2E
    ACTIVATE_SCROLL       = 0x2F
    SET_START_LINE        = 0x40
    SET_CONTRAST          = 0x81
    CHARGE_PUMP           = 0x8D
    SEG_REMAP             = 0xA0
    SET_VERT_SCROLL_AREA  = 0xA3
    DISPLAY_ALL_ON_RESUME = 0xA4
    DISPLAY_ALL_ON        = 0xA5
    NORMAL_DISPLAY        = 0xA6
    INVERT_DISPLAY        = 0xA7
    DISPLAY_OFF           = 0xAE
    DISPLAY_ON            = 0xAF
    COM_SCAN_INC          = 0xC0
    COM_SCAN_DEC          = 0xC8
    SET_DISPLAY_OFFSET    = 0xD3
    SET_COM_PINS          = 0xDA
    SET_VCOM_DETECT       = 0xDB
    SET_DISPLAY_CLOCK_DIV = 0xD5
    SET_PRECHARGE         = 0xD9
    SET_MULTIPLEX         = 0xA8

    MEMORY_MODE_HORIZ = 0x00
    MEMORY_MODE_VERT  = 0x01
    MEMORY_MODE_PAGE  = 0x02

    # Device name will be /dev/spidev-{bus}.{device}
    # dc_pin is the data/commmand pin.  This line is HIGH for data, LOW for command.
    # We will keep d/c low and bump it high only for commands with data
    # reset is normally HIGH, and pulled LOW to reset the display

    def __init__(self, bus=0, device=0, dc_pin=1, reset_pin=2, buffer_rows=64, buffer_cols=128):
        self.cols = 128
        self.rows = 32
        self.dc_pin = dc_pin
        self.reset_pin = reset_pin
#        self.spi = spidev.SpiDev()
#        self.spi.open(bus, device)
#        self.spi.max_speed_hz = 500000
#        self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
#        self.gpio.pinMode(self.reset_pin, self.gpio.OUTPUT)
#        self.gpio.digitalWrite(self.reset_pin, self.gpio.HIGH)
#        self.gpio.pinMode(self.dc_pin, self.gpio.OUTPUT)
#        self.gpio.digitalWrite(self.dc_pin, self.gpio.LOW)
        self.font = font5x8.Font5x8
        self.buffer_rows = buffer_rows
        self.buffer_cols = buffer_cols
        self.col_offset = 0
        self.bytes_per_col = buffer_rows / 8
        self.mem_bytes = self.rows * self.cols * 2 / 8 # total bytes in SSD1306 display ram
        self.buffer = [0] * (self.buffer_cols * self.bytes_per_col)
        
        super(SSD1306, self).__init__(self.cols, self.rows)

#    def reset(self):
#        self.gpio.digitalWrite(self.reset_pin, self.gpio.LOW)
#        self.gpio.delay(10) # 10ms
#        self.gpio.digitalWrite(self.reset_pin, self.gpio.HIGH)
#
#    def command(self, *bytes):
#        # already low
#        # self.gpio.digitalWrite(self.dc_pin, self.gpio.LOW) 
#        self.spi.writebytes(list(bytes))
#
#    def data(self, bytes):
#        self.gpio.digitalWrite(self.dc_pin, self.gpio.HIGH)
#        self.spi.writebytes(bytes)
#        self.gpio.digitalWrite(self.dc_pin, self.gpio.LOW)
#        
#    def begin(self, vcc_state = SWITCH_CAP_VCC):
#        self.gpio.delay(1) # 1ms
#        self.reset()
#        self.command(self.DISPLAY_OFF)
#        self.command(self.SET_DISPLAY_CLOCK_DIV, 0x80)
#        self.command(self.SET_MULTIPLEX, 0x1F)
#        self.command(self.SET_DISPLAY_OFFSET, 0x00)
#        self.command(self.SET_START_LINE | 0x00)
#        if (vcc_state == self.EXTERNAL_VCC):
#            self.command(self.CHARGE_PUMP, 0x10)
#        else:
#            self.command(self.CHARGE_PUMP, 0x14)
#        self.command(self.SET_MEMORY_MODE, 0x00)
#        self.command(self.SEG_REMAP | 0x01)
#        self.command(self.COM_SCAN_DEC)
#        self.command(self.SET_COM_PINS, 0x02)
#        self.command(self.SET_CONTRAST, 0x8f)
#        if (vcc_state == self.EXTERNAL_VCC):
#            self.command(self.SET_PRECHARGE, 0x22)
#        else:
#            self.command(self.SET_PRECHARGE, 0xF1)
#        self.command(self.SET_VCOM_DETECT, 0x40)
#        self.command(self.DISPLAY_ALL_ON_RESUME)
#        self.command(self.NORMAL_DISPLAY)
#        self.command(self.DISPLAY_ON)
        
    def clear_display(self):
        for i in range(0,len(self.buffer)):
            self.buffer[i] = 0

    def invert_display(self):
        self.command(self.INVERT_DISPLAY)

    def normal_display(self):
        self.command(self.NORMAL_DISPLAY)

    def display(self):
        self.command(self.SET_MEMORY_MODE, self.MEMORY_MODE_VERT)
        self.command(self.SET_COL_ADDRESS, 0, 127)
        start = self.col_offset * self.bytes_per_col
        length = self.mem_bytes # automatically trucated if few bytes available in self.buffer
        self.data(self.buffer[start:start+length])

    def display_cols(self, start_col, count):
        self.command(self.SET_MEMORY_MODE, self.MEMORY_MODE_VERT)
        self.command(self.SET_COL_ADDRESS, start_col, (start_col + count) % self.cols)
        start = (self.col_offset + start_col) * self.bytes_per_col
        length = count * self.bytes_per_col
        self.data(self.buffer[start:start+length])


    # Diagnostic print of the memory buffer to stdout
    def dump_buffer(self):
        for y in range(0, self.buffer_rows):
            mem_row = y/8
            bit_mask = 1 << (y % 8)
            line = ""
            for x in range(0, self.buffer_cols):
                mem_col = x
                offset = mem_row + self.buffer_rows/8 * mem_col
                if self.buffer[offset] & bit_mask:
                    line += '*'
                else:
                    line += ' '
            print('|'+line+'|')
            
    # Pixels are stored in column-major order!
    # This makes it easy to reference a vertical slice of the display buffer
    # and we use the to achieve reasonable performance vertical scrolling 
    # without hardware support.
    # 
    #  If the self.buffer_rows = 64, then the bytes are arranged on
    #  the screen like this:
    #
    #  0  8 ...
    #  1  9
    #  2 10
    #  3 11
    #  4 12
    #  5 13
    #  6 14
    #  7 15
    #
    
    def draw_pixel(self, x, y, on=True):
        if (x<0 or x>=self.buffer_cols or y<0 or y>=self.buffer_rows):
            return
        mem_col = x
        mem_row = y / 8
        bit_mask = 1 << (y % 8)
        offset = mem_row + self.buffer_rows/8 * mem_col

        if on:
            self.buffer[offset] |= bit_mask
        else:
            self.buffer[offset] &= (0xFF - bit_mask)
 

    # overwritten from adafruitgfx
    def draw_fast_vline(self, x, y, h, color=1):
        if (x<0 or x>=self.buffer_cols or y<0 or y+h>self.buffer_rows):
            return
        if (h<8):
            self.draw_line(x, y, x, y+h-1, color)
            return

        mem_row_start = y / 8
        mem_row_end = (y+h) / 8
        x *= self.buffer_rows/8
        
        # line start
        bit_mask = (0xff << (y % 8)) & 0xff
        offset = mem_row_start + x

        if color:
            self.buffer[offset] |= bit_mask
        else:
            self.buffer[offset] &= (0xFF - bit_mask)

        # line end
        b = 8 - (y+h) % 8
        bit_mask = 0xff >> (8 - (y+h) % 8)
        offset = mem_row_end + x

        if color:
            self.buffer[offset] |= bit_mask
        else:
            self.buffer[offset] &= (0xFF - bit_mask)
        
        # line middle
        for y in range(mem_row_start+1, mem_row_end):
            offset = y + x
            if color:
                self.buffer[offset] = 0xFF
            else:
                self.buffer[offset] = 0


    # overwritten from adafruitgfx
    def draw_fast_hline(self, x, y, w, color=1):
        # stupidest version - update in subclasses if desired!
        if (x<0 or x+w>self.buffer_cols or y<0 or y>=self.buffer_rows):
            return
        mem_row = y / 8
        bit_mask = 1 << (y % 8)

        for offset in range(mem_row + self.buffer_rows/8 * x, mem_row + self.buffer_rows/8 * (x+w), self.buffer_rows/8):            
            if color:
                self.buffer[offset] |= bit_mask
            else:
                self.buffer[offset] &= (0xFF - bit_mask)
            

    # use fillrect instead
    def clear_block(self, x0,y0,dx,dy):
        fill_rect(x0,y0,dx,dy,0)
