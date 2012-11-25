import gaugette.ssd1306 as ssd1306
import fonts.arial_regular_10

ssd1306 = ssd1306.SSD1306(buffer_rows=32, buffer_cols=128)

#ssd1306.draw_line(0,0,ssd1306.cols,ssd1306.rows,1)
#ssd1306.draw_circle(16,18,12,1)

#for i in range(0,16):
#    ssd1306.draw_fast_vline(i, i, ssd1306.buffer_rows-2*i)

#for i in range(0,16):
#    ssd1306.draw_fast_hline(i, i, ssd1306.buffer_cols-2*i)

ssd1306.draw_fast_vline(0, 0, 1)
ssd1306.fill_rect(110, 8, 3, 3, 1)

#for i in range(0,4):
#    ssd1306.draw_fast_hline(110, i, 10)
#    ssd1306.draw_fast_vline(120-i, 0, ssd1306.rows)

#x = ssd1306.draw_text(30,0,"Test")
#ssd1306.draw_text3(x,0,"Test", fonts.arial_regular_10)

ssd1306.dump_buffer()
