# 함수 정의

from datetime import datetime

def calculate_age(birthdate):
    today = datetime.today()
    birth = datetime.strptime(birthdate, "%Y-%m-%d")
    age = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        age = age-1
    return age



def convert_currency(amount, from_currency, to_currency, rate):
    converted = amount * rate
    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate,
        "converted_amount": converted
    }

def convert_currrency2(amount, rate=1330):
    return amount*rate



def calculate_bmi  (weight, height):
    # height_m = height/100
    if height <= 0:
        return "Height must be greater than zero."
    bmi = weight / (height ** 2)
    return round(bmi, 2)
