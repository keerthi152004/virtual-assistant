import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
import wikipedia

# Initialize the recognizer and the text-to-speech engine
r = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Speak the given text."""
    machine.say(text)
    machine.runAndWait()

def get_instruction():
    """Listen for a voice command and return it."""
    try:
        with sr.Microphone(device_index=0) as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            speech = r.listen(source)
            instruction = r.recognize_google(speech)
            instruction = instruction.lower()
            print("Instruction heard: ", instruction)
            if "john" in instruction:
                instruction = instruction.replace('john', "").strip()
                return instruction
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def play_instruction():
    """Process the instruction and take action based on it."""
    instruction = get_instruction()
    if instruction:
        print("Processed instruction: ", instruction)
        if "play" in instruction:
            song = instruction.replace('play', "").strip()
            talk("Playing " + song)
            pywhatkit.playonyt(song)
            # Wait for some time to ensure the command is executed
            time.sleep(10)
        elif 'time' in instruction:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time_now)
            print('The current time is ' + time_now)
        elif 'day' in instruction:
            day_now = datetime.datetime.now().strftime('%A')
            talk('Today is ' + day_now)
            print('Today is ' + day_now)
        elif 'stop' in instruction:
            talk('Stopping the program')
            return False  # Signal to stop the loop
        elif 'information' in instruction:
            query = instruction.replace('information', "").strip()
            talk('Searching for information about ' + query)
            try:
                summary = wikipedia.summary(query, sentences=2)
                talk(summary)
                print("Information about " + query + ": " + summary)
            except wikipedia.exceptions.DisambiguationError as e:
                talk('There are multiple results for this query. Please be more specific.')
                print('There are multiple results for this query. Please be more specific.')
            except wikipedia.exceptions.PageError:
                talk('No information found for ' + query)
                print('No information found for ' + query)
        else:
            talk("I didn't understand that command.")
            print("I didn't understand that command.")
    else:
        talk("No valid instruction received.")
        print("No valid instruction received.")
    return True  # Continue the loop

# Main loop to keep listening for commands
if __name__ == "__main__":
    listening = True
    while listening:
        listening = play_instruction()
