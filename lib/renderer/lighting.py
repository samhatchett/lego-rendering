import bpy
import math
from mathutils import Vector, Matrix

from lib.renderer.render_options import LightingStyle
from lib.renderer.utils import rotate_around_z_origin, aim_towards_origin


def setup_lighting(options):
    if options.lighting_style == LightingStyle.DEFAULT:
        default_lighting(options)
    elif options.lighting_style == LightingStyle.HARD:
        hard_lighting(options)

def default_lighting(options):
    light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
    light_data.energy = 400
    light_data.shape = 'SQUARE'
    light_data.size = 7
    light_data.color = (1, 1, 1)
    light = bpy.data.objects.new(name="KeyLight", object_data=light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0.1, 0, 0)
    move_object_away_from_origin(light, 4.5)
    rotate_around_z_origin(light, options.light_angle)
    set_height_by_angle(light, 60)
    aim_towards_origin(light)

def hard_lighting(options):
    light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
    light_data.energy = 500
    light_data.shape = 'SQUARE'
    light_data.size = 1
    light_data.color = (1, 1, 1)
    light = bpy.data.objects.new(name="KeyLight", object_data=light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0.1, 0, 0)
    move_object_away_from_origin(light, 6)
    rotate_around_z_origin(light, options.light_angle)
    set_height_by_angle(light, 75)
    aim_towards_origin(light)

# Good for rendering white instructional parts
def bright_lighting(light):
    move_object_away_from_origin(light, 5)
    light.data.shadow_soft_size = 0.1
    light.data.energy = 1
    bpy.data.scenes['Scene'].view_settings.exposure = 2
    bpy.data.scenes["Scene"].view_settings.look = 'None'


def move_object_away_from_origin(obj, distance):
    location = obj.location

    # Calculate the vector from the origin to the objects's location
    origin = Vector((0, 0, 0))
    vector_to_object = location - origin

    # Normalize the vector and multiply it by the desired distance
    vector_to_object.normalize()
    vector_to_object *= distance

    # Calculate the new location for the object
    new_location = origin + vector_to_object

    # Set the objects's location to the new location
    obj.location = new_location


def set_height_by_angle(light, angle_in_degrees):
    # convert the angle to radians
    angle_in_radians = math.radians(angle_in_degrees)

    # calculate the distance to the origin
    distance_to_origin = light.location.length

    # calculate the new height and distance in the ground plane
    new_height = math.sin(angle_in_radians) * distance_to_origin
    new_ground_distance = math.cos(angle_in_radians) * distance_to_origin

    # set the new height, maintaining the same rotation around the Z axis
    light.location.z = new_height
    light.location.xy = light.location.xy.normalized() * new_ground_distance
