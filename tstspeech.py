import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Start loop for continuous recognition
while True:
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)  # Capture audio

    # Convert speech to text using Google Speech API
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")

