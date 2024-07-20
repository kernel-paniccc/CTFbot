from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete

async def is_register(tg_id):
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not id: return "0"
        else: return "1"
