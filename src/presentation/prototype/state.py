from telebot.handler_backends import State, StatesGroup


class User(StatesGroup):
    login = State()
    name = State()
    campus = State()
    is_admin = State()
    is_authorized = State()
    password = State()


class Booking(StatesGroup):
    date = State()
    select = State()
    booking = State()
    set_booking = State()

class UserBooking(StatesGroup):
    login = State()
    object = State()
    date = State()
    time = State()


# class Booking(StatesGroup):
 
#     def __init__(self, login):
#         self.login = login    # имя человека
#         date = State()
#         select = State()
#         booking = State()
#         set_booking = State()

        
