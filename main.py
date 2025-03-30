from aiogram import types, Dispatcher, executor, Bot
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import os
from datetime import date
import datetime
import sqlite3 as sq
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

load_dotenv()

storage = MemoryStorage()
bot = Bot(os.environ['TOKEN_API'])
dp = Dispatcher(bot=bot, storage=storage)

admin_id = os.environ['ADMIN_ID']
website_domain = os.environ['WEBSITE_DOMAIN']

def main_bot():
    db = sq.connect('my_site/sqlite3.db')
    cur = db.cursor()

    datetomonth = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    monthcount = {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31, 'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
    now = str(datetime.datetime.now())
    now_date = int(now.split()[0].split('-')[2])
    now_month = int(now[5]+now[6])
    now_year = int(f'{now[0]}{now[1]}{now[2]}{now[3]}')
    selected_date = now_month
    select_date_admin = now_month
    select_year = now_year
    select_year_admin = now_year


    def date_validation(date):

        try:
            date = date.split('_')
            month_name = date[2]

            month_number = 0
            for k, v in datetomonth.items():
                if v == date[2]:
                    month_number = k

            day = int(date[3])
            year = int(date[1])
            now = datetime.datetime.now()
            if year < now.year or (year == now.year and month_number < now.month) or (
                    year == now.year and month_number == now.month and day < now.day):
                return True

            else:
                return False
        except Exception as ex:
            return False

    def time_validation(time):
        try:
            time = time.split('_')
            month_name = time[2]

            month_number = 0
            for k, v in datetomonth.items():
                if v == time[2]:
                    month_number = k

            day = int(time[3])
            year = int(time[1])
            now = datetime.datetime.now()
            if year < now.year or (year == now.year and month_number < now.month) or (
                    year == now.year and month_number == now.month and day < now.day):
                return True

            else:
                return False
        except Exception as ex:
            return False


    def delete_rubbish():
        all_blocked = cur.execute("SELECT * FROM main_hd_blockedmodel").fetchall()
        for i in all_blocked:
            if date_validation(i[1]):
                cur.execute(f"DELETE FROM main_hd_blockedmodel WHERE id={i[0]}")
                db.commit()

            if time_validation(i[2]):
                cur.execute(f"DELETE FROM main_hd_blockedmodel WHERE id={i[0]}")
                db.commit()



    delete_rubbish()

    class RecordStates(StatesGroup):
        time = State()
        service = State()
        service_id = State()
        phone_number = State()
        where_location = State()
        location = State()
        description = State()
        is_correct = State()

    def cancel_note_date_check(time):
        time = time.split()
        for k, v in datetomonth.items():
            if v == time[1]:
                month_number = k


    @dp.message_handler(commands=['start'])
    async def start_cmd(message: types.Message):
        await start_db()
        await bot.send_message(message.chat.id, 'Welcome to the schedule bot', reply_markup=get_start_kb())

    @dp.message_handler(Text(equals='Make an appointment🗓'))
    async def start1_cmd(message: types.Message):
        await start_db()

        await bot.send_message(message.chat.id, 'Choose date', reply_markup=kalendar_ikb(datetomonth.get(now_month), monthcount.get(datetomonth.get(now_month)), now_year,False))

    @dp.message_handler(Text(equals='My appointments📕'))
    async def check_notes_handler(message: types.Message):
        user_notes = get_user_notes(message.chat.id)
        for i in user_notes:
            await bot.send_message(message.chat.id, f"""Date and time: {i[2]}
Service: {i[3]} {i[4]}
Phone number: {i[5]}
Location: {i[6]} {i[7]}
Comment: {i[8]}""")

    @dp.message_handler(Text(equals='Cancel an appointment💔'))
    async def cancel_note_handler(message: types.Message):
        user_notes = get_user_notes(message.chat.id)
        for i in user_notes:
            if cancel_note_date_check(i[2]) == False:
                continue
            else:
                await bot.send_message(message.chat.id, f"""Date and time: {i[2]}
Service: {i[3]} {i[4]}
Phone number: {i[5]}
Location: {i[6]} {i[7]}
Comment: {i[8]}""", reply_markup=note_cancel_ikb(i[0]))

    @dp.callback_query_handler(Text(endswith='cancel'))
    async def user_note_cancel_handler(callback: types.CallbackQuery):
        note_id = int(callback.data.split('_')[0])
        i = note_cancel_information(note_id)[0]
        note_cancel(note_id)
        await bot.send_message(admin_id, f"""!!!Appointment cancellation!!!
Date and time: {i[2]}
Service: {i[3]} {i[4]}
Phone number: {i[5]}
Location: {i[6]} {i[7]}
Comment: {i[8]}""")
        await bot.send_message(callback.from_user.id, 'Appointment was cancelled')


    @dp.message_handler(Text(equals='Our website🌐'))
    async def out_website_handler(message: types.Message):
        await bot.send_message(message.chat.id, f'<a href="{website_domain}">Click on this text to go to our website</a>', parse_mode='html')

    @dp.callback_query_handler(Text(equals='go-backFalse'))
    async def go_back_callback(callback: types.CallbackQuery):
        nonlocal selected_date
        nonlocal select_year
        if selected_date == now_month and select_year == now_year:
            await bot.answer_callback_query(callback_query_id=callback.id, text='Unfortunately, time cannot be turned back....', show_alert=True)
            return 0
        elif selected_date == 1:
            selected_date = 12
            select_year -= 1
        else:
            selected_date = selected_date-1
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(selected_date), monthcount.get(datetomonth.get(selected_date)), select_year,False))

    @dp.callback_query_handler(Text(equals='go-directFalse'))
    async def go_back_callback(callback: types.CallbackQuery):
        nonlocal selected_date
        nonlocal select_year
        if selected_date == 12:
            selected_date = 1
            select_year += 1
        else:
            selected_date = selected_date+1
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(selected_date), monthcount.get(datetomonth.get(selected_date)), select_year,False))

    @dp.callback_query_handler(Text(equals='go-backTime'))
    async def go_back_callback(callback: types.CallbackQuery):
        nonlocal selected_date
        nonlocal select_year
        if selected_date == now_month and select_year == now_year:
            await bot.answer_callback_query(callback_query_id=callback.id, text='Unfortunately, time cannot be turned back...', show_alert=True)
            return 0
        elif selected_date == 1:
            selected_date = 12
            select_year -= 1
        else:
            selected_date = selected_date-1
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(selected_date), monthcount.get(datetomonth.get(selected_date)), select_year,'Time'))

    @dp.callback_query_handler(Text(equals='go-directTime'))
    async def go_back_callback(callback: types.CallbackQuery):
        nonlocal selected_date
        nonlocal select_year
        if selected_date == 12:
            selected_date = 1
            select_year += 1
        else:
            selected_date = selected_date+1
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(selected_date), monthcount.get(datetomonth.get(selected_date)), select_year,'Time'))

    @dp.message_handler(commands=['admin'])
    async def admin_cmd(message: types.Message):
        if message.from_user.id in [admin_id] == False:
            await message.answer('You are not an administrator.!')

        else:
            await bot.send_message(message.chat.id, 'Select an option:', reply_markup=admin_main_ikb())

    @dp.callback_query_handler(Text(equals='date-block'))
    async def date_block(callback: types.CallbackQuery):
        await bot.send_message(callback.from_user.id, 'Select the date you want to block', reply_markup=kalendar_ikb(datetomonth.get(now_month), monthcount.get(datetomonth.get(now_month)), now_year,True))

    @dp.callback_query_handler(Text(equals='go-backTrue'))
    async def go_back_callback(callback: types.CallbackQuery):
        nonlocal select_date_admin
        nonlocal select_year_admin
        if select_date_admin == now_month and select_year_admin == now_year:
            await bot.answer_callback_query(callback_query_id=callback.id, text='Unfortunately, time cannot be turned back...', show_alert=True)
            return 0
        elif select_date_admin == 1:
            select_date_admin = 12
            select_year_admin -= 1
        else:
            select_date_admin = select_date_admin-1
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(select_date_admin), monthcount.get(datetomonth.get(select_date_admin)), select_year_admin,True))

    @dp.callback_query_handler(Text(equals='go-directTrue'))
    async def go_back_callback(callback: types.CallbackQuery):
        nonlocal select_date_admin
        nonlocal select_year_admin
        if select_date_admin == 12:
            select_date_admin = 1
            select_year_admin += 1
        else:
            select_date_admin = select_date_admin+1
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(select_date_admin), monthcount.get(datetomonth.get(select_date_admin)), select_year_admin,True))

    @dp.callback_query_handler(Text(startswith='unblock'))
    async def unblock_date(callback: types.CallbackQuery):
        date = callback.data.replace('unblock', '').replace('_True', '')
        delete_date(date)
        await bot.send_message(callback.from_user.id, f'{block_back_message(date)} back in the main calendar!')

    @dp.callback_query_handler(Text(startswith='_'))
    async def date_callback(callback: types.CallbackQuery, state: FSMContext):
        if 'True' in callback.data:
            date = callback.data[:-5]
            await block_date(date)
            await bot.send_message(callback.from_user.id, f'{block_back_message(callback.data)[2:]} Blocked, if you did this by accident, then click on the button below', reply_markup=unblock_data_ikb(callback.data))
        elif 'Time' in callback.data:
            date = callback.data[:-5]
            await bot.send_message(callback.from_user.id, 'Choose a time', reply_markup=await time_choose_ikb('Time',date))
        else:
            await RecordStates.time.set()
            await bot.send_message(callback.from_user.id, 'Filling out the form...', reply_markup=cancel_form_kb())
            await bot.send_message(callback.from_user.id, 'Choose a time', reply_markup=await time_choose_ikb(False, block_back_message(callback.data)))

    @dp.message_handler(Text(equals='Cancel filling out the form'), state='*')
    async def stop_handler(message: types.Message, state: FSMContext):
        if state is None:
            return

        await state.finish()
        await bot.send_message(message.chat.id, 'Form filling interrupted', reply_markup=get_start_kb())

    @dp.callback_query_handler(Text(startswith='time_unblock'))
    async def time_unblock_handler(callback: types.CallbackQuery):
        time = callback.data.replace('time_unblock', '')
        delete_time(time)

        await bot.send_message(callback.from_user.id, f'{time[2:]} back in the main calendar!')

    @dp.callback_query_handler(Text(equals='time-block'))
    async def time_for_block_handler(callback: types.CallbackQuery):
        await bot.send_message(callback.from_user.id, 'Select date', reply_markup=kalendar_ikb(datetomonth.get(now_month), monthcount.get(datetomonth.get(now_month)), now_year,'Time'))

    @dp.callback_query_handler(Text(endswith='Time'), Text(startswith='#'))
    async def time_block_handler(callback: types.CallbackQuery):
        block_time(callback.data[:-5])
        await bot.send_message(callback.from_user.id, f'{callback.data[2:][:-5]} blocked, if you did this by accident, click the button below', reply_markup=unblock_time_ikb(callback.data[:-5]))


    @dp.callback_query_handler(Text(startswith='#'), state=RecordStates.time)
    async def time_handler(callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['time'] = block_back_message(callback.data)

        await bot.send_message(callback.from_user.id, 'Choose a service', reply_markup=services_ikb())
        await RecordStates.next()

    @dp.callback_query_handler(state=RecordStates.service)
    async def service_handler(callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['service'] = callback.data.split('_')[0]

        await RecordStates.next()
        cat_name = callback.data.split('_')[0]
        cat_id = callback.data.split('_')[1]
        await bot.send_message(callback.from_user.id, f"""Choose {cat_name} on our <a href="{website_domain}/ourservices/{cat_id}">website</a> and send its id (id is written next to each service)""", parse_mode='html')

    @dp.message_handler(state=RecordStates.service_id)
    async def service_id_handler(message: types.Message, state: FSMContext):
        try:
            service_course = service_course_db(message.text)
            async with state.proxy() as data:
                data['service_id'] = service_course[0]
            await RecordStates.next()
            await bot.send_message(message.chat.id, 'Write your contact phone number')
        except:
            await bot.send_message(message.chat.id, 'Unfortunately, such an id does not exist, please send a correct one.')


    @dp.message_handler(state=RecordStates.phone_number)
    async def phone_num_handler(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['phone_number'] = message.text

        await RecordStates.next()
        await bot.send_message(message.chat.id, 'Choose a place', reply_markup=where())

    @dp.callback_query_handler(state = RecordStates.where_location)
    async def where_location_handler(callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['where_location'] = callback.data
        await RecordStates.next()

        if callback.data == 'Departure':
            await bot.send_message(callback.from_user.id, 'Write your exact address')

            @dp.message_handler(state=RecordStates.location)
            async def adress_location_handler(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['location'] = message.text
                await RecordStates.next()
                await bot.send_message(callback.from_user.id, 'Write your own wishes')

        else:
            async with state.proxy() as data:
                data['location'] = '-'
            await RecordStates.next()
            await bot.send_message(callback.from_user.id, 'Write your own wishes')


    @dp.message_handler(state = RecordStates.description)
    async def desc_handler(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['description'] = message.text
            await bot.send_message(message.chat.id, f"""Service: {data['service']}  {data['service_id']}\nDate and time: {data['time']}\nPhone Number: {data['phone_number']}\nLocation: {data['where_location']} {data['location']}\nComment: {data['description']}""")

        await RecordStates.next()
        await bot.send_message(message.chat.id, 'Everything right?', reply_markup=is_correct_ikb())

    @dp.callback_query_handler(state=RecordStates.is_correct)
    async def is_correct_handler(callback: types.CallbackQuery, state: FSMContext):
        if callback.data == 'all_correct':
            async with state.proxy() as data:
                add_note(data, callback.from_user.id)
                await bot.send_message(chat_id=admin_id, text=f"""Service: {data['service']}  {data['service_id']}\nDate and time: {data['time']}\nPhone Number: {data['phone_number']}\nLocation: {data['where_location']} {data['location']}\nComment: {data['description']}""")

                await bot.send_message(chat_id=admin_id, text='Accept?', reply_markup=accept_ikb(get_id_of_note(data)))


            await bot.send_message(callback.from_user.id, 'Your entry has been sent, we will let you know about responce as soon as possible.', reply_markup=get_start_kb())
        else:
            await bot.send_message(callback.from_user.id, 'Appointment rejected', reply_markup=get_start_kb())

        await state.finish()

    @dp.callback_query_handler(Text(endswith='accept'))
    async def accept_handler(callback: types.CallbackQuery):
        if callback.data.startswith('yes'):
            note_id = get_note_id(callback.data)
            accept_note(note_id)
            time_for_block = time_for_block_db(note_id)
            await bot.send_message(callback.from_user.id, 'Appointment accepted!')
            await bot.send_message(chat_id=str(get_userid(note_id)), text='Appointment accepted')
            block_time(time_for_block)
            block_time_range(note_id)
        else:
            note_id = get_note_id(callback.data)

            delete_note(note_id)

            await bot.send_message(callback.from_user.id, 'Appointment rejected')

    @dp.callback_query_handler(Text(equals='today-notes'))
    async def today_notes_handler(callback: types.CallbackQuery):
        day = get_today_day(now)
        notes_from_t_and_to = get_notes_from_t_and_to(day)
        for i in notes_from_t_and_to:
            i = i[0]
            await bot.send_message(callback.from_user.id, f"""Date and time: {i[2]}
    Service: {i[3]} {i[4]}
    Pgone number: {i[5]}
    Location: {i[6]} {i[7]}
    Comment: {i[8]}
    User: {i[1]}""")

    @dp.callback_query_handler(Text(equals='all-notes'))
    async def all_notes_handler(callback: types.CallbackQuery):
        all_notes = get_all_notes()
        for i in all_notes:
            await bot.send_message(callback.from_user.id, f"""Date and time: {i[2]}
    Service: {i[3]} {i[4]}
    Pgone number: {i[5]}
    Location: {i[6]} {i[7]}
    Comment: {i[8]}
    User: {i[1]}""")

    def get_start_kb():
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(KeyboardButton(text='Make an appointment🗓'))
        kb.insert(KeyboardButton(text='View my appointments📕'))
        kb.insert(KeyboardButton(text='Cancel an appointment💔'))
        kb.add(KeyboardButton(text='Our website🌐'))

        return kb

    def kalendar_ikb(month, days_count, year, admin):
        ikb = InlineKeyboardMarkup(row_width=5)
        ikb.row(InlineKeyboardButton(text='<<', callback_data=f'go-back{admin}'),
                InlineKeyboardButton(text='  ', callback_data='None-back'),
                InlineKeyboardButton(text=f'{month} {year}', callback_data='month-callback'),
                InlineKeyboardButton(text='  ', callback_data='None-back'),
                InlineKeyboardButton(text='>>', callback_data=f'go-direct{admin}'))

        all_blocked = get_blocked()
        if month == datetomonth.get(now_month) and year == now_year:
            for day in range(int(now[8] + now[9]), days_count + 1):
                if f'_{year}_{month}_{day}' in blocked_list(all_blocked) or (
                        f'#_{year}_{month}_{day}_10:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_11:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_12:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_13:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_14:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_15:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_16:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_17:00' in blocked_list(
                        all_blocked) and f'#_{year}_{month}_{day}_18:00' in blocked_list(all_blocked)):
                    continue
                else:
                    ikb.insert(InlineKeyboardButton(text=day, callback_data=f'_{year}_{month}_{day}_{admin}'))
        else:
            for day in range(1, days_count + 1):
                if f'_{year}_{month}_{day}' in blocked_list(all_blocked):
                    continue
                else:
                    ikb.insert(InlineKeyboardButton(text=day, callback_data=f'_{year}_{month}_{day}_{admin}'))

        return ikb

    async def time_choose_ikb(admin, date):
        ikb = InlineKeyboardMarkup(row_width=2)
        all_blocked_time = get_blocked()

        if admin == False:
            date = date.replace(' ', '_')
            for hour in range(10, 19):
                if f'#{date}{hour}:00' in blocked_list(all_blocked_time):
                    continue
                else:
                    ikb.insert(InlineKeyboardButton(text=f'{hour}:00', callback_data=f'#{date}_{hour}:00_{admin}'))
        else:
            date = date.replace(' ', '_')
            for hour in range(10, 19):
                if f'#{date}_{hour}:00' in blocked_list(all_blocked_time):
                    continue
                else:
                    ikb.insert(InlineKeyboardButton(text=f'{hour}:00', callback_data=f'#{date}_{hour}:00_{admin}'))

        return ikb


    def admin_main_ikb():
        ikb = InlineKeyboardMarkup(row_width=3)
        ikb.add(InlineKeyboardButton(text='Block date', callback_data='date-block'))
        ikb.add(InlineKeyboardButton(text='Block time', callback_data='time-block'))
        ikb.add(InlineKeyboardButton(text='Appointments for today and tomorrow', callback_data='today-notes'))
        ikb.add(InlineKeyboardButton(text='All appointments', callback_data='all-notes'))


        return ikb

    def unblock_data_ikb(date):
        ikb = InlineKeyboardMarkup(row_width=1)
        ikb.add(InlineKeyboardButton(text=f'Unblock date ({block_back_message(date)})',
                                     callback_data=f'unblock{date}'))

        return ikb

    def unblock_time_ikb(time):
        ikb = InlineKeyboardMarkup(row_width=1)
        ikb.add(InlineKeyboardButton(text=f'Unblock date ({block_back_message(time)})',
                                     callback_data=f'time_unblock{time}'))

        return ikb

    def services_ikb():
        ikb = InlineKeyboardMarkup(row_width=2)
        all_categories = get_all_categories()
        for cat in all_categories:
            cat_id = cat[0]
            cat_name = cat[1]
            ikb.insert(InlineKeyboardButton(text=f'{cat_name}', callback_data=f'{cat_name}_{cat_id}'))

        return ikb

    def where():
        ikb = InlineKeyboardMarkup(row_width=1)
        ikb.add(InlineKeyboardButton(text='They will come to you.', callback_data='Hairdresser will arrive to you'))
        ikb.add(InlineKeyboardButton(text='You will arrive.', callback_data='You will arrive to studio'))

        return ikb

    def is_correct_ikb():
        ikb = InlineKeyboardMarkup(row_width=1)
        ikb.add(InlineKeyboardButton(text='Yes, everything is correct', callback_data='all_correct'))
        ikb.add(InlineKeyboardButton(text='No, start recording again', callback_data='not_correct'))

        return ikb

    def accept_ikb(note_id):
        ikb = InlineKeyboardMarkup(row_width=1)
        ikb.add(InlineKeyboardButton(text='Yes', callback_data=f'yes_{note_id}_accept'))
        ikb.add(InlineKeyboardButton(text='No', callback_data=f'no_{note_id}_accept'))

        return ikb

    def note_cancel_ikb(id):
        ikb = InlineKeyboardMarkup(row_width=1)
        ikb.add(InlineKeyboardButton(text='Cancel appointment', callback_data=f'{id}_cancel'))

        return ikb

    def cancel_form_kb():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text='Cancel filling out the form'))

        return kb

    async def start_db():
        db.commit()


    async def block_date(date):
        cur.execute(f"INSERT INTO main_hd_blockedmodel (blocked_date, blocked_time) VALUES (?,?)", (date, ''))
        db.commit()

    def get_blocked():
        blocked = cur.execute("SELECT blocked_date, blocked_time FROM main_hd_blockedmodel").fetchall()
        db.commit()
        return blocked

    def delete_date(date):
        cur.execute(f"DELETE FROM main_hd_blockedmodel WHERE blocked_date='{date}'")
        db.commit()

    def add_note(data, user_id):
        cur.execute(
            "INSERT INTO main_hd_notesmodel (user_id,time,service,service_id,phone_number,where_location,location,description,is_accepted) VALUES (?,?,?,?,?,?,?,?,?)",
            (user_id, data['time'], data['service'], data['service_id'], data['phone_number'], data['where_location'],
             data['location'], data['description'], 'FALSE'))
        db.commit()

    def get_id_of_note(data):
        query = """
            SELECT id 
            FROM main_hd_notesmodel 
            WHERE time=? 
            AND service=? 
            AND service_id=? 
            AND phone_number=? 
            AND where_location=? 
            AND location=? 
            AND description=?
        """

        # Execute the query with the data values as parameters
        note_id = cur.execute(query, (
            data['time'],
            data['service'],
            data['service_id'],
            data['phone_number'],
            data['where_location'],
            data['location'],
            data['description']
        )).fetchone()

        return note_id

    def accept_note(note_id):
        cur.execute(f"UPDATE main_hd_notesmodel SET is_accepted='TRUE' WHERE id='{note_id}'")
        db.commit()

    def delete_note(note_id):
        cur.execute(f"DELETE FROM main_hd_notesmodel WHERE id='{note_id}'")
        db.commit()

    def get_userid(note_id):
        note_user_id = cur.execute(f"SELECT user_id FROM main_hd_notesmodel WHERE id={note_id}").fetchone()
        db.commit()
        return note_user_id[0]

    def block_time(time):
        cur.execute("INSERT INTO main_hd_blockedmodel (blocked_date, blocked_time) VALUES (?,?)", ('', time))
        db.commit()

    def delete_time(time):
        cur.execute(f"DELETE FROM main_hd_blockedmodel WHERE blocked_time='{time}'")
        db.commit()

    def time_for_block_db(note_id):
        time = cur.execute(f"SELECT time FROM main_hd_notesmodel WHERE id={note_id}").fetchone()
        db.commit()
        time_finally = get_finally_time(time[0])
        return time_finally

    def get_notes_from_t_and_to(day):
        days_get = cur.execute("SELECT time FROM main_hd_notesmodel").fetchall()
        r = []
        for i in days_get:
            time_day = i[0].split()[2]
            if str(day) == time_day or str(int(day) + 1) == time_day:
                r.append(cur.execute(f"SELECT * FROM main_hd_notesmodel WHERE time='{i[0]}'").fetchall())

        return r

    def get_all_notes():
        notes = cur.execute("SELECT * FROM main_hd_notesmodel").fetchall()
        return notes

    def get_user_notes(user_id):
        user_notes_all = cur.execute(f"SELECT * FROM main_hd_notesmodel WHERE user_id='{user_id}'").fetchall()
        return user_notes_all

    def service_course_db(service_id):
        service_course_get = cur.execute(
            f"SELECT hairdress FROM main_hd_hairdressmodel WHERE id={int(service_id)}").fetchone()
        db.commit()
        return service_course_get

    def note_cancel(note_id):
        note_time = cur.execute(f"SELECT time FROM main_hd_notesmodel WHERE id={note_id}").fetchone()[0].split()
        note_time[0] = '#_' + note_time[0]
        note_time = '_'.join(note_time)
        cur.execute(f"DELETE FROM main_hd_blockedmodel WHERE blocked_time='{note_time}'")
        delete_note(note_id)

    def note_cancel_information(note_id):
        note = cur.execute(f"SELECT * FROM main_hd_notesmodel WHERE id={note_id}").fetchall()
        return note

    def get_all_categories():
        all_cats = cur.execute(f"SELECT * FROM main_hd_category").fetchall()
        return all_cats

    def block_time_range(note_id):
        service_name = cur.execute(f"SELECT service_id FROM main_hd_notesmodel WHERE id={int(note_id)}").fetchone()[0]
        time = get_finally_time(cur.execute(f"SELECT time FROM main_hd_notesmodel WHERE id={int(note_id)}").fetchone()[0])
        time_spend = cur.execute(f"SELECT time_spend FROM main_hd_hairdressmodel WHERE hairdress='{service_name}'").fetchone()[0]

        time_plus = time.split('_')[4]
        time_plus_hours = int(time_plus.split(':')[0])
        for i in range(int(time_spend)):
            time_plus_hours += 1
            time_plus_hours_d = f'{str(time_plus_hours)}:00'
            r = '_'.join(time.split('_')[:4]) + '_' + time_plus_hours_d

            block_time(r)
            db.commit()

    def blocked_list(arr):
        r = []
        for i in arr:
            r.append(''.join(i))

        return r

    def block_back_message(s):
        s = s.replace('True', '').replace('False', '').replace('#', '').split('_')
        return ' '.join(s)

    def get_note_id(s):
        s = s.replace('(', '').replace(')', '').replace(',', '').split('_')
        return s[1]

    def blocked_time(arr):
        r = []
        for i in arr:
            r.append('')

    def get_finally_time(time):
        time = time.split()
        time[0] = '#_' + time[0]
        time = '_'.join(time)
        return time

    def get_today_day(now):
        r = now.split()[0].split('-')[-1]
        return r


    def cancel_note_date_check(time):
        time = time.split()
        month_name = time[1]

        month_number = 0
        for k, v in datetomonth.items():
            if v == time[1]:
                month_number = k

        date = int(time[2])
        year = int(time[0])
        now = datetime.datetime.now()
        if year > now.year or (year == now.year and month_number > now.month) or (
                year == now.year and month_number == now.month and date >= now.day):
            return True
        else:
            return False

    if __name__=='__main__':
        executor.start_polling(dp)


def main():
    main_bot()

if __name__=='__main__':
    main()
