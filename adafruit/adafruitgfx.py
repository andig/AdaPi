#----------------------------------------------------------------------
# adafruitgfx.py ported by Andreas Goetz, http://www.cpuidle.de
#   https://github.com/andig/AdaPi
#
# This library is a pure-python port of the Adafruit GFX C library:
#
#   https://github.com/adafruit/Adafruit-GFX-Library
#
# It is intended to be used with the py-gaugette library for driving
# SSD1306 OLEDs on a Raspberry Pi
#
#   https://github.com/guyc/py-gaugette
#
# This is a our graphics core library, for all our displays. 
# We'll be adapting all the
# existing libaries to use this core to make updating, support 
# and upgrading easier!
# 
# Adafruit invests time and resources providing this open source code, 
# please support Adafruit and open-source hardware by purchasing 
# products from Adafruit!
# 
# Written by Limor Fried/Ladyada  for Adafruit Industries.  
# BSD license, check license.txt for more information
# All text above must be included in any redistribution

WIDTH = 128
HEIGHT = 32

class AdafruitGFX(object):

    def __init__(self, w=WIDTH, h=HEIGHT):
        self._width = w
        self._height = h

        self.rotation = 0;    
        self.cursor_y = cursor_x = 0
        
        self.textsize = 1
        self.textcolor = textbgcolor = 0xFFFF
        
        self.wrap = True

    # self.draw a circle outline
    def draw_circle(self, x0, y0, r, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.draw_pixel(x0, y0+r, color)
        self.draw_pixel(x0, y0-r, color)
        self.draw_pixel(x0+r, y0, color)
        self.draw_pixel(x0-r, y0, color)

        while (x<y):
            if (f >= 0):
                y     -=1
                ddF_y += 2
                f     += ddF_y

            x     +=1
            ddF_x += 2
            f     += ddF_x

            self.draw_pixel(x0 + x, y0 + y, color)
            self.draw_pixel(x0 - x, y0 + y, color)
            self.draw_pixel(x0 + x, y0 - y, color)
            self.draw_pixel(x0 - x, y0 - y, color)
            self.draw_pixel(x0 + y, y0 + x, color)
            self.draw_pixel(x0 - y, y0 + x, color)
            self.draw_pixel(x0 + y, y0 - x, color)
            self.draw_pixel(x0 - y, y0 - x, color)


    def draw_circle_helper(self, x0, y0, r, cornername, color):
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x     = 0
        y     = r

        while (x<y):
            if (f >= 0):
                y     -=1
                ddF_y += 2
                f     += ddF_y

            x     +=1
            ddF_x += 2
            f     += ddF_x

            if (cornername & 0x4):
                self.draw_pixel(x0 + x, y0 + y, color)
                self.draw_pixel(x0 + y, y0 + x, color)

            if (cornername & 0x2):
                self.draw_pixel(x0 + x, y0 - y, color)
                self.draw_pixel(x0 + y, y0 - x, color)

            if (cornername & 0x8):
                self.draw_pixel(x0 - y, y0 + x, color)
                self.draw_pixel(x0 - x, y0 + y, color)

            if (cornername & 0x1):
                self.draw_pixel(x0 - y, y0 - x, color)
                self.draw_pixel(x0 - x, y0 - y, color)


    def fill_circle(self, x0, y0, r, color):
        self.draw_fast_vline(x0, y0-r, 2*r+1, color)
        fill_circle_helper(x0, y0, r, 3, 0, color)

    # used to do circles and roundrects!
    def fill_circle_helper(self, x0, y0, r, cornername, delta, color):
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x     = 0
        y     = r

        while (x<y):
            if (f >= 0):
                y     -=1
                ddF_y += 2
                f     += ddF_y

            x     +=1
            ddF_x += 2
            f     += ddF_x

            if (cornername & 0x1):
                self.draw_fast_vline(x0+x, y0-y, 2*y+1+delta, color)
                self.draw_fast_vline(x0+y, y0-x, 2*x+1+delta, color)

            if (cornername & 0x2):
                self.draw_fast_vline(x0-x, y0-y, 2*y+1+delta, color)
                self.draw_fast_vline(x0-y, y0-x, 2*x+1+delta, color)


    # to be overwritten
    def draw_pixel(self, x, y, color):
        pass

    # bresenham's algorithm - thx wikpedia
    def draw_line(self, x0, y0, x1, y1, color):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if (steep):
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx / 2

        if (y0 < y1):
            ystep = 1
        else:
            ystep = -1

        while (x0 <= x1):
            if (steep):
                self.draw_pixel(y0, x0, color)
            else:
                self.draw_pixel(x0, y0, color)

            err -= dy
            if (err < 0):
                y0 += ystep
                err += dx
            x0+=1


    # self.draw a rectangle
    def draw_rect(self, x, y, w, h, color):
        self.draw_fast_hline(x, y, w, color)
        self.draw_fast_hline(x, y+h-1, w, color)
        self.draw_fast_vline(x, y, h, color)
        self.draw_fast_vline(x+w-1, y, h, color)


    def draw_fast_vline(self, x, y, h, color):
        # stupidest version - update in subclasses if desired!
        self.draw_line(x, y, x, y+h-1, color)


    def draw_fast_hline(self, x, y, w, color):
        # stupidest version - update in subclasses if desired!
        self.draw_line(x, y, x+w-1, y, color)


    def fill_rect(self, x, y, w, h, color):
        # stupidest version - update in subclasses if desired!
        for i in range(x, x+w):
            self.draw_fast_vline(i, y, h, color)


    def fill_screen(self, color):
        fill_rect(0, 0, self._width, self._height, color)


    # self.draw a rounded rectangle!
    def draw_round_rect(self, x, y, w, h, r, color):
        # smarter version
        self.draw_fast_hline(x+r  , y    , w-2*r, color) # Top
        self.draw_fast_hline(x+r  , y+h-1, w-2*r, color) # Bottom
        self.draw_fast_vline(x    , y+r  , h-2*r, color) # Left
        self.draw_fast_vline(x+w-1, y+r  , h-2*r, color) # Right
        # self.draw four corners
        self.draw_circle_helper(x+r    , y+r    , r, 1, color)
        self.draw_circle_helper(x+w-r-1, y+r    , r, 2, color)
        self.draw_circle_helper(x+w-r-1, y+h-r-1, r, 4, color)
        self.draw_circle_helper(x+r    , y+h-r-1, r, 8, color)


    # fill a rounded rectangle!
    def fill_round_rect(self, x, y, w, h, r, color):
        # smarter version
        fill_rect(x+r, y, w-2*r, h, color)

        # self.draw four corners
        fill_circle_helper(x+w-r-1, y+r, r, 1, h-2*r-1, color)
        fill_circle_helper(x+r    , y+r, r, 2, h-2*r-1, color)


    # self.draw a triangle!
    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)


    # fill a triangle!
    def fill_triangle (self, x0, y0, x1, y1, x2, y2, color):
        a, b, y, last

        # Sort coordinates by Y order (y2 >= y1 >= y0)
        if (y0 > y1):
            y0, y1 = y1, y0
            x0, x1 = x1, x0

        if (y1 > y2):
            y2, y1 = y1, y2
            x2, x1 = x1, x2

        if (y0 > y1):
            y0, y1 = y1, y0
            x0, x1 = x1, x0

        # Handle awkward all-on-same-line case as its own thing
        if (y0 == y2): 
            a = b = x0
            if (x1 < a):
                a = x1
            elif(x1 > b):
                b = x1
            if(x2 < a):
                a = x2
            elif(x2 > b):
                b = x2
            self.draw_fast_hline(a, y0, b-a+1, color)
            return

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa   = 0
        sb   = 0

        # For upper part of triangle, find scanline crossings for segments
        # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
        # is included here (and second loop will be skipped, avoiding a /0
        # error there), otherwise scanline y1 is skipped here and handled
        # in the second loop...which also avoids a /0 error here if y0=y1
        # (flat-topped triangle).
        if (y1 == y2):
            last = y1      # Include y1 scanline
        else:
            last = y1-1    # Skip it

        # for(y=y0; y<=last; y+=1)
        for y in range(y, y0+last+1):
            a   = x0 + sa / dy01
            b   = x0 + sb / dy02
            sa += dx01
            sb += dx02
            if(a > b):
                a,b = b,a
            self.draw_fast_hline(a, y, b-a+1, color)

        # For lower part of triangle, find scanline crossings for segments
        # 0-2 and 1-2.  This loop is skipped if y1=y2.
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)

        #for(; y<=y2; y+=1)
        while (y <= y2):
            a   = x1 + sa / dy12
            b   = x0 + sb / dy02
            sa += dx12
            sb += dx02
            if(a > b):
                a,b = b,a
            self.draw_fast_hline(a, y, b-a+1, color)
            y+=1
        

#    def drawBitmap(self, x, y, const *bitmap, w, h, color):
#        i, j, byteWidth = (w + 7) / 8
#        #for(j=0; j<h; j+=1)
#        for j in range(0, h)
#            #for(i=0; i<w; i+=1 )
#            for i in range(0, w)
#                if(pgm_read_byte(bitmap + j * byteWidth + i / 8) & (128 >> (i & 7))):
#                    self.draw_pixel(x+i, y+j, color)


#    def write(self, c):
#        if (c == '\n'):
#            cursor_y += textsize*8
#            cursor_x = 0
#        elif (c == '\r'):
#            # skip em
#        else:
#            self.draw_char(cursor_x, cursor_y, c, textcolor, textbgcolor, textsize)
#            cursor_x += textsize*6
#            if (self.wrap && (cursor_x > (self._width - textsize*6)))
#                cursor_y += textsize*8
#                cursor_x = 0
#
#
#    # self.draw a character
#    def draw_char(self, x, y, unsigned char c, color, ubg, size):
#        if ((x >= self._width)            || # Clip right
#            (y >= self._height)           || # Clip bottom
#            ((x + 5 * size - 1) < 0)      || # Clip left
#            ((y + 8 * size - 1) < 0)):       # Clip top
#            return
#
#        for (i=0; i<6; i+=1)
#        if (i == 5):
#            line = 0x0
#        else:
#            line = pgm_read_byte(font+(c*5)+i)
#        for (j = 0; j<8; j+=1)
#            if (line & 0x1):
#                if (size == 1): # default size
#                    self.draw_pixel(x+i, y+j, color)
#                else:           # big size
#                    fill_rect(x+(i*size), y+(j*size), size, size, color)
#            elif (bg != color):
#                if (size == 1): # default size
#                    self.draw_pixel(x+i, y+j, bg)
#                else:           # big size
#                    fill_rect(x+i*size, y+j*size, size, size, bg)
#            line >>= 1


    def set_cursor(self, x, y):
        cursor_x = x
        cursor_y = y


    def set_text_size(self, s):
        if s > 0:
            self.textsize = s
        else:
            self.textsize = 1            


    def set_text_color(self, uc, ub=None):
        self.textcolor = c
        self.textbgcolor = ub if ub != None else c
        # for 'transparent' background, we'll set the bg 
        # to the same as fg instead of using a flag


    def set_text_wrap(self, w):
        self.wrap = w


    def get_rotation(self):
        self.rotation %= 4
        return self.rotation


    def set_rotation(self, x):
        self.rotation = x % 4;    # cant be higher than 3
        if self.rotation % 2 == 0:
            self._width, self._height = WIDTH, HEIGHT
        else:
            self._width, self._height = HEIGHT, WIDTH


    def invert_display(self, i):
        pass
    # do nothing, can be subclassed


    # return the size of the display which depends on the rotation!
    def get_width(self):
        return self._width


    def get_height(self):
        return self._height


    #
    # following functions imported from ssd1306
    #
    
    # simple text using 5x7 font
    def draw_text(self, x, y, string, size=1, space=1):
        font_bytes = self.font.bytes
        font_rows = self.font.rows
        font_cols = self.font.cols
        for c in string:
            p = ord(c) * font_cols
            for col in range(0,font_cols):
                mask = font_bytes[p]
                p   += 1
                py   = y
                for row in range(0,8):
                    for sy in range(0,size):
                        px = x
                        for sx in range(0,size):
                            self.draw_pixel(px,py,mask & 0x1)
                            px += 1
                        py += 1
                    mask >>= 1
                x += size
            x += space
        return x

    # proportional text using fonts module
    def draw_text3(self, x, y, string, font):
        height = font.char_height
        prev_char = None

        for c in string:
            if (c<font.start_char or c>font.end_char):
                if prev_char != None:
                    x += font.space_width + prev_width + font.gap_width
                prev_char = None
            else:
                pos = ord(c) - ord(font.start_char)
                (width,offset) = font.descriptors[pos]

                if prev_char != None:
                    x += font.kerning[prev_char][pos] + font.gap_width
                    
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