import asyncio
import logging
import os
from datetime import date

import nest_asyncio
from celery import Celery
from celery import shared_task
from celery.schedules import crontab
from dotenv import load_dotenv
from sqlalchemy.future import select

from app.db import session_maker
from app.db.conntection import db_session
from app.bookings.booking import Booking

load_dotenv()
nest_asyncio.apply()

celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery.autodiscover_tasks(['app.tasks'])

celery.conf.beat_schedule = {
    'remove-expired-bookings-every-minute': {
        'task': 'app.tasks.tasks.remove_expired_bookings',
        'schedule': crontab(minute="*")
    },
    'test-task-every-minute': {
        'task': 'app.tasks.tasks.test_task',
        'schedule': crontab(minute="*")
    },
}


@shared_task
def remove_expired_bookings():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_remove_expired_bookings())


async def _remove_expired_bookings():
    async with session_maker() as session:
        db_session.set(session)
        async with session.begin():
            current_date = date.today()
            query = select(Booking).where(Booking.end_date < current_date)
            result = await session.execute(query)
            expired_bookings = result.scalars().all()
            print(f"Просроченные: {expired_bookings}")
            if expired_bookings:
                for booking in expired_bookings:
                    print(f"Просроченный: {booking}")
                    await session.delete(booking)
                await session.commit()


@shared_task
def test_task():
    logging.info("Test task executed")
    print("Test task executed")
