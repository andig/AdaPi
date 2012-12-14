import gaugette.ssd1306 as ssd1306
import fonts.arial_regular_10

ssd1306 = ssd1306.SSD1306(buffer_rows=32, buffer_cols=128)

#ssd1306.draw_line(0,0,ssd1306.cols,ssd1306.rows,1)
#ssd1306.draw_circle(16,18,12,1)

ssd1306.draw_fast_vline(64, 0, 15)

# border-line cases
y=3
dh=0
for i in range(0,8):
    ssd1306.draw_fast_vline(i, y+0, i+1+dh)
    ssd1306.draw_fast_vline(8+i, y+i, 8-i+dh)
    ssd1306.draw_fast_vline(16+i, i, 1)
    ssd1306.draw_fast_vline(24+i, i, 2)
    ssd1306.draw_fast_vline(32+i, i, 3)
    ssd1306.draw_fast_vline(48+i, i, 15-2*i)
    pass
    

#ssd1306.draw_fast_vline(1, 1, ssd1306.buffer_rows-2)
#ssd1306.draw_fast_vline(0, 0, ssd1306.buffer_rows)
#ssd1306.fill_rect(110, 8, 3, 3, 1)

#for i in range(0,4):
#    ssd1306.draw_fast_hline(110, i, 10)
#    ssd1306.draw_fast_vline(120-i, 0, ssd1306.rows)

#x = ssd1306.draw_text(30,0,"Test")
#ssd1306.draw_text3(x,0,"Test", fonts.arial_regular_10)

ssd1306.dump_buffer()
