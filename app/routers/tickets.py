import json
import uuid

from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, select, exc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app import main
from app.db.database import get_db
from app.db.models import UserDB, TicketDB
from app.enums.airports_enum import AirportsEnum
from app.models.rate_model import Rate
from app.models.ticket_model import Ticket
from app.models.user_model import User
from app.utils import get_age_category, compare_departure_arrival

tickets_router = APIRouter(prefix='/tickets')


@tickets_router.get('{dep}/{arr}', response_model=list[Rate])
async def get_tickets(dep: AirportsEnum = Path(..., description='departure airport'),
                      arr: AirportsEnum = Path(..., description='arrival airport')):
    """Get info about flights"""

    await compare_departure_arrival(dep, arr)
    data = await main.app.state.redis_repo.get_all_by_key(f'{dep}-{arr}')

    return [Rate(time=k, **json.loads(v)) for k, v in data.items()]


@tickets_router.post('{dep}/{arr}/{flight_time}', status_code=201)
async def buy_tickets(
        tickets: list[Ticket],
        flight_time: str = Path(..., description='flight time'),
        dep: AirportsEnum = Path(..., description='departure airport'),
        arr: AirportsEnum = Path(..., description='arrival airport'),
        db_sesion: AsyncSession = Depends(get_db)):
    """Buy ticket"""

    await compare_departure_arrival(dep, arr)

    flight_name: str = f'{dep}-{arr}'
    flight_data: str = await main.app.state.redis_repo.get_by_key(flight_name, flight_time)

    if not flight_data:
        raise HTTPException(400, detail="Flight not found")

    flight_data: dict = json.loads(flight_data)
    for ticket in tickets:

        # Check if user exists in db
        user: UserDB = (await db_sesion.execute(select(UserDB).filter(and_(UserDB.document_type == ticket.document_type,
                                                                           UserDB.document_number == ticket.document_number)))).scalar()

        if not user:
            user: UserDB = UserDB(**dict(id=uuid.uuid4(),
                                         first_name=ticket.first_name,
                                         last_name=ticket.last_name,
                                         middle_name=ticket.middle_name,
                                         gender=ticket.gender,
                                         document_type=ticket.document_type,
                                         document_number=ticket.document_number,
                                         date_birth=ticket.date_birth))
            db_sesion.add(user)

        ticket: TicketDB = TicketDB(**dict(id=uuid.uuid4(),
                                           flight_time=flight_time,
                                           pet=ticket.pet,
                                           luggage=ticket.luggage,
                                           price=flight_data[(await get_age_category(ticket.date_birth))] + flight_data[
                                               'luggage'] * ticket.luggage + flight_data['pet'] * ticket.pet,
                                           flight_name=flight_name))
        ticket.user_id = user.id
        try:
            db_sesion.add(ticket)
            await db_sesion.commit()
        except exc.IntegrityError as e:
            await db_sesion.rollback()

            # in case when user already buy a ticket for this flight
            if e.orig.pgcode == '23505':
                raise HTTPException(status_code=400, detail='Some of users already bought tickets')
            raise HTTPException(status_code=500)
    else:
        # decrease total count of tickets
        flight_data['total'] -= len(tickets)
        await main.app.state.redis_repo.set_by_key_field(flight_name, flight_time, json.dumps(flight_data))
    return Response(status_code=201)


@tickets_router.get('{dep}/{arr}/{flight_time}', response_model=list[Ticket])
async def get_bought_tickets_info(dep: AirportsEnum = Path(..., description='departure airport'),
                                  arr: AirportsEnum = Path(..., description='arrival airport'),
                                  flight_time: str = Path(..., description='flight time'),
                                  db_session: AsyncSession = Depends(get_db)):
    """Get information about bought tickets"""

    await compare_departure_arrival(dep, arr)

    data = (await db_session.execute(select([TicketDB, UserDB])
                                     .join(UserDB, TicketDB.user_id == UserDB.id)
                                     .filter(and_(TicketDB.flight_time == flight_time,
                                                  TicketDB.flight_name == f'{dep}-{arr}'))))
    result = []
    for i in data:
        user = User.from_orm(i[1])
        ticket = Ticket(id=i[0].id, flight_time=i[0].flight_time, flight_name=i[0].flight_name, pet=i[0].pet,
                        luggage=i[0].luggage, price=i[0].price, user=user)
        result.append(ticket)
    return result
