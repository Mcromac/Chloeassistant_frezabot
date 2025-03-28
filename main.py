#Главный скрипт
import telebot  # Telegram API
import time
from telebot import types  #Модуль для создания клавиатуры(кнопок в боте)
from background import keep_alive  #Ссылка на сервер для бота
from random import randint
import os
import google.generativeai as genai  #ИИ от гугла

AIon = True  #Модуль ИИ вкл\выкл
DisableRole = False  #Отключенить рп

bottoken = os.getenv("BotToken")  #Токен бота
aitoken = os.getenv("AIToken")  #Токен ИИ

bot = telebot.TeleBot(bottoken)  #Создание экземпляра бота
genai.configure(api_key=aitoken)
model = genai.GenerativeModel('gemini-2.0-flash')  #Модель ИИ
print("Bot Started")


def tgprint(
    chatid, text,
    markup):  #Функция для отправки сообщений в телеграм (для упрощения кода)
  if markup is None:
    return bot.send_message(chatid, text)
  else:
    return bot.send_message(chatid, text, reply_markup=markup)


def gethist(chatid):  #Функция для получения истории сообщений
  if not os.path.exists(f"botusers/{chatid}.txt"):
    open(f"botusers/{chatid}.txt", "w")
    return [
      {'role':"user",
       'parts':[open("Personalityprompt.txt", "r").read()]},
      {'role':"model",
       'parts':["Хорошо"]}]

  else:
    histfile = open(f"botusers/{chatid}.txt", "r")
    hist = histfile.read()
    histfile.close()
    hist = hist.split("[LINESSEPARATOR]")
    class msg():
      def __init__(self,role,text):
        self.role = role
        self.parts = text  
    messages = []
    for i in range(len(hist)-1):
      thismessage = hist[i].split("[STRINGSEPARATOR]")
      print(thismessage)
      messages.append({'role':thismessage[0],
           'parts':[thismessage[1]]})
    return messages


class user():  #Класс для хранения данных пользователя

  def __init__(self, id):
    self.id = id


class message():  #Класс для хранения данных сообщения

  def __init__(self, text, frmus):
    self.text = text
    self.from_user = frmus

banlist = [""]  #Список забаненных пользователей




def aimodule(chatid, prompt):
  chat = model.start_chat(history=gethist(chatid))
  response = chat.send_message(prompt, stream=True)
  msg = tgprint(chatid, "Секунду...","")
  time.sleep(0.3)
  responsestr = ""
  for chunk in response:
    print(chunk.text)
    responsestr += chunk.text
    bot.edit_message_text(responsestr, chatid, msg.message_id)
  histfile = open(f"botusers/{chatid}.txt", "r+")
  historystr = ""
  for message in chat.history: 
    historystr += message.role + "[STRINGSEPARATOR]" + message.parts[0].text + "[LINESSEPARATOR]"
  histfile.write(historystr)
  histfile.close()


@bot.message_handler(content_types=['text'])
def get_text_messages(
    message):  #Обработка полученного от пользователя сообщения
  if  message.from_user.id not in banlist:
    if message.text == "/start" or message.text == " ":  #Если пользователь написал /start
      chatid = message.from_user.id
      print(chatid)
    else:
      if AIon:  #Если ИИ включена
        chatid = message.from_user.id
        aimodule(chatid, message.text)  
  else:
    tgprint(message.from_user.id, "Вы забанены :(",
            "")  #Если пользователь забанен


keep_alive()  #Запуск сервера
bot.polling(none_stop=True, interval=1)  #Бесконечный цикл