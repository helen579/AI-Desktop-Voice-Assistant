import pyttsx3 #Converts text to speech
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

dict = {'helen':'helenmvdelhi@gmail.com','dhwani':'dhwani.apurva@btech.christuniversity.in', 'sagar':'sagarkc9999@gmail.com'}

engine = pyttsx3.init('sapi5') #To take voice input(Microsoft speech API)
voices = engine.getProperty('voices') #To set voice 
#print(voices[1].id)
engine.setProperty('voice', voices[1].id) #Apply 0 instead of 1 for male voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait() #without this speech will not be audible to us

def wishMe():  #It will wish according to the time
    hour = int(datetime.datetime.now().hour) #current time
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Evening!")

    speak("I am Siri, houw may I help you!")

def takeCommand():   
    #Microphone() helps to take input from the user and returns string output
    #Recognizer will help us to recognize the audio. 
    #if you want the the sysem to avoid unnecessary voices then increase the energy_threshold value from the recognizer class(library)
    #Takes 1 sec gap to take the input of users voice i.e., lets the user complete his command

    r = sr.Recognizer()
    r.energy_threshold = 300
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8 
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")  #To recognize the users voice to avoid any error
        query = r.recognize_google(audio)
        print(f"User said: {query}\n") #or print("User said: ", query) this has used fstring

    except Exception as e:   #Applies if it didnt recognize the voice
        #print(e) dont show the error
        print("Say that again please...")
        return "None"  #returning string none
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)  #Creating a SMTP object for connection with server
    server.ehlo()
    server.starttls() #TLS connection required by gmail
    server.login('helen.mary@btech.christuniversity.in', '48830951')
    server.sendmail('sender@gmail.com', to, content) 
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:   
        query = takeCommand().lower()

        #logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query= query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=1)
            speak("According to wikepedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'list my folders' in query:
            folder_dir = 'D:\\'
            folder = os.listdir(folder_dir)
            print(folder)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Maam, the time is {strTime}")

        elif 'open visual studio code' in query:
            vspath = "C:\\Users\\acer\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
            os.startfile(vspath)

        elif 'send email' in query:
            try: 
                name = list(query.split()) # extract receiver's name ...one should say 'send email to persons name'
                name = name[name.index('to')+1]
                speak("What should I say?")
                content = takeCommand().lower()
                print("content:", content)
                to = dict[name]
                sendEmail(to, content)
                speak("Email sent successfully!")
                print("Email sent successfully!\n")

            except Exception as e:
                print(e)
                speak("Sorry my friend, I am not able to send this email")
        
        elif 'exit' in query:
            exit(0)

