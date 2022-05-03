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


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="100%")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        smfont = graphics.Font()
        font.LoadFont("../fonts/7x13B.bdf")
#        smfont.LoadFont("../fonts/tom-thumb.bdf")
        smfont.LoadFont("../fonts/clR6x12.bdf")
        textColor = graphics.Color(255, 255, 255) #white?
        ampColor = graphics.Color(255, 255, 0) #white?
        frameColor = graphics.Color(125, 0, 125) #

        red = graphics.Color(255, 0, 0)
        dimred = graphics.Color(125, 0, 0)
        green = graphics.Color(0, 255, 0)
        blue = graphics.Color(0, 0, 255)
        white = graphics.Color(255, 255, 255)

        pos = offscreen_canvas.width
        my_text = self.args.text
        soc_text = ["S","O","C"]
        amp_text = "+33A"

        currentData =np.array(
                     [0, 0, 0, 0, -9.3, -10.9, -5.1,  0.0, 0.0,   0.0,
                      12.6, 16.1,  16.9,  18.9,  22.5,  24.5, 25.6, 25.9, 27.0, 29.0,
                      30.0, 26.3,  46.3,  54.5,  49.5,  43.0, 38.5, 35.0, 34.0,	33.0,
		      33.0, 34.7])



        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, 1, offscreen_canvas.height, textColor, my_text)
        left_start = offscreen_canvas.width-len-2
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, left_start, 9, textColor, my_text)
        #len = graphics.DrawText(offscreen_canvas, smfont, left_start-10, 6, textColor, soc_text[0])
        #len = graphics.DrawText(offscreen_canvas, smfont, left_start-6, 8, textColor, soc_text[1])
        #len = graphics.DrawText(offscreen_canvas, smfont, left_start-2, 10, textColor, soc_text[2])

        len = graphics.DrawText(offscreen_canvas, smfont, left_start, 18, green, amp_text)

        graphOrigin = [left_start, 18] #remember 0,0 is top left corner
        graphHeight = 32 - graphOrigin[1] - 1
        graphWidth = 64-left_start-1
        graphBottom = graphOrigin[1]+graphHeight


        edgeSetback = (max(currentData[0:graphWidth]) - min(currentData[0:graphWidth])) * 0.05
        maxCurrent = max(currentData[0:graphWidth]) + edgeSetback
        minCurrent = min(currentData[0:graphWidth]) - edgeSetback
        currentRange = maxCurrent - minCurrent


        graphics.DrawLine(offscreen_canvas,
           graphOrigin[0], graphOrigin[1],
           graphOrigin[0], graphOrigin[1]+graphHeight, frameColor)
        graphics.DrawLine(offscreen_canvas,
           graphOrigin[0], graphOrigin[1]+graphHeight,
           graphOrigin[0]+graphWidth, graphOrigin[1]+graphHeight, frameColor)

        print("range:", currentRange, " edge:", edgeSetback, " max:", maxCurrent, " min:", minCurrent)

        #Draw zero Line
        if (minCurrent < 0):
           percentOfRange = (0-minCurrent)/currentRange
           y = int(round(graphBottom - (percentOfRange * graphHeight)))
           print("Zero line:", y)
           graphics.DrawLine(offscreen_canvas, graphOrigin[0], y, graphOrigin[0]+graphWidth, y, dimred)

        #First Point
        percentOfRange = (currentData[0]-minCurrent)/currentRange
        y = int(round(graphBottom - (percentOfRange * graphHeight)))
        offscreen_canvas.SetPixel(graphOrigin[0]+1, y, 0, 255, 0)
        lasty = y

        for x in range(1, graphWidth):
           percentOfRange = (currentData[x]-minCurrent)/currentRange
           y = int(round(graphBottom - (percentOfRange * graphHeight)))
           print(currentData[x],percentOfRange*100, y)
           graphics.DrawLine(offscreen_canvas, x+graphOrigin[0], lasty, x+graphOrigin[0]+1, y, green)
           lasty = y



        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


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
