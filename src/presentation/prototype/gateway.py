import datetime
from operator import is_
from telebot import types

week_days = {
    1: 'Понедельник',
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}

def get_week_days():
    today_week_day = int(datetime.datetime.today().weekday()) + 1
    today_date = datetime.datetime.today().date()
    response = "Выберите день:\n"
    for i in range(1, 8, 1):
        response += f"{i} {week_days[today_week_day]} {str(today_date)}\n"
        today_week_day += 1
        today_date += datetime.timedelta(days=1)
        if today_week_day >= 8:
            today_week_day %= 7
    return response


def get_objects_response(objects):
    response = "Выберите объект:\n"
    i = 1
    for object in objects:
        response += f"{i}. \"{object[2]}\" этаж: {object[4]} комната: {object[5]}\n"
        i += 1
    return response


def get_ticket_list(tickets):
    time = datetime.timedelta(seconds=0)
    available = True
    response = "Свободные брони:\n"
    tickets_dates = []
    step = 1
    for i in range(1, 25, 1):
        for ticket in tickets:
            if ticket[3] == time:
                available = False
        if available:
            tickets_dates.append(time)
            response += f"{str(step)}. {time.seconds // 3600}:{(time.seconds//60) % 60}0\n"

            step += 1
        else:
            available = True
        time += datetime.timedelta(hours=1)

    return response, tickets_dates


def get_booking_text(bookings):
    response = "Ваши бронирования:\n"
    for i in range(len(bookings)):
        response += f"{i + 1}. {bookings[i][7]} {bookings[i][4]} {bookings[i][3]}\n"
    return response
  

def select(is_admin, id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_create = types.InlineKeyboardButton(text = 'Создать бронь', callback_data = 'create_' + str(id) + "_" + str(is_admin))
    button_show = types.InlineKeyboardButton(text = 'Показать бронь', callback_data = 'show_' + str(id) + "_" + str(is_admin))
    button_admin = types.InlineKeyboardButton(text = 'Режим АДМ', callback_data = 'admin')
    markup.add(button_create, button_show)
    if is_admin:
        markup.add(button_admin)
    return markup

def get_types_markup(objects_types, id, is_admin):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for type in objects_types:
        button = types.InlineKeyboardButton(text = type[1], callback_data = "type_"+str(type[0]))
        markup.add(button)
    # ксюша - лучшая!!!!
    button = types.InlineKeyboardButton(text="Назад", callback_data="back_" + str(id) + "_" + str(is_admin))
    markup.add(button)
    return markup
    
def get_types_markup_time():
    markup = types.InlineKeyboardMarkup(row_width=4)
    for time in range(1, 7, 1) :
        button1 = types.InlineKeyboardButton(text = str((time - 1) * 4) + ":00", callback_data="set " +str((time - 1) * 4))
        button2 = types.InlineKeyboardButton(text = str((time - 1) * 4 + 1) + ":00", callback_data="set " + str((time - 1) * 4 + 1))
        button3 = types.InlineKeyboardButton(text = str((time - 1) * 4 + 2) + ":00", callback_data="set " + str((time - 1) * 4 + 2))
        button4 = types.InlineKeyboardButton(text = str((time - 1) * 4 + 3) + ":00", callback_data="set " + str((time - 1) * 4 + 3))
        markup.row(button1, button2, button3, button4)
    return markup


def cancel(is_admin, id, idx):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_cancel = types.InlineKeyboardButton(text='Отменить бронь', callback_data='cancel_' + idx)
    button_back = types.InlineKeyboardButton(text='Назад', callback_data='back_' + str(id) + "_" + str(is_admin))
    markup.add(button_cancel)
    markup.add(button_back)
    return markup
