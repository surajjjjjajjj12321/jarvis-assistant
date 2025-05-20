import os
import sys
import subprocess
import requests
import tempfile
import shutil
import speech_recognition as sr
import pyttsx3

# ======== CONFIGURATION ========
# Replace this URL with your GitHub raw URL after uploading your jarvis.py file there
GITHUB_RAW_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/jarvis.py"
# ==============================

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except Exception:
        return ""

def open_notepad():
    speak("Opening Notepad")
    subprocess.Popen("notepad.exe")

def open_browser():
    speak("Opening default web browser")
    if sys.platform == "win32":
        os.startfile("https://www.google.com")
    else:
        subprocess.Popen(["xdg-open", "https://www.google.com"])

def shutdown_pc():
    speak("Shutting down the computer in 10 seconds. Please save your work.")
    if sys.platform == "win32":
        os.system("shutdown /s /t 10")
    else:
        os.system("shutdown now")

def check_for_update():
    try:
        speak("Checking for updates...")
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code == 200:
            latest_code = response.text
            current_file = os.path.abspath(sys.argv[0])
            with open(current_file, "r", encoding="utf-8") as f:
                current_code = f.read()
            if latest_code != current_code:
                speak("New update found. Updating Jarvis now.")
                # Save new code to a temp file
                temp_dir = tempfile.mkdtemp()
                temp_file = os.path.join(temp_dir, "jarvis_new.py")
                with open(temp_file, "w", encoding="utf-8") as f:
                    f.write(latest_code)
                # Replace current file with new code
                shutil.copy(temp_file, current_file)
                shutil.rmtree(temp_dir)
                speak("Update completed. Restarting Jarvis.")
                # Restart the program
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                speak("Jarvis is up to date.")
        else:
            speak("Failed to check updates from GitHub.")
    except Exception as e:
        speak("Error checking updates.")
        print("Update error:", e)

def jarvis_loop():
    speak("Jarvis activated. How can I help you?")
    while True:
        command = listen()

        if command == "":
            continue

        if "open notepad" in command:
            open_notepad()

        elif "open browser" in command:
            open_browser()

        elif "shutdown" in command:
            shutdown_pc()
            break

        elif "update yourself" in command or "check for update" in command:
            check_for_update()

        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.")

if __name__ == "__main__":
    check_for_update()
    jarvis_loop()
