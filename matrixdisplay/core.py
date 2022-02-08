#!/usr/bin/env python
from rgbmatrix import graphics
from samplebase import SampleBase
import math


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
        font.LoadFont("../fonts/7x13.bdf")
        smfont.LoadFont("../fonts/5x7.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text
        soc_text = "S"

        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, 1, offscreen_canvas.height, textColor, my_text)
        left_start = offscreen_canvas.width-len-2
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, left_start, 15, textColor, my_text)
        len = graphics.DrawText(offscreen_canvas, smfont, left_start-10, 6, textColor, soc_text)

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