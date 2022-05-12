from pydantic import BaseModel, Field


class Rate(BaseModel):
    time: str = Field(..., example='8:20', description='A flight time')
    adult: int = Field(..., example='800', description='Ticket price for persons over 18 years old')
    teen: int = Field(..., example='700', description='Ticket price for persons from 5 to 18')
    kid: int = Field(..., example='700', description='Ticket price for persons under 5 years old')
    luggage: int = Field(..., example='400', description='Price for additional luggage')
    pet: int = Field(..., example='400', description='Price for pet transfer')
    total: int = Field(..., example='400', description='Total tickets for flight')