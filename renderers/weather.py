from typing import TYPE_CHECKING

from PIL import ImageFont
import requests

from .message import render_message

if TYPE_CHECKING:
    from PIL import ImageDraw  # noqa: F401


def render_weather(
    draw: 'ImageDraw',
    x: int,
    y: int,
    font_file: str,
    latitude: float,
    longitude: float,
    api_key: str,
):
    response = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format(
        api_key, latitude, longitude
    ))

    data = response.json()

    render_message(draw, x, y, 200, 100, font_file, str(data['currently']['temperature']))
