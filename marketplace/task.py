from celery import shared_task
from requests import get
from django.conf import settings
from django.core.mail import send_mail
from yaphets.settings import EMAIL_HOST_USER,RECAPTCHA_PUBLIC_KEY


@shared_task
def get_user_currency():

    valuto_dict = {"all": "lek", "usd": "$", "afn": "؋", "ars": "$", "awg": "ƒ", "aud": "$", "azn": "ман", "bsd": "$", "bbd": "$", "byr": "p.", "eur": "€", "bzd": "bz$", "bmd": "$", "bob": "$b", "bam": "km", "bwp": "p", "bgn": "лв", "brl": "r$", "gbp": "£", "bnd": "$", "khr": "៛", "cad": "$", "kyd": "$", "clp": "$", "cny": "¥", "cop": "$", "crc": "₡", "hrk": "kn", "cup": "₱", "czk": "kč", "dkk": "kr", "dop": "rd$", "xcd": "$", "egp": "£", "svc": "$", "fkp": "£", "fjd": "$", "ghc": "¢", "gip": "£", "gtq": "q", "ggp": "£", "gyd": "$", "hnl": "l", "hkd": "$", "huf": "ft", "isk": "kr", "inr": "₹", "idr": "rp", "irr": "﷼", "imp": "£", "ils": "₪", "jmd": "j$", "jpy": "¥", "jep": "£", "kzt": "лв", "kpw": "₩", "krw": "₩", "kgs": "лв", "lak": "₭", "lvl": "ls", "lbp": "£", "lrd": "$", "chf": "chf", "ltl": "lt", "mkd": "ден", "myr": "rm", "mur": "₨", "mxn": "$", "mnt": "₮", "mzn": "mt", "nad": "$", "npr": "₨", "ang": "ƒ", "nzd": "$", "nio": "c$", "ngn": "₦", "nok": "kr", "omr": "﷼", "pkr": "₨", "pab": "b/.", "pyg": "gs", "pen": "s/.", "php": "php", "pln": "zł", "qar": "﷼", "ron": "lei", "rub": "руб", "shp": "£", "sar": "﷼", "rsd": "дин.", "scr": "₨", "sgd": "$", "sbd": "$", "sos": "s", "zar": "r", "lkr": "₨", "sek": "kr", "srd": "$", "syp": "£", "twd": "nt$", "thb": "฿", "ttd": "tt$", "try": "₺", "trl": "£", "tvd": "$", "uah": "₴", "uyu": "$u", "uzs": "лв", "vef": "bs", "vnd": "₫", "yer": "﷼", "zwd": "z$"}

    response = get(f'https://ipapi.co/json/?key={settings.LOCATION_API_KEY}')
    curency = response.json()["currency"]
    currency = curency.lower()
    url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@2024-03-06/v1/currencies/inr.json"
    resp = get(url)
    data = resp.json()
    try:
        inr_user_value = data['inr'][currency]
        symbol = valuto_dict[currency]
    except:
        inr_user_value = data['inr']['usd']
        symbol = valuto_dict['usd']
    return {"symbol": symbol, "inr_user_value": inr_user_value}


@shared_task
def sendmail(subject,email_body,to_list):
    send_mail(subject, email_body, EMAIL_HOST_USER, to_list, fail_silently=True)