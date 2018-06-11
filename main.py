from io import BytesIO

from PIL import Image
from PIL import ImageDraw

from renderers import render_message


EPD_WIDTH = 640
EPD_HEIGHT = 384


def main():
    target = 'console'

    image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(image)

    # Render a message across the top
    render_message(
        draw,
        x=10,
        y=10,
        width=EPD_WIDTH - 20,
        height=96,
        font_file='fonts/NeutraFace.otf',
        message='HELLO, GORGEOUS.',
        align_x='center',
        align_y='top'
    )

    if target == 'display':
        from vendor import epd7in5b

        print('instantiating epd')
        epd = epd7in5b.EPD()
        print('initializing epd')
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
