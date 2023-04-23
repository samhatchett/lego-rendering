import os
import bpy
import random
import bpy_extras.object_utils
from math import radians
from mathutils import Vector, Matrix
import glob


def rotate_object_randomly(obj, min_angle=-360, max_angle=360):
    random_x = radians(random.uniform(min_angle, max_angle))
    random_y = radians(random.uniform(min_angle, max_angle))
    random_z = radians(random.uniform(min_angle, max_angle))
    obj.rotation_euler = (random_x, random_y, random_z)


def place_object_on_ground(obj):
    # Update the object's bounding box data
    bpy.context.view_layer.update()

    # Find the lowest point of the object's bounding box
    world_corners = [obj.matrix_world @
                     Vector(corner) for corner in obj.bound_box]
    lowest_z = min(corner.z for corner in world_corners)

    # Move the object up so that its lowest point is on the ground plane (Z=0)
    obj.location.z -= lowest_z


def rotate_object_around_scene_origin(obj, angle_degrees):
    # Convert the angle from degrees to radians
    angle_radians = radians(angle_degrees)

    # Create the rotation matrix around the Z-axis
    rotation_matrix = Matrix.Rotation(angle_radians, 4, 'Z')

    # Apply the rotation matrix to the object's matrix_world
    obj.matrix_world = rotation_matrix @ obj.matrix_world


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

# https://blender.stackexchange.com/a/158236


def get_2d_bounding_box(obj, camera):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.
    """

    scene = bpy.context.scene
    mat = camera.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = obj.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(obj.matrix_world)
    me.transform(mat)

    camera = camera.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return [
        (
            round(min_x * dim_x),            # X
            round(dim_y - max_y * dim_y),    # Y
        ), (
            round(max_x * dim_x),  # X2
            round(max_y * dim_y)   # Y2
        )
    ]

# Converts from
#   [(min_x, min_y), (max_x, max_y)] in pixels
# to
#   [center_x, center_y, width, height] normalized to 0.0-1.0
#


def bounding_box_to_dataset_format(bounding_box, width, height):
    [(min_x, min_y), (max_x, max_y)] = bounding_box
    box_width = max_x - min_x
    box_height = max_y - min_y
    center_x = min_x + (box_width / 2)
    center_y = min_y + (box_height / 2)
    return [center_x/width, center_y/width, box_width/width, box_height/height]


def draw_bounding_box(bounding_box, input_filename):
    from PIL import Image, ImageDraw
    image = Image.open(input_filename)
    draw = ImageDraw.Draw(image)
    draw.rectangle(bounding_box, outline=(0, 255, 0), width=2)
    base, ext = os.path.splitext(input_filename)
    image.save(base + "_bounding" + ext)


def move_camera_back(camera, percentage):
    # Get the camera's forward vector (negative local Z-axis)
    forward_vector = camera.matrix_world.to_3x3() @ Vector((0, 0, 1))
    # forward_vector = -forward_vector  # Negate the vector

    # Scale the forward vector by the specified percentage
    scaled_vector = forward_vector * percentage

    # Move the camera along the scaled vector
    camera.location += scaled_vector


def reset_scene():
    # Create a new scene with default settings
    new_scene = bpy.data.scenes.new("New Scene")

    # Set the new scene as the active scene
    bpy.context.window.scene = new_scene

    # Delete the old scene
    bpy.data.scenes.remove(bpy.context.scene)


def change_object_color(obj, new_color):
    # This is very specific to how ImportLdraw creates the matieral
    # so will be someone fragile
    bpy.data.materials["Material_4_c"].node_tree.nodes["Group"].inputs[0].default_value = new_color
    return


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


def default_lighting(light):
    move_object_away_from_origin(light, 5)
    light.data.shadow_soft_size = 0.1
    light.data.energy = 1000
    bpy.data.scenes['Scene'].view_settings.exposure = 0
    bpy.data.scenes["Scene"].view_settings.look = 'None'


def soft_lighting(light):
    move_object_away_from_origin(light, 1)
    light.data.shadow_soft_size = 0.1
    light.data.energy = 1
    bpy.data.scenes['Scene'].view_settings.exposure = 0
    bpy.data.scenes["Scene"].view_settings.look = 'None'


def hard_lighting(light):
    move_object_away_from_origin(light, 1)
    light.data.shadow_soft_size = 0.001
    light.data.energy = 100
    bpy.data.scenes['Scene'].view_settings.exposure = -2
    bpy.data.scenes["Scene"].view_settings.look = 'High Contrast'

def file_exists(pattern, search_path):
    matching = glob.glob(os.path.join(search_path, '**', pattern), recursive=True)
    return len(matching) > 0
