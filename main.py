import argparse
import random
import sys
from io import BytesIO

from PIL import Image
from PIL import ImageDraw

from renderers.message import render_message
from renderers.weather import render_weather_today

# Create this file and seed it with config variables
from local import LATITUDE, LONGITUDE, DARK_SKY_KEY, FONT_FILE


EPD_WIDTH = 640
EPD_HEIGHT = 384


MESSAGES = [
    'GOOD MORNING, GOOD LOOKING.',
    'HELLO, GORGEOUS.',
    'UP AND AT ’EM, TIGER',
]


def setup():
    parser = argparse.ArgumentParser(
        description='Render information to a waveshare 7.5" e-paper display'
    )
    parser.add_argument(
        '--target',
        type=str,
        nargs='?',
        help='Where to display the image. Either \'iterm\' or \'display\'.',
        default='iterm'
    )

    return parser


def main():
    parser = setup()
    args = parser.parse_args()
    target = args.target

    image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(image)

    # Render a message across the top
    _, _, msg_h, _, msg_y = render_message(
        draw,
        x=10,
        y=10,
        width=EPD_WIDTH - 20,
        height=96,
        font_file=FONT_FILE,
        message=random.choice(MESSAGES),
        align_x='center',
        align_y='top'
    )

    render_weather_today(
        draw,
        x=10,
        # 10px lower than the message
        y=msg_h + msg_y + 10,
        # 1/3 width of the display with 10px gutters (10px on L, 5px on R)
        width=EPD_WIDTH / 3 - 15,
        # height left over after message with 10px padding on the top & bottom
        height=EPD_HEIGHT - msg_h - msg_y - 20,
        font_file=FONT_FILE,
        longitude=LONGITUDE,
        latitude=LATITUDE,
        api_key=DARK_SKY_KEY,
    )

    if target == 'display':
        from vendor import epd7in5b

        epd = epd7in5b.EPD()
        epd.init()
        epd.display_frame(epd.get_frame_buffer(image))

    elif target == 'iterm':
        import iterm2_tools

        # print for iterm
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        print(iterm2_tools.image_bytes(buffered.getvalue()))

    else:
        sys.stderr.write((
            'Invalid option for target `{}`. Must be `iterm` or `display`\n'
        ).format(target))


if __name__ == '__main__':
    main()
