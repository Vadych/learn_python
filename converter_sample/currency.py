from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date),)  # Использовать переданный requests
    soup=BeautifulSoup(response.content,'xml')
    nom_from=val_from=nom_to=val_to=Decimal(1.0)
    if cur_from !="RUR":
        nom_from=Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string)
        val_from = str(soup.find('CharCode', text=cur_from).find_next_sibling('Value').string)
        val_from=Decimal(val_from.replace(',','.'))
    if cur_to !="RUR":
        nom_to = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string)
        val_to = str(soup.find('CharCode', text=cur_to).find_next_sibling('Value').text)
        val_to=val_to.replace(",",".")
        val_to=Decimal(val_to)
    a=val_from/nom_from/val_to*nom_to*amount
    pass
    result = a.quantize(Decimal('0.0001'))
    return result  # не забыть про округление до 4х знаков после запятой
