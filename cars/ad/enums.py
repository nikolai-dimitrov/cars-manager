from enum import Enum


class Fuel(Enum):
    diesel = 'Diesel'
    petrol = 'Petrol'
    gas = 'Gas'

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]


class BodyType(Enum):
    sedan = 'Sedan'
    touring = 'Touring'
    coupe = 'Coupe'
    suv = 'SUV'

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]


class Transmission(Enum):
    manual = 'Manual'
    automatic = 'Automatic'

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]
