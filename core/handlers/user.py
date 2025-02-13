from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, StateFilter, CommandObject
from aiogram.utils import deep_linking
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode


from core.db.dbconnect import get_all_id, get_user_data_func, new_user_add_func, referals_up_func, balance_down
from core.db.info import add_user, add_withdraw, get_data
from core.db.cases import get_cases, get_case_price
from core.db.support import add_message
from core.db.case_content import get_case_content


from core.keyboards.user_inline_kb import subs_keyboard, start_keyboard, cancel_kb, cases_kb, case_open_kb, case_open_denied_kb
from core.keyboards.admin_kb import admin_start_kb


from core.filters.InGroupCheck import InGroupCheck


from core.utils.states import Help, ReplySupport, EditCase, CreateCase, DeleteCase


router = Router()
case_name = ''


#===================================================================
# /start


@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject, bot: Bot, state: FSMContext):
    ids = get_all_id()
    if message.from_user.id != 0:
        if message.from_user.id not in ids:

            args = command.args

            if args:
                if int(args) in ids:
                    referals_up_func(args)
                    new_user_add_func(message.from_user.id)
                    add_user()
                    data = get_user_data_func(args)
                    await bot.send_message(0, f'Пользователь {data[0]} пригласил {message.from_user.first_name}', parse_mode=ParseMode.HTML)
                    await message.answer(f'Привет, {message.from_user.first_name}')
                    await message.answer('Подпишитесь на каналы, чтобы продолжить пользоваться ботом',
                                    reply_markup=subs_keyboard)
                else:
                    new_user_add_func(message.from_user.id)
                    add_user()
                    await bot.send_message(0, f'Пользователь {data[0]} пригласил {message.from_user.first_name}')
                    await message.answer(f'Привет, {message.from_user.first_name}')
                    await message.answer('Подпишитесь на каналы, чтобы продолжить пользоваться ботом',
                                        reply_markup=subs_keyboard)
                
            else:
                new_user_add_func(message.from_user.id)
                add_user()
                await bot.send_message(0, f'Пользователь {message.from_user.first_name} перешёл в бота!')
                await message.answer('Подпишитесь на каналы, чтобы продолжить пользоваться ботом',
                                        reply_markup=subs_keyboard)
        else:
            if await InGroupCheck(message.from_user.id, bot):
                await message.answer('И я вас приветствую!',
                                    reply_markup=start_keyboard)
                await state.set_state(Help.default)
            else:
                await message.answer('Подпишитесь на каналы, чтобы продолжить пользоваться ботом',
                                        reply_markup=subs_keyboard)
    else:
        await message.answer('Привет, хозяин!',
                             reply_markup=admin_start_kb)
        await state.set_state(ReplySupport.default)
    
            

@router.callback_query(F.data == 'check_subs')
async def check_subs(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if await InGroupCheck(callback.from_user.id, bot):
        await callback.message.edit_text('Спасибо за то что подписались на нас!\n',
                                        reply_markup=start_keyboard)
        await state.set_state(Help.default)
    else:
        pass
    

#=============================================================================
# Профиль


@router.callback_query(F.data == 'profile_button')
async def profile_button(callback: CallbackQuery, bot: Bot):
    if await InGroupCheck(callback.from_user.id, bot):
        link = await deep_linking.create_start_link(bot=bot, payload=callback.from_user.id)
        data = get_user_data_func(callback.from_user.id)
        await callback.message.edit_text(f'Ваш ID: {data[0]}\n\n'
                                         f'Рефералов: {data[1]}\n'
                                         f'Баланс: {data[2]}₽\n\n'
                                         #f'Скинов в инвентаре: {}\n\n'
                                         f'Ваша реферальная ссылка:\n\n {link}',
                                         reply_markup=cancel_kb)
    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)


#===============================================================================
# Обычная кнопка


@router.callback_query(F.data == 'roadmap_button')
async def roadmap_func(callback: CallbackQuery, bot: Bot):
    if await InGroupCheck(callback.from_user.id, bot):
        await callback.message.edit_text('Ближайшие обновления:\n\n'
                                        'Пока что ничего',
                                        reply_markup=cancel_kb)
    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)


#=======================================================================
# Кнопка "назад"


@router.callback_query(F.data == 'cancel')
async def cancel_process(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if await InGroupCheck(callback.from_user.id, bot):
        info = get_data()
        if callback.from_user.id != 0:
            await state.set_state(Help.default)
            await callback.message.edit_text(f'Всего пользователей: {info[0]}\n'
                                            f'Выведено скинов: {info[1]} (в рублях)\n',
                                            reply_markup=start_keyboard)
        else:
            await callback.message.edit_text(f'Всего пользователей: {info[0]}\n'
                                            f'Выведено скинов: {info[1]} (в рублях)\n',
                                            reply_markup=admin_start_kb)
            await state.set_state(EditCase.default)
            await state.set_state(CreateCase.default)
            await state.set_state(DeleteCase.default)
            await state.set_state(ReplySupport.default)
    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)
    

#==========================================================
# Поддержка


@router.callback_query(F.data == 'support_button')
async def help_pressed(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if await InGroupCheck(callback.from_user.id, bot):
        await callback.message.edit_text(
                                        '| Вы можете предложить идею для обновления |\n'
                                        '| Написать свои пожелания админам |\n'
                                        '| Выразить своё недовольство |\n\n'
                                        'P.S. Просто введите текст и он будет отправлен админам',
                                        reply_markup=cancel_kb)
        await state.set_state(Help.message)
    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)


@router.message(StateFilter(Help.message))
async def help_message_sending(message: Message, bot: Bot, state: FSMContext):
    try:
        add_message(message.from_user.id, message.text, message.message_id)
        await message.answer('Обращение было успешно отправлено!',
                            reply_markup=cancel_kb)
        await bot.send_message(0, 
                            f'Обращение в поддержку от {message.from_user.id}\n\n',
                            reply_markup=admin_start_kb)
        await state.set_state(Help.default)
    except Exception:
        await message.answer('Извините, но нужно отправить сообщение в текстовом формате',
                             reply_markup=cancel_kb)

@router.callback_query(F.data == 'help_for_admins')
async def donate_pressed(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text('USDT | TRC20:\n\n'
                                     'TNvviAVKRPZSnuiHTNCpqLC1UBpCsxAZ8t\n\n\n'
                                     'BSC | BEP20:\n\n'
                                     '0x431cb2df19603e29c3c1cec568c7655fa1919847\n\n\n'
                                     'Т-Банк:\n\n'
                                     '2200 7009 9950 0704\n\n\n\n'
                                     'P.S. Спасибо большое за вашу финансовую поддержку, '
                                     'каждый рубль будет вложен в улучшение бота<3',
                                     reply_markup=cancel_kb)
    

#======================================================
# Че то связанное с кейсами


@router.callback_query(F.data == 'case_button')
async def case_pressed(callback: CallbackQuery, bot: Bot):
    if await InGroupCheck(callback.from_user.id, bot):
        await callback.message.edit_text('Доступные кейсы: ',
                                        reply_markup=cases_kb(callback.from_user.id))
    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)
        

@router.callback_query(F.data.startswith('case='))
async def user_choiced_case_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if await InGroupCheck(callback.from_user.id, bot):
        global case_name
        case_name = callback.data.split('=')[1]

        data = get_case_content(case_name=case_name)

        message = "Название | Шанс % | Стоимость ₽ |\n\n"
        for info in data:
            message += f"{info[0]} | {info[1]}% | {info[2]}₽\n"

        await callback.message.edit_text(message, reply_markup=case_open_kb)

    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)


@router.callback_query(F.data == 'open_case_button')
async def case_opening(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_data = get_user_data_func(callback.from_user.id)

    balance = user_data[2]

    price = get_case_price(case_name=case_name)

    if balance >= price:
        balance_down(callback.from_user.id, price)
        await callback.message.edit_text('Да',
                                         reply_markup=cancel_kb)
        #логика открытия
    else:
        await callback.message.edit_text('Недостаточно средств для открытия кейса\n\n'
                                         f'Цена кейса: {price}₽\n\n'
                                         f'Ваш баланс: {balance}₽',
                                         reply_markup=case_open_denied_kb)
    


#открытие кейса





@router.callback_query(F.data == 'cancel_from_open_case')
async def cancel_from_open_case_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if await InGroupCheck(callback.from_user.id, bot):
        await callback.message.edit_text('Доступные кейсы: ',
                                        reply_markup=cases_kb(callback.from_user.id))
    else:
        await callback.message.answer('Чтобы начать пользоваться ботом, пожалуйста, подпишитесь на наш канал с новостями:\n',
                             reply_markup=subs_keyboard)