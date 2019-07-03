from . import voice_to_lights
from . import bridge

hues = {'red': 0, 'yellow': 10000, 'green': 20000, 'cyan': 35000, 'blue': 45000, 'purple': 49152, 'pink': 57500}
colors = {'red', 'green', 'blue', 'cyan', 'yellow', 'purple'}

r = hues['red']
b = hues['blue']
g = hues['green']
y = hues['yellow']
p = hues['purple']

# define mapping with words: (hue, brightness, saturation)
mapping = {
    'battle': (r, 255, 255),
    'fight': (r, 255, 255),
    'rest': (b, 100, 255),
    'sleep': (b, 100, 255),
    'night': (b, 100, 255),
    'day': (y, 255, 100),
    'morning': (y, 255, 100),
    'over': (g, 255, 100)
}

triggers = set(mapping).union(colors)
