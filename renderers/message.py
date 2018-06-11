from typing import TYPE_CHECKING
from PIL import ImageFont

if TYPE_CHECKING:
    from PIL import ImageDraw  # noqa: F401


def render_message(
    draw: 'ImageDraw',
    x: int,
    y: int,
    width: int,
    height: int,
    font_file: str,
    message: str,
    align_x='center',
    align_y='center',
    max_font_size=72,
    min_font_size=10,
    font_size_step=1,
    **pil_kwargs
):
    """
    Render a message directly into an ImageDraw object at particular
    coordinates and fit that message within a particular box size

    Returns a tuple:

        (
            image_draw,
            rendered_width,
            rendered_height,
            rendered_x,
            rendered_y,
        )
    """

    # Choose a font size that fits in the frame:
    size = max_font_size
    font = ImageFont.truetype(
        font_file, size, layout_engine=ImageFont.LAYOUT_RAQM
    )
    text_w, text_h = draw.textsize(message, font=font, **pil_kwargs)

    while (text_w > width or text_h > height) and size > min_font_size:
        size = size - font_size_step
        font = ImageFont.truetype(
            font_file, size, layout_engine=ImageFont.LAYOUT_RAQM
        )
        text_w, text_h = draw.textsize(message, font=font, **pil_kwargs)

    # Calculate coordinates for aligning text as requested

    if align_x == 'center':
        text_x = x + (width - text_w) / 2
    elif align_x == 'left':
        text_x = x
    elif align_x == 'right':
        text_x = x + width
    else:
        raise ValueError('align_x must be \'center\', \'right\', or \'left\'')

    if align_y == 'center':
        text_y = y + (height - text_h) / 2
    elif align_y == 'top':
        text_y = y
    elif align_y == 'bottom':
        text_y = y + height
    else:
        raise ValueError('align_y must be \'center\', \'top\', or \'bottom\'')

    # Render the image

    draw.fontmode = "1"  # Disable anti-aliasing
    draw.text((text_x, text_y), message, font=font, fill=000, **pil_kwargs)

    # Return useful values

    return (
        draw,
        text_w,
        text_h,
        text_x,
        text_y,
    )
