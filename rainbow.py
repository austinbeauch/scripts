from phue import Bridge
import time


MAX_HUE = 65535
INC = 875  # MAX_HUE // 20
SLEEP = 0.1
bridge_ip = '192.168.0.10'

b = Bridge(bridge_ip)
b.get_api()


def next_color(n):
    if n >= MAX_HUE:
        n = 0
    n += INC
    print((n + INC) % MAX_HUE, n)
    return n


def map_color(h, offset=0):
    if h + offset > MAX_HUE:
        return h + offset - MAX_HUE
    else:
        return h + offset


def main():
    names = [i for i in b.get_light_objects('name')]
    lights = b.get_light_objects('name')

    for light in names:
        b.set_light(light, 'on', True)
        b.set_light(light, 'bri', 245)

    h = next_color(0)
    offset = MAX_HUE / len(b.get_light_objects('name'))

    while True:
        h = next_color(h)
        for i, light in enumerate(names):
            lights[light].saturation = 255
            lights[light].hue = map_color(h, i*offset)
        time.sleep(SLEEP)


if __name__ == "__main__":
    print("Starting on", bridge_ip)
    main()
