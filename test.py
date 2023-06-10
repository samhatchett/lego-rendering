import bpy
import sys
import os

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look
from lib.colors import RebrickableColors

renderer = Renderer(ldraw_path="./ldraw")

color = RebrickableColors.TransClear

options = RenderOptions(
    image_filename = "renders/test.png",
    bounding_box_filename = "renders/test.txt",
    blender_filename = "renders/test.blend",
    quality = Quality.DRAFT,
    lighting_style = LightingStyle.DEFAULT,
    light_angle = 160,
    part_color = color.value.rebrickable_blender,
    part_transparent = color.value.is_transparent,
    part_rotation=(0, 0, 0),
    camera_height=45,
    zoom=0.1,
    look=Look.NORMAL,
    render_width=244,
    render_height=244,
)
renderer.render_part("60169", options)
