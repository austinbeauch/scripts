import speech_recognition as sr
import modules.bridge as bridge
import modules.voice_to_lights as vtl

if __name__ == "__main__":
    br = bridge.Bridge()
    r = sr.Recognizer()
    m = sr.Microphone()
    try:
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            with m as source:
                audio = r.listen(source)
            print("Recognizing")
            try:
                value = r.recognize_google(audio)
                print("You said {}".format(value))
                vtl.voice_to_lights(br, value)

            except (sr.UnknownValueError, sr.RequestError):
                print("Error recognizing")
                pass

    except KeyboardInterrupt:
        pass
