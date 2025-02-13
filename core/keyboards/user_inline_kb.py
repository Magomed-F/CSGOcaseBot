from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.db.cases import get_cases
from core.db.case_content import get_total_chance


def cases_kb(id):
    if id != 0:

        cases_lst = []
        cases = get_cases()

        for case in cases:
            chance = get_total_chance(case[0])
            if chance == 100:
                button = InlineKeyboardButton(text=f'{case[0]} | {case[1]}', callback_data=f'case={case[0]}')
                cases_lst.append([button])
            else:
                pass

        button = InlineKeyboardButton(text='Назад', callback_data='cancel')
        cases_lst.append([button])
        
        cases_kb = InlineKeyboardMarkup(inline_keyboard=cases_lst)

        return cases_kb
    else:

        cases_lst = []
        lst = []

        button = InlineKeyboardButton(text='Добавить кейс', callback_data='add_case')
        lst.append(button)

        button = InlineKeyboardButton(text='Изменить кейс', callback_data='edit_case')
        lst.append(button)

        button = InlineKeyboardButton(text='Удалить кейс', callback_data='del_case')
        lst.append(button)

        cases_lst.append(lst)

        cases = get_cases()

        for case in cases:
            button = InlineKeyboardButton(text=f'{case[0]} | {case[1]}', callback_data=f'case={case}')
            cases_lst.append([button])

        button = InlineKeyboardButton(text='Назад', callback_data='cancel')
        cases_lst.append([button])

        cases_kb = InlineKeyboardMarkup(inline_keyboard=cases_lst)

        return cases_kb

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Профиль',
                callback_data='profile_button'
            )
        ],
        [
            InlineKeyboardButton(
                text='Кейсы',
                callback_data='case_button'
            ),
            InlineKeyboardButton(
                text='RoadMap',
                callback_data='roadmap_button'
            )
        ],
        [
            InlineKeyboardButton(
                text='Поддержка',
                callback_data='support_button'
            ),
            InlineKeyboardButton(
                text='Инвентарь',
                callback_data='inventory_button'
            )
        ],
        [
            InlineKeyboardButton(
                text='Пожертвовать на развитие бота',
                callback_data='help_for_admins'
            )
        ]
    ]
)


subs_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подписаться',
                url=f'https://t.me/csbottest'
            )
        ],
        [
            InlineKeyboardButton(
                text='Проверить подписки',
                callback_data='check_subs'
            )
        ]
    ]
)


withdraw_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вывести',
                callback_data='withdraw_button'
            )
        ]
    ]
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='cancel'
            )
        ]
    ]
)


case_open_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Открыть кейс',
                callback_data='open_case_button'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='cancel_from_open_case'
            )
        ]
    ]
)


case_open_denied_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='cancel_from_open_case'
            )
        ]
    ]
)