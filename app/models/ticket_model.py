from datetime import date

from pydantic import BaseModel

from app.enums.documents_enum import DocumentsEnum
from app.enums.gender_enum import GenderEnum
from app.models.user_model import User


class Ticket(BaseModel):
    pet: int = 0
    luggage: int = 0
    price: int

class TicketUser(Ticket):
    user: User


class BuyTicket(BaseModel):
    pet: int = 0
    luggage: int = 0
    first_name: str
    middle_name: str | None = None
    last_name: str
    gender: GenderEnum
    document_type: DocumentsEnum
    document_number: str
    date_birth: date
