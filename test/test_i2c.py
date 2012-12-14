# -*- coding: latin-1 -*-

import gaugette.ssd1306 as ssd1306
import fonts.arial_regular_10
import fonts.ms_reference_sans_serif_regular_10
import fonts.calibri_regular_10
import fonts.arial_monospaced_for_sap_regular_10
import fonts.arial_monospaced_for_sap_regular_12
import fonts.arial_monospaced_for_sap_regular_14
import fonts.arial_monospaced_for_sap_regular_20
import time

ssd1306 = ssd1306.SSD1306_I2C(bus=1, device=0x3c)
ssd1306.begin()
ssd1306.clear_display()

x = ssd1306.draw_text(0,0,"Test")
ssd1306.draw_text3(x,0,"Test 26C", fonts.arial_monospaced_for_sap_regular_14)

ssd1306.display()

#ssd1306.startscrollright(0, 0xF)
#time.sleep(5)
#ssd1306.stopscroll()
