from io import BytesIO

from PIL import Image
from PIL import ImageDraw

from renderers.message import render_message
from renderers.weather import render_weather

# Create this file and seed it with config variables
from local import LATITUDE, LONGITUDE, DARK_SKY_KEY, FONT_FILE


EPD_WIDTH = 640
EPD_HEIGHT = 384


def main():
    target = 'console'

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
        message='HELLO, GORGEOUS.',
        align_x='center',
        align_y='top'
    )

    render_weather(
        draw,
        x=10,
        y=msg_h + msg_y + 10, # 10px lower than the message
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

    elif target == 'console':
        import iterm2_tools

        # print for iterm
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        print(iterm2_tools.image_bytes(buffered.getvalue()))


if __name__ == '__main__':
    main()
