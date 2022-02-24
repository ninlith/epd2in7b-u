#!/usr/bin/env python3
import logging
import time
from PIL import Image, ImageOps
from lib import epd2in7b_u as epd2in7b

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in7b-u Demo")
    epd = epd2in7b.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)

    logging.info("Creating images...")
    black_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    red_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    empty_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    for x in range(epd.height):
        for y in range(epd.width):
            if (x + y) % 16 == 0:
                red_image.putpixel((x, y), 0)
            if (x + y + 8) % 16 == 0:
                black_image.putpixel((x, y), 0)
    mirrored_black_image = ImageOps.mirror(black_image)
    black_image = black_image.rotate(90, expand=True)
    red_image = red_image.rotate(90, expand=True)
    empty_image = empty_image.rotate(90, expand=True)
    mirrored_black_image = mirrored_black_image.rotate(90, expand=True)

    logging.info("Differential refresh (fast partial update)...")
    epd.set_lut(fast=True)
    epd.display_partial_image(mirrored_black_image,
                              empty_image,
                              32,
                              epd.height - 64 - 32,
                              64,
                              64)
    time.sleep(20)
    epd.display_partial_image(black_image,
                              empty_image,
                              32,
                              epd.height - 64 - 32,
                              64,
                              64)
    time.sleep(20)

    logging.info("Windowed refresh using full flush cycle...")
    epd.set_lut(fast=False)
    epd.display_partial_image(black_image,
                              red_image,
                              32,
                              epd.height - 64*2 - 32*2,
                              64,
                              64)
    time.sleep(20)

    logging.info("Clear...")
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7b.epdconfig.module_exit()
    exit()
