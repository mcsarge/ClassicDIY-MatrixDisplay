#!/usr/bin/env python
from rgbmatrix import graphics
from samplebase import SampleBase
import math
import time
import numpy as np


def scale_col(val, lo, hi):
    if val < lo:
        return 0
    if val > hi:
        return 255
    return 255 * (val - lo) / (hi - lo)


def rotate(x, y, sin, cos):
    return x * cos - y * sin, x * sin + y * cos

def drawGraph(data, theOrigin, theHeight, theWidth, o_canvas, f_color, z_color, v_color, self):
    currentData = data
    graphOrigin = theOrigin #remember 0,0 is top left corner
    graphHeight = theHeight
    graphWidth = theWidth
    graphBottom = graphOrigin[1]+graphHeight
    #valueColor = graphics.Color(255, 255, 255)
    #valueColor = v_color


    edgeSetback = (max(currentData[0:graphWidth]) - min(currentData[0:graphWidth])) * 0.05
    maxValue = max(currentData[0:graphWidth]) + edgeSetback
    minValue = min(currentData[0:graphWidth]) - edgeSetback
    valueRange = maxValue - minValue


    graphics.DrawLine(o_canvas,
          graphOrigin[0], graphOrigin[1],
          graphOrigin[0], graphOrigin[1]+graphHeight, f_color)
    graphics.DrawLine(o_canvas,
          graphOrigin[0], graphOrigin[1]+graphHeight,
          graphOrigin[0]+graphWidth, graphOrigin[1]+graphHeight, f_color)

    print("range:", valueRange, " edge:", edgeSetback, " max:", maxValue, " min:", minValue)

    #Draw zero Line
    if (minValue < 0):
      percentOfRange = (0-minValue)/valueRange
      y = int(round(graphBottom - (percentOfRange * graphHeight)))
      print("Zero line:", y)
      graphics.DrawLine(o_canvas, graphOrigin[0], y, graphOrigin[0]+graphWidth, y, z_color)

    #First Point
    percentOfRange = (currentData[0]-minValue)/valueRange
    y = int(round(graphBottom - (percentOfRange * graphHeight)))
    o_canvas.SetPixel(graphOrigin[0]+1, y, v_color.red, v_color.green, v_color.blue)
    lasty = y

    for x in range(1, graphWidth):
      percentOfRange = (currentData[x]-minValue)/valueRange
      y = int(round(graphBottom - (percentOfRange * graphHeight)))
      print(currentData[x],percentOfRange*100, y)
      graphics.DrawLine(o_canvas, x+graphOrigin[0], lasty, x+graphOrigin[0]+1, y, v_color)
      lasty = y

    o_canvas = self.matrix.SwapOnVSync(o_canvas)

        
    
    



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=" 88%")

    
    
    
    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        socfont = graphics.Font()
        ampsfont = graphics.Font()
        wattsfont = graphics.Font()
        socfont.LoadFont("../fonts/7x13B.bdf")
#        smfont.LoadFont("../fonts/tom-thumb.bdf")
        ampsfont.LoadFont("../fonts/clR6x12.bdf")
        wattsfont.LoadFont("../fonts/5x8.bdf")
        socColor = graphics.Color(255, 255, 255) #white?
        ampColor = graphics.Color(255, 255, 0) #white?
        wattsColor = graphics.Color(0, 175, 175) #dimyellow?
        frameColor = graphics.Color(125, 0, 125) #

        #General Colors
        red = graphics.Color(255, 0, 0)
        dimred = graphics.Color(125, 0, 0)
        green = graphics.Color(0, 255, 0)
        blue = graphics.Color(0, 0, 255)
        white = graphics.Color(255, 255, 255)
        dimYellow = graphics.Color(0, 175, 175) #dimyellow?
        pos = offscreen_canvas.width
        my_text = self.args.text
        soc_text = ["S","O","C"]
        amp_text = "+2.3A"
        watts_text = "+900W"


        currentData =np.array(
                     [0, 0, 0, 0, -9.3, -10.9, -5.1,  0.0, 0.0,   0.0,
                      12.6, 16.1,  16.9,  18.9,  22.5,  24.5, 25.6, 25.9, 27.0, 29.0,
                      30.0, 26.3,  46.3,  54.5,  49.5,  43.0, 38.5, 35.0, 34.0,	33.0,
                      33.0, 34.7])


        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, socfont, 0, 0, socColor, my_text)
        left_start = offscreen_canvas.width-len-1
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, socfont, left_start, 9, socColor, my_text)
        len = graphics.DrawText(offscreen_canvas, ampsfont, left_start, 20, green, amp_text)
        
        len = graphics.DrawText(offscreen_canvas, ampsfont, left_start, 32
                                , wattsColor, watts_text)
#        len = graphics.DrawText(offscreen_canvas, wattsfont, left_start, 25, wattsColor, watts_text)

        graphOrigin = [0, 0] #remember 0,0 is top left corner
        graphHeight = 32 - graphOrigin[1] - 1
        graphWidth = 32

        drawGraph(currentData, graphOrigin, graphHeight, graphWidth, offscreen_canvas, frameColor, dimred, blue, self)


        while True:
#            offscreen_canvas.Clear()
#            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
#            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


class RotatingBlockGenerator(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RotatingBlockGenerator, self).__init__(*args, **kwargs)

    def run(self):
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(self.matrix.width, self.matrix.height) * 0.7
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * 3.14159265 / 360
        rotation = 0

        # Pre calculate colors
        col_table = []
        for x in range(int(min_rotate), int(max_rotate)):
            col_table.insert(x, scale_col(x, min_display, max_display))

        offset_canvas = self.matrix.CreateFrameCanvas()

        while True:
            rotation += 1
            rotation %= 360

            # calculate sin and cos once for each frame
            angle = rotation * deg_to_rad
            sin = math.sin(angle)
            cos = math.cos(angle)

            for x in range(int(min_rotate), int(max_rotate)):
                for y in range(int(min_rotate), int(max_rotate)):
                    # Our rotate center is always offset by cent_x
                    rot_x, rot_y = rotate(x - cent_x, y - cent_x, sin, cos)

                    if x >= min_display and x < max_display and y >= min_display and y < max_display:
                        x_col = col_table[x]
                        y_col = col_table[y]
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, x_col, 255 - y_col, y_col)
                    else:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)


# Main function
if __name__ == "__main__":
#    program = RotatingBlockGenerator()
    program = RunText()
    if (not program.process()):
        program.print_help()
