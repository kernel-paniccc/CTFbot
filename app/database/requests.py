from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete

async def is_register(tg_id):
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not id: return "0"
        else: return "1"


# async def submit_flag(tg_id, flag):
#     async with async_session() as session:
#         user_state = await session.scalar(select(Flag).where(Flag.tg_id == tg_id, Flag.flag == flag))
#         if user_state:
#             print('флаг уже сдан')
#         else:
#             session.add(User(tg_id=tg_id, flag=flag))
#             session.query(User).filter(User.tg_id == tg_id).update({'flag_count': User.flag_count + 1})