#Скрипт который держит бота включенным (лучше не трогать)
from flask import Flask #Модуль Flask
from flask import request #Модуль запросов
from threading import Thread #Модуль для запуска бота в отдельном потоке
import time
import requests


app = Flask('') #Создание экземпляра Flask

@app.route('/') #Декоратор для обработки запросов
def home(): 
  return "Я тут в соло сервер держу ^_^, приходи ещё! :3" #Главная страница

def run():
  app.run(host='0.0.0.0', port=80) 

def keep_alive(): #Функция запуска бота в отдельном потоке
  t = Thread(target=run)
  t.start()