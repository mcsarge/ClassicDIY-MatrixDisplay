#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        smfont = graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/9x18B.bdf")
        smfont.LoadFont("../../rpi-rgb-led-matrix/fonts/tom-thumb.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

        len = graphics.DrawText(offscreen_canvas, font, 32, 12, textColor, my_text)
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width-len, 12, textColor, my_text)
        len = graphics.VerticalDrawText(offscreen_canvas, font, offscreen_canvas.width-len-9, 12, textColor, my_text)
        print(len)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        while True:
#            offscreen_canvas.Clear()
#            len = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

#            time.sleep(0.4)
#            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
