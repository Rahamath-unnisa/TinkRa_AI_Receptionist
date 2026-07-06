import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
                       print("🎤 Microphone Opened")

                       recognizer.adjust_for_ambient_noise(source, duration=0.5)

                       print("🎙 Speak now...")

                       audio = recognizer.listen(source)

                       print("✅ Audio Captured")

        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""

    except Exception as e:
        print("Voice Error:", e)
        return ""