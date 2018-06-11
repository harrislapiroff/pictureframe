from decimal import Decimal
from typing import TYPE_CHECKING

import requests

from .message import render_message

if TYPE_CHECKING:
    from PIL import ImageDraw  # noqa: F401


def render_weather_today(
    draw: 'ImageDraw',
    x: int,
    y: int,
    width: int,
    height: int,
    font_file: str,
    latitude: float,
    longitude: float,
    api_key: str,
):
    api_url = 'https://api.darksky.net/forecast/{}/{},{}'.format(
        api_key, latitude, longitude
    )
    response = requests.get(api_url)

    data = response.json()

    temperature = Decimal(data['currently']['temperature'])
    icon = data['currently']['icon']
    summary = data['currently']['summary']

    _, _, msg_h, _, msg_y = render_message(
        draw,
        x,
        y,
        width,
        height // 8,
        font_file,
        '{}° {}'.format(round(temperature, 0), summary),
        max_font_size=height // 8,
        align_y='top',
        align_x='left',
        features=['case', 'cpsp']
    )

    _, _, msg_h, _, msg_y = render_message(
        draw,
        x,
        msg_h + msg_y + 10,
        width,
        height // 8,
        font_file,
        'Low: {} High: {}'.format(
            data['daily']['data'][0]['temperatureLow'],
            data['daily']['data'][0]['temperatureHigh']
        ),
        max_font_size=height // 8,
        align_y='top',
        align_x='left',
        features=['case', 'cpsp']
    )
