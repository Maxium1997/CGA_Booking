from enum import Enum


class Privilege(Enum):
    SystemManager = (0b1000000, 'System Manager')
    User = (0b1, 'User')


class Identity(Enum):
    Consumer = (1, 'Consumer', '消費者')
    Proprietor = (2, 'Proprietor', '業者')


class Gender(Enum):
    Unset = (0, 'Unset', '尚未設定')
    Male = (1, 'Male', '男')
    Female = (2, 'Female', '女')
    Privacy = (3, 'Privacy', '不公開')