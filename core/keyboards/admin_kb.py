from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core.db.case_content import get_case_content


def generate_kb_func(case_name):
    data = get_case_content(case_name=case_name)

    lst = []

    for info in data:
        button = InlineKeyboardButton(text=f'{info[0]}', callback_data=f'id={info[3]}')
        lst.append([button])
    
    button = InlineKeyboardButton(text='Назад', callback_data='cancel_from_edit_case')
    lst.append([button])

    new_kb = InlineKeyboardMarkup(inline_keyboard=lst)

    return new_kb










admin_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Заявки на вывод',
                callback_data='withdraw_requests'
            )
        ],
        [
            InlineKeyboardButton(
                text='Кейсы',
                callback_data='case_button'
            )
        ],
        [
            InlineKeyboardButton(
                text='Начать рассылку',
                callback_data='start_mailing'
            )
        ],
        [
            InlineKeyboardButton(
                text='Обращения в поддержку',
                callback_data='support_requests'
            )
        ]
    ]
)


support_check_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Ответить',
                callback_data='reply_support'
            )
        ],
        [
            InlineKeyboardButton(
                text='Просмотрено',
                callback_data='looked'
            )
        ],
        [
            InlineKeyboardButton(
                text='⏪',
                callback_data='left_support'
            ),
                        InlineKeyboardButton(
                text='Меню',
                callback_data='cancel'
            ),
            InlineKeyboardButton(
                text='⏩',
                callback_data='right_support'
            )
        ]
    ]
)


edit_case_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить скин',
                callback_data='add_skin'
            ),
            InlineKeyboardButton(
                text='Удалить скин из кейса',
                callback_data='del_definite_content'
            ),
            InlineKeyboardButton(
                text='Удалить всё содержимое кейса',
                callback_data='del_all_content'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='cancel_from_edit_case'
            )
        ]
    ]
)


cancel_from_create_case = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='cancel_from_crcs'
            )
        ]
    ]
)


confirm_the_exit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, я хочу выйти',
                callback_data='cancel'
            )
        ],
        [
            InlineKeyboardButton(
                text='Продолжить заполнение',
                callback_data='continue_the_filling'
            )
        ]
    ]
)