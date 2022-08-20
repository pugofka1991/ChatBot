import datetime

from dal import DateBase
from telebot import custom_filters
import telebot
from telebot.storage import StateMemoryStorage

from gateway import get_week_days, get_objects_response, get_ticket_list, get_booking_text, select, get_types_markup, cancel
from state import User, Booking


def main():
    state_storage = StateMemoryStorage()
    bot = telebot.TeleBot("5349004299:AAFKlLWtsTVuohgxyM_5UF6vTrq7B1K5yE4",
                          state_storage=state_storage)
    db = DateBase('localhost', 'root', 'root', 'book_21')

    @bot.message_handler(commands=["start"])
    def start(m):
        bot.set_state(m.from_user.id, User.login, m.chat.id)

        bot.send_message(m.chat.id, 'Введите логин')

    @bot.message_handler(state="*", commands=['back'])
    def any_state(message):
        """
        Cancel state
        """
        bot.send_message(message.chat.id, "Your state was cancelled.")
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=User.login)
    def login_step(m):
        if db.value_exists('login', m.text):
            bot.send_message(m.chat.id, 'Введите пароль')
            bot.set_state(m.from_user.id, User.password, m.chat.id)
        else:
            bot.reply_to(m, 'Неверный ')
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data['login'] = m.text
            data['id'] = db.get_user_id_by_login(m.text)[0][0]

    @bot.message_handler(state=User.password)
    def password_step(m):
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            authorized = False
            if db.confirm_password(m.text, data['login']):
                authorized = True
            else:
                bot.reply_to(m, 'Неверный пароль')

            is_admin = db.get_field_from_row('admin', 'login', data['login'])

            if authorized:

                markup = select(is_admin, data['id'])

                bot.send_message(m.chat.id, f"Привет, <b>{data['login']}</b> !", parse_mode='html', reply_markup=markup)
                data['is_authorized'] = authorized
                data['is_admin'] = is_admin
                data['campus'] = db.get_field_from_row('campus', 'login', data['login'])
        bot.set_state(m.from_user.id, Booking.select, m.chat.id)

    @bot.callback_query_handler(lambda query: query.data.startswith("create"))
    def callback_create(query):
        objects_types = db.get_objects_types()
        objects_types_markup = get_types_markup(objects_types, query.data.split('_')[1], query.data.split('_')[2])
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=objects_types_markup)

    @bot.callback_query_handler(lambda query: query.data.startswith("show"))
    def callback_show(query):
        id, is_admin = int(query.data.split('_')[1]), int(query.data.split('_')[2])
        bookings = db.get_user_bookings(id)
        idx = "_".join([str(i[0]) for i in bookings])
        response = get_booking_text(bookings)
        bot.send_message(query.message.chat.id, response, reply_markup=cancel(is_admin, id, idx))
        

    @bot.callback_query_handler(lambda query: query.data.startswith("back"))
    def callback_show(query): 
        id, is_admin = int(query.data.split('_')[1]), int(query.data.split('_')[2])
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=select(is_admin, id))


    def date_chose(m, objects):
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            markup = select(data['is_admin'], data['id'])
            try:
                object_num = int(m.text)
                if object_num <= 0 or object_num > db.get_object_by_id(objects[object_num - 1][0])[0][0]:
                    raise Exception
                data['object_num'] = objects[object_num - 1][0]
                response = get_week_days()
                msg = bot.send_message(m.chat.id, response)
                bot.register_next_step_handler(msg, chose_booking)
            except:
                bot.send_message(m.chat.id, f"Что-то не так уж точно", parse_mode='html', reply_markup=markup)

            
    def chose_booking(m):
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            markup = select(data['is_admin'], data['id'])
            try:
                date = int(m.text)
                if date >= 8 or date <= 0:
                    raise Exception
                date = datetime.date.today() + datetime.timedelta(days=date - 1)
                data['date'] = date
                tickets = db.get_tickets(data['object_num'], date)
                response, tickets_list = get_ticket_list(tickets)
                data['tickets_list'] = tickets_list
                msg = bot.send_message(m.chat.id, response)
                bot.register_next_step_handler(msg, set_booking)
            except:
                bot.send_message(m.chat.id, f"Что-то не так уж точно", parse_mode='html', reply_markup=markup)
            
    def set_booking(m):
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            ticket = 0
            markup = select(data['is_admin'], data['id'])
            try:
                ticket = int(m.text)
                if not (0 < ticket < len(data['tickets_list']) + 1):
                    raise Exception
                db.set_booking(data['id'], data['object_num'], data['date'], data['tickets_list'][ticket - 1])
                markup = select(data['is_admin'], data['id'])
                bot.send_message(m.chat.id, f"Бронь успешно создана!!!", reply_markup=markup)
            except:
                bot.send_message(m.chat.id, f"Что-то не так уж точно", parse_mode='html', reply_markup=markup)

            

    @bot.callback_query_handler(lambda query: query.data.startswith('type'))
    def callback_create(query):
        objects = db.get_objects_by_id(int(query.data.split('_')[1]))
        msg = bot.send_message(query.message.chat.id, get_objects_response(objects))
        bot.register_next_step_handler(msg, date_chose, objects)

    @bot.callback_query_handler(lambda query: query.data.startswith('cancel'))
    def callback_cancel(query):
        bookings = query.data.split('_')[1:]
        print(bookings)
        msg = bot.send_message(query.message.chat.id, "Выберите бронирование")
        bot.register_next_step_handler(msg, drop_booking, bookings)

    def drop_booking(m, bookings):
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            booking_id = 0
            markup = select(data['is_admin'], data['id'])
            try:
                booking_id = int(m.text)
                if len(bookings) >= booking_id and booking_id > 0:
                    db.drop_booking(bookings[booking_id - 1])
                    bot.send_message(m.chat.id, f"Бронь успешно удалена!!!", parse_mode='html', reply_markup=markup)
                else:
                    raise Exception
            except:
                bot.send_message(m.chat.id, f"Что-то не так уж точно", parse_mode='html', reply_markup=markup)


    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())

    bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    main()
