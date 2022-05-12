import datetime

from fastapi import HTTPException


async def get_age_category(dof: datetime.date) -> str:
    now = datetime.datetime.now()
    age = now.year - dof.year
    if age < 5:
        return 'kid'
    elif age < 18:
        return 'teen'
    else:
        return 'adult'


async def compare_departure_arrival(dep: str, arr: str) -> None | HTTPException:
    if dep == arr:
        raise HTTPException(400, detail="Departure and Arrival can't be equal")
    return