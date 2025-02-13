from aiogram.fsm.state import State, StatesGroup


#user

class Help(StatesGroup):
    default = State()
    message = State()


#admin

class CreateCase(StatesGroup):
    default = State()
    name = State()
    content = State()


class EditCase(StatesGroup):
    default = State()
    choice = State()
    content = State()


class DeleteCase(StatesGroup):
    default = State()
    deleting = State()


class ReplySupport(StatesGroup):
    default = State()
    reply = State()


class Mailing(StatesGroup):
    default = State()
    sending = State()