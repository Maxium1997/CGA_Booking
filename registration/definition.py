from enum import Enum


class Privilege(Enum):
    SystemManager = (0b1000000, 'System Manager')
    User = (0b1, 'User')


class Identity(Enum):
    Traveler = (1, 'Traveler', '旅客')
    Proprietor = (2, 'Proprietor', '業者')


class Gender(Enum):
    Unset = (0, 'Unset', '尚未設定')
    Male = (1, 'Male', '男')
    Female = (2, 'Female', '女')
    Privacy = (3, 'Privacy', '不公開')


class ServeState(Enum):
    Active = (1, 'Active Duty', '現役')
    Retirement = (2, 'Retirement', '退役')
    Exemption = (3, 'Exemption', '免役')
    Discharged = (4, 'Discharged', '除役')


class MilitaryService(Enum):
    Obligatory = (1, 'Obligatory military service', '義務役')
    Regular = (2, 'Service for regulars', '常備役')
    Voluntary = (3, 'Voluntary military service', '志願役')
    Reservist = (4, 'Reservist', '後備軍人')
