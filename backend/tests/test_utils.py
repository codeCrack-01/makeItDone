from PIL import Image

from utils import get_contrast_fill_color

# ========================================================================= #
# ------------------------------Unit Tests--------------------------------- #
# ========================================================================= #


def test_get_contrast_fill_color_for_dark_image():
    # A dark transparent image should result in a light background
    dark_img = Image.new("RGBA", (10, 10), (20, 20, 20, 255))
    color = get_contrast_fill_color(dark_img)
    # 255 - 20 = 235 (Light)
    assert color[0] > 180


def test_get_contrast_fill_color_for_light_image():
    # A light transparent image should result in a dark background
    light_img = Image.new("RGBA", (10, 10), (240, 240, 240, 255))
    color = get_contrast_fill_color(light_img)
    assert color[0] < 180
