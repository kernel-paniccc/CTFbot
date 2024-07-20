from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.requests import is_register
from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete



class Registration(StatesGroup):
    name = State()

class Send_Flag(StatesGroup):
    Flag = State()


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет, это бот zelCTF, кидай мне флаг и получай баллы ! Список команд: /help")


@router.message(Command('registration'))
async def start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not id:
            await message.answer('Введите ваш никнейм:')
            await state.set_state(Registration.name)
        else:
            await message.answer(f'Вы уже зарегистрированны !')
            state.clear()

@router.message(Registration.name)
async def register2(message: Message, state: FSMContext):
    username = message.text
    tg_id = message.from_user.id
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        is_user = await session.scalar(select(User).where(User.username == username))
        if not id and not is_user:
            session.add(User(tg_id=tg_id, username=username, flag_count=0))
            await session.commit()
            state.clear()
            await message.answer('Вы успешно зарегистрированны !')
        elif not id and is_user:
            await message.answer('Данное имя пользователя уже занято. Попробуйте еще раз: /registration')
            state.clear()


@router.message(Command('submit_flag'))
async def submit_flag(message: Message, state: FSMContext):
    is_reg = await is_register(message.from_user.id)
    if is_reg == "0":
        await message.answer("Вы не зарегистрированны ! Для регистрации перейдите на /registration")
        state.clear()
    elif is_reg == '1':
        await message.answer('Отправь мне флаг')
        await state.set_state(Send_Flag.Flag)

@router.message(Send_Flag.Flag)
async def register2(message: Message, state: FSMContext):
    flag = message.text
    print(flag)



@router.message(Command('help'))
async def help(message: Message):
        await message.answer("/start - запуск бота\n"
                             "/registration - регистрация участника\n"
                             "/submit_flag - сдача флага\n"
                             "/scoreboard - рейтинг участников")

@router.message()
async def echo(messange: Message):
    await messange.answer('Я вас не понимаю. Для вывода списка комманд используйте: /help')