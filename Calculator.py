import speech_recognition as sr
import pyttsx3
from word2number import w2n

# Initialize TTS engine globally
engine = pyttsx3.init()

def speak_text(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def get_voice_input(prompt):
    """Get voice input from the user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak_text(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Improve recognition
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the request.")
            return None

def get_input(prompt):
    """Allow user to choose between voice and text input"""
    print(f"{prompt} (You can type or speak)")
    speak_text(f"{prompt}. You can type or speak.")

    user_choice = input("Type 'T' to type or press Enter to use voice: ").strip().lower()
    
    if user_choice == "t":
        return input(f"{prompt}: ").strip().lower()
    else:
        return get_voice_input(prompt)

def get_valid_number(prompt):
    """Get a valid number from the user, allowing voice or manual input"""
    attempts = 1  # Allow one voice attempt, then fallback to typing
    for _ in range(attempts):
        value = get_input(prompt)
        if value in ["exit", "quit"]:
            speak_text("Exiting calculator.")
            exit()
        if value is not None:
            try:
                return w2n.word_to_num(value)  # Convert spoken words to numbers
            except ValueError:
                print("That doesn't seem like a valid number. Please try again.")

    # If voice fails, allow manual input
    while True:
        try:
            value = input(f"{prompt} (or type it): ")
            if value.lower() in ["exit", "quit"]:
                speak_text("Exiting calculator.")
                exit()
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def calculator():
    while True:
        operations = {
            "add": "+",
            "subtract": "-",
            "multiply": "*",
            "divide": "/"
        }

        print("\nSay or type 'add', 'subtract', 'multiply', or 'divide' to choose an operation.")
        speak_text("Say or type 'add', 'subtract', 'multiply', or 'divide' to choose an operation.")

        operation = None
        while operation not in operations:
            operation = get_input("Select the operation you want to perform")
            if operation in ["exit", "quit"]:
                speak_text("Exiting calculator.")
                exit()
            if operation not in operations:
                print("Invalid choice, please try again.")

        n = get_valid_number("Enter your first number:")
        n1 = get_valid_number("Enter your second number:")

        try:
            result = eval(f"{n} {operations[operation]} {n1}")
            response = f"The result of {n} {operations[operation]} {n1} is: {result}"
        except ZeroDivisionError:
            response = "Division by zero is not allowed."

        print(response)
        speak_text(response)

        # Ask if the user wants to continue
        print("\nDo you want to perform another calculation? (Say or type 'yes' or 'no')")
        speak_text("Do you want to perform another calculation? Say or type yes or no.")

        continue_response = None
        while continue_response not in ["yes", "no"]:
            continue_response = get_input("Say yes to continue or no to exit")
            if continue_response in ["exit", "quit"]:
                speak_text("Goodbye!")
                exit()
            if continue_response not in ["yes", "no"]:
                print("Invalid response. Please say or type yes or no.")

        if continue_response == "no":
            speak_text("Goodbye!")
            print("Goodbye!")
            break  # Exit the loop and end the program

if __name__ == "__main__":
    calculator()
