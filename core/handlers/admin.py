from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import StateFilter


from core.keyboards.user_inline_kb import cases_kb, start_keyboard, cancel_kb
from core.keyboards.admin_kb import admin_start_kb, support_check_kb, cancel_from_create_case, confirm_the_exit, edit_case_kb, generate_kb_func

from core.db.case_content import add_case_content, del_case_content, create_case, get_case_content, get_total_chance, del_all_content
from core.db.cases import add_case, del_case
from core.db.support import del_message, get_message
from core.db.prices import add_price
from core.db.dbconnect import get_all_id

from core.utils.states import EditCase, CreateCase, ReplySupport, DeleteCase, Mailing

import re


router = Router()

message_num = 0

messages = get_message()

user_id_for_reply = 0

message_id_for_delete = 0

editing_case = ''

#=====================================================================
# Добавить кейс


@router.callback_query(F.data == 'cancel_from_crcs')
async def cancel_from_create_case_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if get_total_chance(editing_case) != 100:
        await callback.message.edit_text('Шансы не доведены до 100%\n'
                                        'Вы точно хотите прекратить заполнение кейса?\n'
                                        'Кейс не будет отображаться у пользователей, до тех пор, пока его шансы не заполнены до 100%',
                                        reply_markup=confirm_the_exit)
    else:
        await callback.message.edit_text("Меню: ",
                                         reply_markup=admin_start_kb)
    

@router.callback_query(F.data == 'continue_the_filling')
async def continue_the_filling_case(callback: CallbackQuery, bot: Bot, state: FSMContext):

    chance = get_total_chance(editing_case)

    await callback.message.edit_text(f'Нужно заполнить шкалу шанса на 100%, на данный момент, шкала заполнена на {chance}%',
                                     reply_markup=cancel_from_create_case)



@router.callback_query(F.data == 'add_case')
async def add_case_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_text('Введите данные о кейсе в таком формате:\n\n'
                                     'Название | Цена',
                                     reply_markup=cancel_kb)
    await state.set_state(CreateCase.name)


@router.message(StateFilter(CreateCase.name))
async def add_case_cont2(message: Message, bot: Bot, state: FSMContext):
    try:
        case_data = message.text.split('|')

        global editing_case
        editing_case = case_data[0]

        add_case(case_data[0].rstrip(), case_data[1].lstrip())
        create_case(case_data[0])

        total_chance = get_total_chance(editing_case)

        await message.answer('А теперь введите данные о добавляемом скине в таком формате:\n\n'
                             'Название скина | Шанс выпадения | Цена продажи\n\n'
                            f'Шкала шанса заполнена на {total_chance}%',
                            reply_markup=cancel_kb)
        await state.set_state(CreateCase.content)
    except Exception:
        await message.answer('Ошибка... Введите данные в указанном выше формате.')


@router.message(StateFilter(CreateCase.content))
async def add_case_cont(message: Message, bot: Bot, state: FSMContext):
    try:
        global editing_case

        case_data = message.text.split(' | ')

        chance = get_total_chance(editing_case)

        if chance + float(case_data[1]) > 100:
            await message.answer('Шкала шансов на выпадение скина не должна превышать 100%\n\n'
                                f'Шкала заполнена на: {chance}%',
                                reply_markup=cancel_from_create_case)
            
        elif chance + float(case_data[1]) == 100:
            add_case_content(editing_case, case_data[0], case_data[1], case_data[2])
            add_price(case_data[0], case_data[2])
            await message.answer('Шкала заполнена на 100% !\n\n'
                                'Кейс добавлен в список кейсов для пользователей.',
                                reply_markup=admin_start_kb)
            await state.set_state(CreateCase.default)
        else:
            add_case_content(editing_case, case_data[0], case_data[1], case_data[2])
            add_price(case_data[0], case_data[2])
            await message.answer('Скин успешно добавлен в кейс, можете снова ввести данные.\n\n'
                                f'Нужно заполнить шкалу шанса на 100%, на данный момент, шкала заполнена на {chance + float(case_data[1])}%',
                                reply_markup=cancel_from_create_case)
    except Exception:
        await message.answer('Ошибка... Введите данные в указанном выше формате.')
        


#===========================================================
# Изменить кейс

@router.callback_query(F.data == 'edit_case')
async def choice_case_for_edit(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_text('Выберите кейс для редактирования:',
                                     reply_markup=cases_kb(0))
    await state.set_state(EditCase.choice)


@router.callback_query(F.data == 'cancel_from_edit_case')
async def choi_case_for_edit(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_text('Выберите кейс для редактирования:',
                                     reply_markup=cases_kb(0))
    await state.set_state(EditCase.choice)


@router.callback_query(F.data == 'del_all_content')
async def del_all_content_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global editing_case

    del_all_content(editing_case)

    await callback.message.edit_text(f'Содержимое кейса {editing_case} удалено!',
                                     reply_markup=admin_start_kb)
    
    await state.set_state(EditCase.default)


@router.callback_query(F.data == 'add_skin')
async def add_skin_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_text('Введите данные о добавляемом скине в таком формате:\n\n'
                                     'Название скина | Шанс выпадения | Цена продажи',
                                     reply_markup=cancel_kb)
    
    await state.set_state(CreateCase.content)


@router.callback_query(F.data == 'del_definite_content')
async def del_definite_content_func(callback: CallbackQuery, bot: Bot ,state: FSMContext):
    data = get_case_content(editing_case)
    message = "Название | Шанс % | Стоимость ₽ | ID\n\n"
    for info in data:
        message += f"{info[0]} | {info[1]}% | {info[2]}₽ | ID: {info[3]}\n"
    await callback.message.edit_text(message, reply_markup=generate_kb_func(editing_case))

    await state.set_state(EditCase.default)


@router.callback_query(F.data.startswith('id='))
async def deL_def_case_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global editing_case

    id = callback.data.split('=')[1]

    del_case_content(editing_case, id)

    await callback.message.edit_text('Скин успешно удален из кейса!\n\n'
                                     'Выберите следующий скин для удаления: ',
                                     reply_markup=generate_kb_func(editing_case))



@router.callback_query(StateFilter(EditCase.choice) & F.data.startswith('case='))
async def case_choiced(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global editing_case
    editing_case = callback.data.split('=')[1]

    await callback.message.edit_text(f'Вы выбрали кейс "{editing_case}"',
                                     reply_markup=edit_case_kb)
    await state.set_state(EditCase.default)


#===========================================================
# Удалить кейс

@router.callback_query(F.data == 'del_case')
async def del_case_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_text('Выберите кейс, который хотите удалить:',
                                     reply_markup=cases_kb(0))
    await state.set_state(DeleteCase.deleting)


@router.callback_query(StateFilter(DeleteCase.deleting) & F.data.startswith('case='))
async def deleting_case(callback: CallbackQuery, bot: Bot, state: FSMContext):

    case_name = callback.data.split('=')

    del_case(case_name[1].strip())

    await callback.message.edit_text(f'Кейс "{case_name[1]}" был успешно удален!',
                                     reply_markup=cancel_kb)


#========================================================================
# Обращение в поддержку


@router.callback_query(F.data == 'support_requests')
async def support_requests_func(callback: CallbackQuery, bot: Bot):
    global messages
    messages = get_message()

    try:
        await callback.message.edit_text(f'Обращение от: {messages[message_num][0]}\n\n'
                                         f'{messages[message_num][1]}\n\n'
                                         f'ID обращения: {messages[message_num][2]}',
                                         reply_markup=support_check_kb)
    except IndexError:
        await callback.message.edit_text('Обращений в поддержку не найдено, зайдите позже',
                                         reply_markup=cancel_kb)
        
    

@router.callback_query(F.data == 'looked')
async def looked_support_request(callback: CallbackQuery, bot: Bot):
    global messages
    messages = get_message()

    user_id_match = re.search(r'Обращение от: \s*(\d+)', callback.message.text)
    user_id = user_id_match.group(1)

    message_id_match = re.search(r'ID обращения: \s*(\d+)', callback.message.text)
    message_id = message_id_match.group(1)

    del_message(message_id=message_id)

    await bot.send_message(user_id, 'Ваше обращение в поддержку было просмотрено админом',
                           reply_markup=start_keyboard)
    
    global message_num
    message_num += 1

    try:
        await callback.message.edit_text(f'Обращение от: {messages[message_num][0]}\n\n'
                                         f'{messages[message_num][1]}\n\n'
                                         f'ID обращения: {messages[message_num][2]}',
                                         reply_markup=support_check_kb)
    except IndexError:
        await callback.message.edit_text('Обращений в поддержку не найдено, зайдите позже',
                                         reply_markup=cancel_kb)
        message_num = 0
        

@router.callback_query(F.data == 'reply_support')
async def reply_support_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id_match = re.search(r'Обращение от: \s*(\d+)', callback.message.text)
    message_id_match = re.search(r'ID обращения: \s*(\d+)', callback.message.text)

    global user_id_for_reply, message_id_for_delete
    
    message_id_for_delete = message_id_match.group(1)
    user_id_for_reply = user_id_match.group(1)

    await callback.message.edit_text('Введите ответ на обращение:',
                                     reply_markup=cancel_kb)
    await state.set_state(ReplySupport.reply)


@router.message(StateFilter(ReplySupport.reply))
async def send_support_reply(message: Message, bot: Bot, state: FSMContext):
    global message_id_for_delete, user_id_for_reply, message_num

    await bot.send_message(f'Ответ админа на ваше обращение в поддержку:\n\n'
                           f'{user_id_for_reply, message.text}',
                           reply_markup=cancel_kb)
    await message.answer('Ответ был успешно отправлен пользователю!',
                         reply_markup=cancel_kb)
    
    del_message(message_id=message_id_for_delete)

    await state.set_state(ReplySupport.default)

    message_num += 1

    try:
        await message.answer(f'Обращение от: {messages[message_num][0]}\n\n'
                                         f'{messages[message_num][1]}\n\n'
                                         f'ID обращения: {messages[message_num][2]}',
                                         reply_markup=support_check_kb)
    except IndexError:
        await message.answer('Обращений в поддержку не найдено, зайдите позже',
                                         reply_markup=cancel_kb)
        message_num = 0


@router.callback_query(F.data == 'left_support')
async def left_support_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global message_num
    message_num -= 1

    user_id_match = re.search(r'Обращение от: \s*(\d+)', callback.message.text)
    user_id = user_id_match.group(1)

    message_id_match = re.search(r'ID обращения: \s*(\d+)', callback.message.text)
    message_id = message_id_match.group(1)

    try:
        await callback.message.edit_text(f'Обращение от: {messages[message_num][0]}\n\n'
                                         f'{messages[message_num][1]}\n\n'
                                         f'ID обращения: {messages[message_num][2]}',
                                         reply_markup=support_check_kb)
    except IndexError:
        await callback.message.edit_text('Обращений в поддержку не найдено, зайдите позже',
                                         reply_markup=cancel_kb)
        message_num = 0


@router.callback_query(F.data == 'right_support')
async def right_support_func(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global message_num
    message_num += 1

    user_id_match = re.search(r'Обращение от: \s*(\d+)', callback.message.text)
    user_id = user_id_match.group(1)

    message_id_match = re.search(r'ID обращения: \s*(\d+)', callback.message.text)
    message_id = message_id_match.group(1)

    try:
        await callback.message.edit_text(f'Обращение от: {messages[message_num][0]}\n\n'
                                         f'{messages[message_num][1]}\n\n'
                                         f'ID обращения: {messages[message_num][2]}',
                                         reply_markup=support_check_kb)
    except IndexError:
        await callback.message.edit_text('Обращений в поддержку не найдено, зайдите позже',
                                         reply_markup=cancel_kb)
        message_num = 0



#====================================================
# Рассылка


@router.callback_query(F.data == 'start_mailing')
async def start_mailing_button_pressed(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_text('Отправьте текст/фото/видео одним сообщением, для рассылки пользователям',
                                     reply_markup=cancel_kb)
    await state.set_state(Mailing.sending)


@router.message(StateFilter(Mailing.sending))
async def mailing_sending_func(message: Message, bot: Bot, state: FSMContext):
    ids = get_all_id()
    
    for id in ids:
        await bot.copy_message(id, message.chat.id, message.message_id)
    
    await message.answer('Рассылка успешно завершена!',
                         reply_markup=admin_start_kb)
    

#================================================================
# Заявки на вывод
    

    
    
