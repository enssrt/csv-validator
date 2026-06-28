# source/validators.py

from datetime import datetime

def validate_price(value):
    try:
        price = float(value)
        if price > 0:
            return True, None
        else:
            return False, "Цена должна быть строго больше нуля"
    except ValueError:
        return False, "Значение не является числом"
    
def validate_date(value):
    try:
        datetime.strptime(value,"%Y-%m-%d" )
        return True, None
    except ValueError:
        return False, "Некорректный формат даты или несуществующая дата"