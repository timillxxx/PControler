import os
import telebot
import tempfile
from PIL import ImageGrab
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pyaudio
import wave
import datetime
import pyautogui
import urllib.request
from io import BytesIO
from PIL import Image
import winsound

with open("token.txt", "r") as file:
    bot_token = file.read().strip()

bot = telebot.TeleBot(bot_token)

now = datetime.datetime.now()
weekday = now.strftime('%A')
day = now.day
month = now.strftime('%B')
year = now.year

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📸 Получить скриншот")
    markup.add("🔋 Выключить")
    markup.add("⏳ Перезагрузить")
    markup.add("💤 Спящий режим")
    markup.add("📩 Отправить сообщение")
    markup.add("🎤 Записать 15 с записи микрофона")
    bot.send_message(message.chat.id, f" Привет хозяин \nСегодня {weekday}, {day} {month} {year} года", reply_markup=markup)

@bot.message_handler(regexp='выключить')
def echo_message(message):
    bot.send_message(message.chat.id, '✅ Выключаю...')
    os.system("shutdown -s -t 0")

@bot.message_handler(regexp='получить скриншот')
def echo_message(message):
    path = tempfile.gettempdir() + 'screenshot.png'
    screenshot = ImageGrab.grab()
    screenshot.save(path, 'PNG')
    bot.send_photo(message.chat.id, open(path, 'rb'))

@bot.message_handler(regexp='перезагрузить')
def echo_message(message):
    bot.send_message(message.chat.id, '✅ Перезагружаю...')
    os.system("shutdown /r /t 0")

@bot.message_handler(regexp='спящий режим')
def echo_message(message):
    bot.send_message(message.chat.id, '✅ Перевожу в спящий режим...')
    os.system("shutdown /h")

@bot.message_handler(regexp='отправить сообщение')
def echo_message(message):
    bot.send_message(message.chat.id, '✅ Открываю...')
    path = r'"C:\Users\timillxxx\Desktop\5789347896523\123123.vbs"'
    os.startfile(path)

def record_audio(duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

    audio = pyaudio.PyAudio()

    # Создание потока для записи аудио
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Запись аудио...")

    frames = []

    # Записываем аудио
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Аудио записано.")

    # Остановка потока
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Сохраняем аудио в файл
    wf = wave.open("audio.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🎤 Записать 15 с записи микрофона":
        bot.send_message(message.chat.id, '⏳ Записываю аудио...')
        # Записываем аудио
        record_audio(15)
        bot.send_message(message.chat.id, '✅ Аудио записано.')

        # Отправляем аудио в Telegram
        audio = open('audio.wav', 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()

bot.infinity_polling()
