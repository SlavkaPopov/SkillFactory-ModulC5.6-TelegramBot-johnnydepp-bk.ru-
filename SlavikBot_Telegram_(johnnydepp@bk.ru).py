import telebot
from BotUnits import TOKEN, currency
from Extensions import CurrencyConverter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_welcome(message):
    text_start = f"Добро пожаловать, {message.chat.username}\n \
При работе Бота используются следующие команды:\n \
/start - вывод данного сообщения повторно;\n \
/help - помощь при работе с Ботом;\n \
/values - вывод списка доступных для конвертации валют;\n \
/about - вывод информации о программе."
    bot.send_message(message.chat.id, text_start)


@bot.message_handler(commands=['help'])
def send_help(message):
    text_help = f"Я умею конвертировать одну валюту в другую, если сделать соответствующий запрос:\n \
[Исходная валюта] [Конвертируемая валюта] [Количество исходной валюты]\n \
При вводе команды /values можно узнать список доступных валют для конвертации"
    bot.send_message(message.chat.id, text_help)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Валюты, доступные для конвертации:"
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['about'])
def about(message: telebot.types.Message):
    text = "Программа-бот разработана в рамках обучения в SkillFactory, Профессия Python-разработчик. \
Автор: Вячеслав Попов (johnnydepp@bk.ru) - группа PDEV-16. Задание Модуля C5.6."
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')

        if len(values_) != 3:
            raise APIException(bot.reply_to(message, "Введены не верные параметры. Введите запрос заново."))

        quote, base, amount = values_
        answer = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка ввода данных. Введите запрос заново.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка обработки данных. Попробуйте позднее.\n{e}")
    else:
        text = f"По Вашему запросу получена информация:\n \
Стоимость {amount} {quote} составляет {answer} {base}"
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['photo'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, f'{message.chat.username}, это хорошая фотография, но я еще не умею с ними работать ХDD')


bot.polling(non_stop=True)
