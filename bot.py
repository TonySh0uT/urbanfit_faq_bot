import gspread
from gspread import Client, Worksheet
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types


SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1V07IpXSkcnDZ6plMYDu8D2P4aGoUnu4MguqA2myLTuE/edit#gid=0"
telegrambot = '6627221249:AAErv5DurpVRQkrwADYsNrn63670Zef0UKI'
bot = AsyncTeleBot(telegrambot)

gc: Client = gspread.service_account("service_account.json")
sh = gc.open_by_url(SPREADSHEET_URL)

wsQuestions: Worksheet = sh.worksheet("Вопросы")
list_of_questions = wsQuestions.get_all_values()[1:]
print(list_of_questions)
print("Questions updated")

wsCategories: Worksheet = sh.worksheet("Категории")
list_of_categories = wsCategories.get_all_values()[1:]
print(list_of_categories)
print("Categories updated")




@bot.message_handler(commands=['start'])
async def handle_message(message):
    print("Message from " + str(message.from_user.id))
    markup = types.InlineKeyboardMarkup()
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark.add("Начать")
    await bot.send_message(chat_id=message.from_user.id, text="Доброго времени суток! 🌗\n\nВ этом боте можно получить актуальные ответы на вопросы о вселенной URBANFIT. Действуй!▶️", reply_markup=mark)
    for category in list_of_categories:
        if (category[1] == ""):
            markup.add(types.InlineKeyboardButton(text="🔘 " + category[0] , callback_data=category[0]))
    await bot.send_message(chat_id=message.from_user.id, text="Выберите категорию:", reply_markup=markup)

@bot.message_handler(commands=['refresh'])
async def handle_message(message):
    if(message.from_user.id == 438991752 or message.from_user.id == 358983633):
        global list_of_questions
        global list_of_categories
        list_of_questions = wsQuestions.get_all_values()[1:]
        list_of_categories = wsCategories.get_all_values()[1:]
        await bot.send_message(chat_id=message.from_user.id, text="Информация обновлена")
    print("Message from " + str(message.from_user.id))




@bot.message_handler(content_types=['text'])
async def handle_message(message):
    if message.text == "Начать":
        print("Message from " + str(message.from_user.id))
        markup = types.InlineKeyboardMarkup()
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark.add("Начать")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Доброго времени суток! 🌗\n\nВ этом боте можно получить актуальные ответы на вопросы о вселенной URBANFIT. Действуй!▶️",
                               reply_markup=mark)
        for category in list_of_categories:
            if (category[1] == ""):
                markup.add(types.InlineKeyboardButton(text="🔘 " + category[0] , callback_data=category[0]))
        await bot.send_message(chat_id=message.from_user.id, text="Выберите категорию:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
async def answer(call):
    markup = types.InlineKeyboardMarkup()
    is_category = False
    is_question = False
    is_categoryBack = False
    is_questionBack = False

    for category in list_of_categories:
        if call.data[:-6] == category[0]:
            is_categoryBack = True
            break
    if not(is_categoryBack):
        for question in list_of_questions:
            if call.data[:-6] == question[0]:
                is_questionBack = True
                break

    for category in list_of_categories:
        if call.data == category[0]:
            is_category = True
            break
    if not(is_category):
        for question in list_of_questions:
            if call.data == question[0]:
                is_question = True
                break

    if (not (is_questionBack) and not (is_categoryBack) and not (is_question) and not (is_category) and not (call.data == "!back!")):
        for category in list_of_categories:
            if (category[1] == ""):
                markup.add(types.InlineKeyboardButton(text="🔘 " + category[0], callback_data=category[0]))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Данного вопроса/категории больше нет.\nВыберите категорию",
                                    reply_markup=markup)
        return

    if(call.data == "!back!"):
        for category in list_of_categories:
            if (category[1] == ""):
                markup.add(types.InlineKeyboardButton(text="🔘 " + category[0], callback_data=category[0]))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Выберите категорию", reply_markup=markup)

    elif(call.data[-6:] == "!back!"):
        calldata = call.data
        while(calldata[-6:] == "!back!"):
            calldata = calldata[:-6]
        for category in list_of_categories:
            target_category = ""
            if (category[0] == calldata):
                target_category = category[1]
                for category in list_of_categories:
                    if (category[1] == target_category):
                        markup.add(types.InlineKeyboardButton(text="🔘 " + category[0], callback_data=category[0]))
                for question in list_of_questions:
                    if (question[1] == target_category):
                        markup.add(types.InlineKeyboardButton(text="☑️️ " + question[0], callback_data=question[0]))
                break
        if(target_category != ''):
            markup.add(types.InlineKeyboardButton(text="Назад", callback_data=call.data + "!back!"))

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Выберите категорию", reply_markup=markup)

    elif(is_category):
        for category in list_of_categories:
            if call.data == category[1]:
                markup.add(types.InlineKeyboardButton(text="🔘 " + category[0], callback_data=category[0]))
        for question in list_of_questions:
            if (call.data == question[1]):
                markup.add(types.InlineKeyboardButton(text="☑️️ " + question[0], callback_data=question[0]))
        if(call.data != ""):
            markup.add(types.InlineKeyboardButton(text="Назад", callback_data= call.data + "!back!"))
        if(len(markup.keyboard) == 1):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="Категория пуста, вернитесь назад", reply_markup=markup)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="Выберите категорию", reply_markup=markup)

    elif(is_question):
        for question in list_of_questions:
            if (call.data == question[0]):
                markup.add(types.InlineKeyboardButton(text="В начало", callback_data="!back!" ))
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=question[2], reply_markup=markup, parse_mode='HTML')
                break
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Информация в боте была обновлена.\nВыберите категорию", reply_markup=markup)

asyncio.run(bot.polling(non_stop=True, request_timeout=90))