from enum import Enum


class Use(Enum):
    OfficialBusiness = (1, 'Official Business', '公務需求')
    FamilyVisit = (2, 'Family Visit', '眷探需求')
    Guidance = (3, 'Guidance', '視導需求')
    Other = (4, 'Other', '其他需求')


class State(Enum):
    Outstanding = (1, 'Outstanding', '未付款')
    Paid = (2, 'Paid', '已付款')
    Canceled = (3, 'Canceled', '已取消')
    CheckedOut = (4, 'Check Out', '已退房')
