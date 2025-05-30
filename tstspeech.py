import speech_recognition as sr

recognizer = sr.Recognizer()

# Select the correct microphone (usually index 0)
with sr.Microphone(device_index=0) as source:
    print("Listening... Speak now.")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError as e:
    print("Sorry, I couldn't understand that.\t"+ e)
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")
