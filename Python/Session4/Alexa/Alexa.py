import os
import datetime
import webbrowser
import random
import pygame
import threading
import speech_recognition as sr
from gtts import gTTS
import sys
import pyautogui
import requests
import pyjokes
import openpyxl
from time import sleep
from plyer import notification
import schedule
from googletrans import Translator

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator=Translator()
        schedule.every(60).seconds.do(self.Alexa_Notification)
        threading.Thread(target=self.run_schedule).start()

    def run_schedule(self):
        while True:
            schedule.run_pending()
            sleep(10)

    def speak(self, text, lang='ar'):
        tts = gTTS(text=text, lang=lang)
        filename = "voice.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
        os.remove(filename)

    def record_audio(self,lang="ar-en"):
        with self.microphone as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing...")
                if audio:
                    self.recognizer.adjust_for_ambient_noise(source)
                    try:
                        recognized_text = self.recognizer.recognize_google(audio, language=lang)
                        print(f"Recognized : {recognized_text}")
                        return recognized_text
                    except sr.UnknownValueError:
                        print("Sorry, I didn't catch that. Could you repeat?")
                    except sr.RequestError:
                        print("Service is unavailable. Please try again later.")
                else:
                    print("No audio detected")
            except sr.WaitTimeoutError:
                print("Timeout waiting for audio")
            return ""

    def Alexa_GM(self):
        response = "صباح الفل يبرو"
        self.speak(response, lang='ar')
        return response

    def Alexa_Song(self):
        response = "هختار أغنية من أغانيك المفضلة"
        self.speak(response, lang='ar')
        songList = ["تملي معاك", "بحبه", "حبه جنه", "دي عيله واطيه ونصابه", "هيجيلي موجوع"]

        selected_song = random.choice(songList)
        youtube_url = f"https://www.youtube.com/results?search_query={selected_song}"
        webbrowser.open(youtube_url)
        sleep(5)
        pyautogui.click(553, 565)
        return response

    def Alexa_Time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = "الساعة الآن " + current_time
        self.speak(response, lang='ar')
        return response

    def Alexa_Bye(self):
        response = "مع السلامة يا قلبي"
        self.speak(response)
        sys.exit()
        

    def Alexa_Open_LinkedIn(self):
        webbrowser.open("https://www.linkedin.com/in/anas-kotb-02145a25b/")
        return "فتح لينكد ان"
    def Alexa_WhoIam(self):
        response = "You Are Anas an Embedded Systems Engineer with R&D Team at vision valley Egypt"
        self.speak(response,lang='en')
        return response    

    def Alexa_Joke(self):
        self.speak("هقولك اضحوكه", lang='ar')
        joke = pyjokes.get_joke()
        self.speak(joke, lang='en')
        return joke

    def Alexa_WFH_Email(self):
        response = "حاضر يا باشا"
        self.speak(response)
        sleep(3)
        pyautogui.hotkey('win')
        sleep(3)
        pyautogui.write('outlook')
        sleep(2)
        pyautogui.press('enter')
        sleep(3)
        pyautogui.hotkey('ctrl', 'n')
        sleep(2)
        pyautogui.write('nourhan.shemais@visionvalley.net')
        pyautogui.press('enter')
        pyautogui.click(160, 255)
        sleep(2)
        pyautogui.write('mohamed.saleh@visionvalley.net')
        pyautogui.press('enter')
        sleep(2)
        pyautogui.write('youssef.waleed@visionvalley.net')
        pyautogui.press('enter')
        sleep(1)
        pyautogui.click(197, 286)
        pyautogui.write('WFH')
        pyautogui.press('enter')
        sleep(1)
        pyautogui.click(103, 341)
        pyautogui.write("Dear Nourhan,\n\nKindly note that I will be working from home next Thursday")
        pyautogui.moveTo(34, 249) 
        return response
    def Alexa_Translator(self):
        self.speak(" اختر اللغة الى هتترجم منها ممكن تختار بين عربي او انجليزي")
        while True:
            text = self.record_audio()          
            if(text == "عربي"):
                self.speak("اتفضل اتكلم و انا هترجم للإنجليزية")
                arabic_sentence = self.record_audio('ar')
                translated_sentence = self.translator.translate(arabic_sentence,dest="en").text
                self.speak(translated_sentence)
                return translated_sentence
                break
            elif(text == "انجليزي"):
                self.speak("اتفضل اتكلم و انا هترجم للعربية")
                English_sentence = self.record_audio('en')
                translated_sentence = self.translator.translate(English_sentence,dest="ar").text
                self.speak(translated_sentence)
                return translated_sentence
                break
            else:
                self.speak(" مفهمتش قول تاني") 
    def Alexa_Weather(self):
        City = "Cairo"
        api_key = "fae4e4336c31fe86cbbcc17161fec8e5" # Replace with your actual OpenWeatherMap API key
        url = "http://api.openweathermap.org/data/2.5/weather?q=Cairo&appid=fae4e4336c31fe86cbbcc17161fec8e5&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors
            weather = response.json()
            if "weather" not in weather or "main" not in weather:
                raise ValueError("Incomplete weather data received")

            weather_description_en = weather["weather"][0]["description"]
            weather_description_ar = self.translator.translate(weather_description_en, dest="ar").text
            temperature = weather["main"]["temp"]
            humidity = weather["main"]["humidity"]
            weather_report = (f"الجو دلوقتي {weather_description_ar}, و الحرارة دلوقتي {temperature} درجة, "
                              f"و الرطوبة برضو {humidity} في الميه")
            self.speak(weather_report, lang='ar')
            return weather_report
        except requests.exceptions.RequestException as e:
            error_message = f"HTTP error occurred: {e}"
            print(error_message)
            self.speak("حدث خطأ أثناء جلب بيانات الطقس", lang='ar')
            return error_message
        except ValueError as e:
            error_message = f"Data error occurred: {e}"
            print(error_message)
            self.speak("حدث خطأ أثناء جلب بيانات الطقس", lang='ar')
            return error_message
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            self.speak("حدث خطأ أثناء جلب بيانات الطقس", lang='ar')
            return error_message
    def Alexa_GoogleSearch(self):
        self.speak("What do you want to search for on Google?", lang='en')
        query = self.record_audio(lang='en')
        
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            response = f"Searching Google for: {query}"
            self.speak(response, lang='en')
            return response
        else:
            error_message = "Failed to capture search query"
            self.speak(error_message, lang='en')
            return error_message
    def respond(self, text):
        print(f"Responding to: {text}")
        if self.search_word_in_string(["hello","صباح", "الخير", "صباحو", "اهلا"], text):
            return self.Alexa_GM()
        if self.search_word_in_string(["who","me","introduce ", "عرفيني", "انا مين", "مين"], text):
            return self.Alexa_WhoIam()
        elif self.search_word_in_string(["الساعه", "وقت", "ساعه", "الساعه كم"], text):
            return self.Alexa_Time()
        elif self.search_word_in_string(["متضايق", "انا متضايق", "ضحكيني", "قوليلي نكته", "نكته"], text):
            return self.Alexa_Joke()
        elif self.search_word_in_string(["مع السلامه", "سلامه", "سلام", "باي"], text):
            return self.Alexa_Bye()
        elif self.search_word_in_string(["افتحي لينكد ان","linkedin", "لينكد ان", "لينكد"], text):
            return self.Alexa_Open_LinkedIn()
        elif self.search_word_in_string(["Work from home", "اشتغل من البيت", "البيت", "ابعت", "ميل"], text):
            return self.Alexa_WFH_Email()
        elif self.search_word_in_string(["song","شغليلي اغنيه", "شغلي اغنيه", "ليست", "بلاي", "اغنيه"], text):
            return self.Alexa_Song()
        elif self.search_word_in_string(["الطقس", "الجو", "ويزر", "الحراره"], text):
            return self.Alexa_Weather()
        elif self.search_word_in_string(["google", "جوجل"], text):
            return self.Alexa_GoogleSearch()
        elif(self.search_word_in_string(["translate","تترجملي","اترجم"],text)):
            self.Alexa_Translator()
        else:
            self.speak("عيد تاني معلش.", lang='ar')
            return "عيد تاني معلش."
    
    def search_word_in_string(self, words, text):
        return any(word in text for word in words)

    def Alexa_Excel_Record(self, command, response):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            workbook = openpyxl.load_workbook('LOGS.xlsx')
            sheet = workbook['LOGS']
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = 'LOGS'
            sheet.append(['Time', 'Command', 'Response'])

        sheet.append([current_time, command, response])
        workbook.save('LOGS.xlsx')

    def Alexa_Notification(self):
        notification.notify(
            title="Reminder",
            message="صلي علي النبي ",
            timeout=60
        )
        self.Alexa_Excel_Record("Alexa Notification", "Notification: This is your 10-second reminder!")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.speak("Alexa is Ready", lang='en')
    while True:
        command = assistant.record_audio('ar-en')
        if command:
            response = assistant.respond(command)
            assistant.Alexa_Excel_Record(command, response)
