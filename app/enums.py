from enum import Enum


class DescriptiveEnum(Enum):
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, description: str = None):
        self._description_ = description

    @classmethod
    def choices(cls):
        return [(choice.name, choice.description) for choice in cls]

    # def __str__(self):
    #     return self.value

    # this makes sure that the description is read-only
    @property
    def description(self):
        return self._description_


class PriceUnit(DescriptiveEnum):
    egp = 0, "E£"
    usd = 1, "$"


class SpaceUnit(DescriptiveEnum):
    hour = 0, "ساعة"
    day = 1, "يوم"


class ToolUnit(DescriptiveEnum):
    hour = 0, "ساعة"
    day = 1, "يوم"
    gram = 2, "جرام"
    trivial = 3, "ثابت"


class ReservationTypes(Enum):
    space = 0
    tool = 1


class PaymentTypes(DescriptiveEnum):
    no_payment = 0, "غير مدفوع"
    down_payment = 1, "مدفوع جزئيا"
    full_payment = 2, "مدفوع"


class Gender(DescriptiveEnum):
    male = 0, "ذكر"
    female = 1, "أنثى"
    prefer_not_answer = 2, "أرجو عدم التوضيح"
