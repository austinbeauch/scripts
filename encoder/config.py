import argparse

arg_lists = []
parser = argparse.ArgumentParser()


# ----------------------------------------
# Some nice macros to be used for arparse
def str2bool(v):
    return v.lower() in ("true", "1")


def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg


def print_notification(content_list, notifi_type='NOTIFICATION'):
    print(
        '---------------------- {0} ----------------------'.format(notifi_type))
    print()
    for content in content_list:
        print(content)
    print()
    print('---------------------- END ----------------------')


def print_config(config):
    content_list = []
    args = list(vars(config))
    args.sort()
    for arg in args:
        content_list += [arg.rjust(25, ' ') + '  ' + str(getattr(config, arg))]
    print_notification(content_list, 'CONFIG')


main_arg = add_argument_group("Main")

main_arg.add_argument("--mode", type=str,
                      default="encode",
                      choices=["encode", "decode"],
                      help="Encode message or decode")

main_arg.add_argument("--message", type=str,
                      help="String to encode")

main_arg.add_argument("--image", type=str, required=True,
                      help="Image for encoding/decoding")

main_arg.add_argument("--out", type=str,
                      default="out.png",
                      help="Output file")


def get_config():
    config, unparsed = parser.parse_known_args()

    return config, unparsed


def print_usage():
    parser.print_usage()
