# -*- coding: latin-1 -*-

import time, random
import gaugette.ssd1306 as ssd1306

# fonts
import fonts.arial_regular_10
import fonts.ms_reference_sans_serif_regular_10
import fonts.calibri_regular_10
import fonts.arial_monospaced_for_sap_regular_10
import fonts.arial_monospaced_for_sap_regular_12
import fonts.arial_monospaced_for_sap_regular_14
import fonts.arial_monospaced_for_sap_regular_20

TITLE = "DAX"
X_INDEX = 127 - 2*5 - 1
DELAY = 0.01

# intialize display
ssd1306 = ssd1306.SSD1306_I2C(bus=1, device=0x3c)
ssd1306.begin()
ssd1306.clear_display()
TITLE_WIDTH = ssd1306.draw_text(0,0,TITLE)
ssd1306.display()

y = 16
t = time.time()

# running this be sure I2C speed is set as desired
# sudo modprobe -r i2c_bcm2708 && sudo modprobe i2c_bcm2708 baudrate=2000000
for i in range(0,128):
    # chart title
    if (i<TITLE_WIDTH): 
        ssd1306.draw_text(0,0,TITLE)
    
    # moving indicator
    ssd1306.draw_fast_vline(i,0,32,1)
    # transfer as little data as possible
    ssd1306.display_cols(max(i-1,0),min(2,128-i))

    # constant delay
    delay = t + DELAY - time.time()
    if (delay > 0):
        time.sleep(delay)
    t = time.time()

    # generate chart data
    y += random.randint(-1,1)
    y = min(max(y,0),31)
    
    # display actual value
    ssd1306.draw_text(X_INDEX,0,"{:2d}".format(y))
    ssd1306.display_cols(X_INDEX,128-X_INDEX-1)
    
    # clear moving indicator and print chart data
    ssd1306.draw_fast_vline(i,0,32,0)
    ssd1306.draw_pixel(i,y,1)
    
ssd1306.display()
