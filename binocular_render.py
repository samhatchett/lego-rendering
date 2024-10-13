import bpy
import sys
import os
from PIL import Image

# This script runs Blender as a module. Add the current
# directly to the path so we can import our own modules too
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look, Material
from lib.colors import RebrickableColors, RebrickableColorsById

import io_scene_importldraw as ld
ld.register()


"""
make a set of binocular images for training data. returns a PIL that can be written out to a file if desired.
pass in the part and color.
"""
def make_image(part=None, color=None, rotation=(0,0,0)):

    color = int(color)
    color = RebrickableColorsById[color]
    if color is None:
        raise "could not find color"


    renderer = Renderer(ldraw_path = os.path.join(dir_path, "ldraw"))

    options = RenderOptions(
        image_filename="renders/top.png",
        quality=Quality.NORMAL,
        lighting_style=LightingStyle.DEFAULT,
        part_color=color.best_hex,
        material=Material.TRANSPARENT if color.is_transparent else Material.PLASTIC,
        light_angle=-60,
        part_rotation=rotation,
        camera_height=40,
        zoom=.8,
        look=Look.NORMAL,
        width=320,
        height=240,
    )

    renderer.render_part(part, options)
    options.camera_height = -40
    options.image_filename = "renders/bottom.png"
    renderer.render_part(part, options)

    top_img = Image.open("renders/top.png")
    bottom_img = Image.open("renders/bottom.png")

    os.remove("renders/top.png")
    os.remove("renders/bottom.png")

    top_image_rotated = top_img.rotate(90, expand=True)
    bottom_image_rotated = bottom_img.rotate(90, expand=True)

    # Create a new image large enough to fit both rotated images side by side
    new_width = top_image_rotated.width + bottom_image_rotated.width
    new_height = max(top_image_rotated.height, bottom_image_rotated.height)

    # Create a new blank image with a white background
    new_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))

    # Paste the rotated images side by side in the new image
    new_image.paste(top_image_rotated, (0, 0))
    new_image.paste(bottom_image_rotated, (top_image_rotated.width, 0))

    return new_image
