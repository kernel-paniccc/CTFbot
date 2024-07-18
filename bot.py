from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.types import message, Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time as t


class flag(StatesGroup):
    flager = State()


bot = Bot(token="TOKEN")
dp = Dispatcher()


def get_users():
    users = []
    file = open('users.txt', 'r')
    lines = 0
    for line in file:
        lines += 1

    with open('users.txt', 'r') as file:
        userslist = file.read()

    for i in range(lines):
        start = userslist.find('[') + 1
        end = userslist.find(']')
        usr = userslist[start:end]
        userslist = userslist[end + 1:]
        users.append(usr)
    return users



@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет, это бот zelCTF, кидай мне флаг и получай баллы ! Список команд: /help")




@dp.message(Command('help'))
async def help(message: Message):
        await message.answer("/start - запуск бота\n /register - регистрация\n /flag - сдача флага\n /scoreboard - рейтинг участников")





@dp.message(Command('register'))
async def register(message: Message,):
    username_oi = message.from_user.username
    username = str(username_oi)
    with open("users.txt", "r") as f:
        name = f.read()
        f.close
    if str(username) == 'None' or str(username) == "none":
        await message.answer('У вас нет никнейма телеграмм. Пожалуйста, добавьте его для успешной регистрации')
    elif username in name:
        await message.answer('Извините, вы уже зарегистрированны')
    else:
        with open("users.txt", "a") as file:
            file.write(f'[{username}]\n')
            file.close
            await message.answer(f'Отлично, твой ник: {username}. Он будет отображаться в скорборде.')




@dp.message(Command('flag'))
async def flags(message: Message, state: FSMContext):
    user_oi = message.from_user.username
    user = str(user_oi)
    dir = get_users()
    if user in dir:
       await state.set_state(flag.flager)
       await message.answer('Отправь мне флаг')
    else:
        await message.answer('Вы не зарегистрированны !')




@dp.message(flag.flager)
async def flag_solvs(message: Message, state: FSMContext):
    await state.update_data(flag=message.text)
    data = await state.get_data()
    answer = ["FLAGS"]


    username_oi = message.from_user.username
    username = str(username_oi)
    system_flag = str(data)
    flag_corrective = system_flag[10:]
    flag_correct = flag_corrective[:-2]
    # print(flag_correct)
    with open("solve.txt", "r") as fil:
        solver = fil.read()
        fil.close

       # print((str(username)+str(flag_correct)))
       # print(solver)

    if (str(username)+str(flag_correct)) in str(solver):
        await message.answer("Флаг уже сдан !")
        await state.clear()

    else:
        if flag_correct in answer:
            await message.answer("Отлично, флаг верный !")
            await state.clear()
            with open("solve.txt", "a") as file:
                file.write(f"{username}{flag_correct}\n")
                file.close
        else:
            await message.answer("Неправильный флаг. Попробуй еще раз.")
            await state.clear()



@dp.message(Command('scoreboard'))
async def score(message: Message):
    t.sleep(1)
    with open('scoreboard.txt', 'w'):
        pass
    mas = get_users()
    for i in mas:
        s = 0
        with open('solve.txt', 'r') as file:
            solv = file.read()
            if i in solv:
                s = solv.count(str(i))
                file.close()
            else:
                s = 0
                file.close()
        with open('scoreboard.txt', 'a') as f:
            f.write(f'{i}: {s * 10} баллов\n')
    with open("scoreboard.txt", "r") as fi:
        board = fi.read()
        fi.close()
    await message.answer(f"🏆 Рейтинг участников:\n\n{board}")




async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())