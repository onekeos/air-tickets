from datetime import date

from pydantic import BaseModel

from app.enums.documents_enum import DocumentsEnum
from app.enums.gender_enum import GenderEnum
from app.models.user_model import User


class Ticket(BaseModel):
    user: User
    pet: int = 0
    luggage: int = 0
    price: int
