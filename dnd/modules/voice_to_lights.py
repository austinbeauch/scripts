from modules import triggers, mapping, colors, hues


def voice_to_lights(br, word_list):
    word_list = set(word_list.split())
    intersect = list(word_list.intersection(triggers))

    print("Intersect", intersect)

    if len(intersect) == 0:
        return

    word = intersect[0]

    try:
        settings = mapping[word]

        if "battle" in intersect and "over" in intersect:
            br.execute(*mapping['over'])
        else:
            br.execute(*settings)

    except KeyError:
        if word in colors:
            br.saturation(255)
            br.hue(hues[word])
