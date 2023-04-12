import random
from enum import Enum
import colorsys

class Color(Enum):
    BLUE = (0.000, 0.333, 0.749, 1)
    BLACK = (0.020, 0.075, 0.114, 1)
    WHITE = (1.000, 1.000, 1.000, 1)
    LIGHT_BLUISH_GRAY = (0.627, 0.647, 0.663, 1)
    RED = (0.788, 0.102, 0.035, 1)
    DARK_BLUISH_GRAY = (0.424, 0.431, 0.408, 1)
    YELLOW = (0.949, 0.804, 0.216, 1)
    REDDISH_BROWN = (0.345, 0.165, 0.071, 1)
    TAN = (0.894, 0.804, 0.620, 1)
    GREEN = (0.137, 0.471, 0.255, 1)
    ORANGE = (0.996, 0.541, 0.094, 1)
    TRANS_CLEAR = (0.988, 0.988, 0.988, 1)
    LIME = (0.733, 0.914, 0.043, 1)
    PEARL_GOLD = (0.667, 0.498, 0.180, 1)
    DARK_TAN = (0.584, 0.541, 0.451, 1)
    DARK_BLUE = (0.039, 0.204, 0.388, 1)
    DARK_RED = (0.447, 0.055, 0.059, 1)
    TRANS_LIGHT_BLUE = (0.682, 0.937, 0.925, 1)
    FLAT_SILVER = (0.537, 0.529, 0.533, 1)
    TRANS_RED = (0.788, 0.102, 0.035, 1)
    BRIGHT_LIGHT_ORANGE = (0.973, 0.733, 0.239, 1)
    MEDIUM_AZURE = (0.212, 0.682, 0.749, 1)
    MEDIUM_NOUGAT = (0.667, 0.490, 0.333, 1)
    BRIGHT_GREEN = (0.294, 0.624, 0.290, 1)
    DARK_PURPLE = (0.247, 0.212, 0.569, 1)
    DARK_BROWN = (0.208, 0.129, 0.000, 1)
    DARK_ORANGE = (0.663, 0.333, 0.000, 1)
    LIGHT_NOUGAT = (0.965, 0.843, 0.702, 1)
    DARK_GREEN = (0.094, 0.275, 0.196, 1)
    TRANS_ORANGE = (0.941, 0.561, 0.110, 1)
    TRANS_YELLOW = (0.961, 0.804, 0.184, 1)
    BRIGHT_PINK = (0.894, 0.678, 0.784, 1)
    DARK_AZURE = (0.027, 0.545, 0.788, 1)
    MAGENTA = (0.573, 0.224, 0.471, 1)
    DARK_TURQUOISE = (0.000, 0.561, 0.608, 1)
    MEDIUM_BLUE = (0.353, 0.576, 0.859, 1)
    SAND_GREEN = (0.627, 0.737, 0.675, 1)
    DARK_PINK = (0.784, 0.439, 0.627, 1)
    TRANS_DARK_BLUE = (0.000, 0.125, 0.627, 1)

def random_color_for_blender():
  return random.choice(list(Color)).value

def random_color_for_pil():
  color = random_color_for_blender()
  return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

# hsv in floats (0-1), rgb in ints (0-255)
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
