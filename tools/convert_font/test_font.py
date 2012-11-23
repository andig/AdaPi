import sys, glob, re
sys.path.insert(0, './fonts')

import arial_monospaced_for_sap_regular_10
import arial_monospaced_for_sap_regular_12
import arial_monospaced_for_sap_regular_14
import arial_monospaced_for_sap_regular_20
import arial_regular_10
import arial_regular_12
import arial_regular_14
import arial_regular_20
import calibri_regular_10
import calibri_regular_12
import calibri_regular_14
import calibri_regular_20
import lucida_console_regular_10
import lucida_console_regular_12
import lucida_console_regular_14
import lucida_console_regular_20
import lucida_sans_regular_10
import lucida_sans_regular_12
import lucida_sans_regular_14
import lucida_sans_regular_20
import ms_reference_sans_serif_regular_10
import ms_reference_sans_serif_regular_12
import ms_reference_sans_serif_regular_14
import ms_reference_sans_serif_regular_20
import polo_regular_10
import polo_regular_12
import polo_regular_14
import polo_regular_20
import segoe_print_regular_10
import segoe_print_regular_12
import segoe_print_regular_14
import segoe_print_regular_20
import tahoma_regular_10
import tahoma_regular_12
import tahoma_regular_14
import tahoma_regular_20

# Debugging version of the OLED class from py-gaugette
class SSD1306:

    def __init__(self, bus=0, device=0, dc_pin=1, reset_pin=2, buffer_rows=64, buffer_cols=128):
        self.cols = 128
        self.rows = 32
        self.buffer_rows = buffer_rows
        self.buffer_cols = buffer_cols
        self.buffer = [0] * (self.buffer_cols * self.buffer_rows)
        
    def draw_pixel(self, px,py,c):
#        print(px,py,c)
        self.buffer[py*self.buffer_cols+px] = c
        
    def clear_buffer(self):
        for i in range(0, len(self.buffer)):
            self.buffer[i] = 0
        
    def show_buffer(self):
        map = [' ', '*']
        for y in range(0, self.buffer_rows):
            print(''.join([map[char] for char in self.buffer[y*self.buffer_cols : (y+1)*self.buffer_cols]]))
            
    def draw_text3(self, x, y, string, font):
        height = font.char_height
        prev_char = None

        for c in string:
 #           print("Char "+c+" Prev "+str(prev_char))
            if (c<font.start_char or c>font.end_char):
                if prev_char != None:
                    x += font.space_width + prev_width + font.gap_width
                prev_char = None
            else:
                pos = ord(c) - ord(font.start_char)
                (width,offset) = font.descriptors[pos]
#                print("Width: "+str(width))

                if prev_char != None:
                    x += font.kerning[prev_char][pos] + font.gap_width
#                    print("Kern: "+str(font.kerning[prev_char][pos]))
                    
                prev_char = pos
                prev_width = width
                
                bytes_per_row = (width + 7) / 8
                for row in range(0,height):
                    py = y + row
                    mask = 0x80
                    p = offset
                    for col in range(0,width):
                        px = x + col
                        if (font.bitmaps[p] & mask):
                            self.draw_pixel(px,py,1)  # for kerning, never draw black
                        mask >>= 1
                        if mask == 0:
                            mask = 0x80
                            p+=1
                    offset += bytes_per_row
          
        if prev_char != None:
            x += prev_width

        return x

def export():
    for font in sorted(glob.glob('./fonts/*.py')):
        m = re.search(r'.*\\(.*)\.py', font)
        print("import "+m.group(1))

    for font in sorted(glob.glob('./fonts/*.py')):
        m = re.search(r'.*\\(.*)\.py', font)
        print("""
print("%s")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, %s)
ssd.show_buffer()""" % (m.group(1), m.group(1)))

#export()
#sys.exit()

ssd = SSD1306(buffer_rows=52, buffer_cols=128*32)
text = "The quick brown fox jumps over the fence."
text = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

print("arial_monospaced_for_sap_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_monospaced_for_sap_regular_10)
ssd.show_buffer()

print("arial_monospaced_for_sap_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_monospaced_for_sap_regular_12)
ssd.show_buffer()

print("arial_monospaced_for_sap_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_monospaced_for_sap_regular_14)
ssd.show_buffer()

print("arial_monospaced_for_sap_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_monospaced_for_sap_regular_20)
ssd.show_buffer()

print("arial_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_regular_10)
ssd.show_buffer()

print("arial_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_regular_12)
ssd.show_buffer()

print("arial_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_regular_14)
ssd.show_buffer()

print("arial_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, arial_regular_20)
ssd.show_buffer()

print("calibri_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, calibri_regular_10)
ssd.show_buffer()

print("calibri_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, calibri_regular_12)
ssd.show_buffer()

print("calibri_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, calibri_regular_14)
ssd.show_buffer()

print("calibri_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, calibri_regular_20)
ssd.show_buffer()

print("lucida_console_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_console_regular_10)
ssd.show_buffer()

print("lucida_console_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_console_regular_12)
ssd.show_buffer()

print("lucida_console_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_console_regular_14)
ssd.show_buffer()

print("lucida_console_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_console_regular_20)
ssd.show_buffer()

print("lucida_sans_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_sans_regular_10)
ssd.show_buffer()

print("lucida_sans_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_sans_regular_12)
ssd.show_buffer()

print("lucida_sans_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_sans_regular_14)
ssd.show_buffer()

print("lucida_sans_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, lucida_sans_regular_20)
ssd.show_buffer()

print("ms_reference_sans_serif_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, ms_reference_sans_serif_regular_10)
ssd.show_buffer()

print("ms_reference_sans_serif_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, ms_reference_sans_serif_regular_12)
ssd.show_buffer()

print("ms_reference_sans_serif_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, ms_reference_sans_serif_regular_14)
ssd.show_buffer()

print("ms_reference_sans_serif_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, ms_reference_sans_serif_regular_20)
ssd.show_buffer()

print("polo_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, polo_regular_10)
ssd.show_buffer()

print("polo_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, polo_regular_12)
ssd.show_buffer()

print("polo_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, polo_regular_14)
ssd.show_buffer()

print("polo_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, polo_regular_20)
ssd.show_buffer()

print("segoe_print_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, segoe_print_regular_10)
ssd.show_buffer()

print("segoe_print_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, segoe_print_regular_12)
ssd.show_buffer()

print("segoe_print_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, segoe_print_regular_14)
ssd.show_buffer()

print("segoe_print_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, segoe_print_regular_20)
ssd.show_buffer()

print("tahoma_regular_10")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, tahoma_regular_10)
ssd.show_buffer()

print("tahoma_regular_12")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, tahoma_regular_12)
ssd.show_buffer()

print("tahoma_regular_14")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, tahoma_regular_14)
ssd.show_buffer()

print("tahoma_regular_20")
ssd.clear_buffer()
ssd.draw_text3(0, 0, text, tahoma_regular_20)
ssd.show_buffer()
