import speech_recognition as sr


def diagnose_ears():
    print("--- AUDITORY DIAGNOSTIC ---")
    r = sr.Recognizer()

    print("\n1. Listing available Audio Devices:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"   [{i}] {name}")

    print("\n2. Attempting to calibrate for ambient noise... (Please stay silent)")
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("   Calibration successful.")

            print("\n3. Listening for a test phrase... (Please say 'Testing Christin')")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("   Audio captured. Sending to Google for translation...")

            text = r.recognize_google(audio)
            print(f"   Success! I heard: '{text}'")

    except sr.WaitTimeoutError:
        print("   Error: Listening timed out. I didn't hear anything.")
    except sr.RequestError as e:
        print(
            f"   Error: Could not request results from Google Speech Recognition service; {e}")
    except sr.UnknownValueError:
        print("   Error: Google Speech Recognition could not understand the audio.")
    except Exception as e:
        print(f"   Unexpected Error: {e}")


if __name__ == "__main__":
    diagnose_ears()
