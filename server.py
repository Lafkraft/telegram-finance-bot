"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os
import telebot
from telebot import types
from telebot import apihelper
import exceptions
import expenses
from categories import Categories

# from middlewares import AccessMiddleware
# dp.middleware.setup(AccessMiddleware(ACCESS_ID))

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
apihelper.proxy = {'https': PROXY_URL}
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    """Отправляет приветственное сообщение и помощь по боту"""
    if not checkuserid(message):
        return
    bot.send_message(message.from_user.id,
                     "Бот для учёта финансов\n\n"
                     "Добавить расход: 250 такси\n"
                     "Сегодняшняя статистика: /today\n"
                     "За текущий месяц: /month\n"
                     "Последние внесённые расходы: /expenses\n"
                     "Категории трат: /categories"
                     )

@bot.message_handler(commands=['categories'])
def categories_list(message):
    """Отправляет список категорий расходов"""
    if not checkuserid(message):
        return
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    bot.send_message(message.from_user.id, answer_message)

@bot.message_handler(commands=['today'])
def today_statistics(message):
    """Отправляет сегодняшнюю статистику трат"""
    if not checkuserid(message):
        return
    answer_message = expenses.get_today_statistics()
    bot.send_message(message.from_user.id, answer_message)

@bot.message_handler(commands=['month'])
def month_statistics(message):
    """Отправляет статистику трат текущего месяца"""
    if not checkuserid(message):
        return
    answer_message = expenses.get_month_statistics()
    bot.send_message(message.from_user.id, answer_message)

@bot.message_handler(commands=['expenses'])
def list_expenses(message):
    """Отправляет последние несколько записей о расходах"""
    if not checkuserid(message):
        return
    last_expenses = expenses.last()
    if not last_expenses:
        bot.send_message(message.from_user.id, "Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{row['amount']} руб. на {row['category_name']} —  нажми "
        f"/del{row['id']} для удаления"
        for row in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* ".join(last_expenses_rows)
    bot.send_message(message.from_user.id, answer_message)

@bot.message_handler(content_types=['text'])
def add_expense(message):
    """Добавляет новый расход"""
    if not checkuserid(message):
        return
    if message.text.startswith('/del'):
        del_expense(message)
        return
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        bot.send_message(message.from_user.id, str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    bot.send_message(message.from_user.id, answer_message)

def del_expense(message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    bot.send_message(message.from_user.id, answer_message)

def checkuserid(message):
    res = int(message.from_user.id) == int(ACCESS_ID)
    if not res:
        bot.send_message("Access Denied")
    return res

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)