import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from config import get_config, print_usage, print_config


def encode(img, msg):
    orig_shape = img.shape
    img[np.logical_and(img % 2 != 0, img != 0)] -= 1
    flat = img.flatten()
    bits = [bin(ord(i))[2:].zfill(8) for i in msg]
    joined = "".join(bits)
    bit_array = np.array([c for c in joined]).astype(np.uint8)
    padded = np.pad(bit_array, (0, flat.size - bit_array.size))
    encoded_flat = flat + padded
    encoded = encoded_flat.reshape(orig_shape)
    return encoded


def decode(image):
    flat = image.flatten()
    byte = np.split((flat % 2), 8)
    asc = np.packbits(byte)
    msg = "".join([chr(i) for i in asc if i != 0])
    return msg


def main(config):
    if config.mode == "encode":
        image = np.array(Image.open(config.image))
        message = config.message
        encoded = encode(image, message)
        result = Image.fromarray(encoded)
        result.save(config.out)

    elif config.mode == "decode":
        img_read = np.array(Image.open(config.image))
        message = decode(img_read)
        print(message)

    else:
        raise ValueError("Unknown mode")


if __name__ == "__main__":
    conf, unparsed = get_config()

    if len(unparsed) > 0:
        print_usage()
        exit(1)

    print_config(conf)
    main(conf)
