from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.requests import is_register
from app.database.models import async_session
from app.database.models import User, Flag
from sqlalchemy import select, update, delete

from dotenv import load_dotenv

import json
import os



class Registration(StatesGroup):
    name = State()


class Send_Flag(StatesGroup):
    Flag = State()


load_dotenv()
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет, это бот zelCTF 😎, кидай мне флаг и получай баллы ! Список команд: /help")


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
            await state.clear()

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
            await message.answer('Вы успешно зарегистрированы ! 🎉')
            await state.clear()
        elif not id and is_user:
            await message.answer('Данное имя пользователя уже занято. Попробуйте еще раз: /registration')
            await state.clear()


@router.message(Command('submit_flag'))
async def submit_flag(message: Message, state: FSMContext):
    is_reg = await is_register(message.from_user.id)
    if is_reg == "0":
        await message.answer("Вы не зарегистрированны ! Для регистрации перейдите на /registration")
    elif is_reg == '1':
        await message.answer('Отправь мне флаг 🚩')
        await state.set_state(Send_Flag.Flag)

@router.message(Send_Flag.Flag)
async def register2(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    flag = message.text
    flag_list = json.loads(os.environ['FLAGS'])
    if flag in flag_list:

        async with async_session() as session:
            user_state = await session.scalar(select(Flag).where(Flag.tg_id == tg_id, Flag.flag == flag))
            if user_state:
                await message.answer('Флаг уже сдан !')
                await state.clear()
            else:
                session.add(Flag(tg_id=tg_id, flag=flag))
                user = await session.scalar(select(User).where(User.tg_id == tg_id))
                user.flag_count += 1
                await session.commit()
                await message.answer('Отлично, флаг верный !')
                await state.clear()

    elif flag not in flag_list:
        await message.answer('Неверный флаг. Попробуйте еще раз ! ❌')


@router.message(Command('profile'))
async def submit_flag(message: Message):
    is_reg = await is_register(message.from_user.id)
    if is_reg == "0":
        await message.answer("Вы не зарегистрированны ! Для регистрации перейдите на /registration")
    elif is_reg == '1':
        async with async_session() as session:
            tg_id = message.from_user.id
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            await message.answer(f'🔒 Профиль:\n\n😎 Имя пользователя: {user.username}\n🚩 Кол-во сданных флагов: {user.flag_count}\n')


@router.message(Command('help'))
async def help(message: Message):
        await message.answer("/start - запуск бота\n"
                             "/registration - регистрация участника\n"
                             "/submit_flag - сдача флага\n"
                             "/scoreboard - рейтинг участников\n"
                             "/profile - профиль участника\n")

@router.message()
async def echo(messange: Message):
    await messange.answer('Я вас не понимаю. Для вывода списка комманд используйте: /help')