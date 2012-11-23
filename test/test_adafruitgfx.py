import gaugette.ssd1306 as ssd1306
import fonts.arial_regular_10

ssd1306 = ssd1306.SSD1306()

ssd1306.draw_line(0,0,ssd1306.cols,ssd1306.rows,1)
ssd1306.draw_circle(16,16,12,1)
x = ssd1306.draw_text(30,0,"Test")
ssd1306.draw_text3(x,0,"Test", fonts.arial_regular_10)
ssd1306.dump_buffer()
