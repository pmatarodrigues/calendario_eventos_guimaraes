from bs4 import BeautifulSoup
import requests
import re
import json
from unidecode import unidecode

emguimaraes_link = "https://em.guimaraes.pt"


def getHTMLdoc(url):

    response = requests.get(url, verify=False)

    return response.text




def get_event_name(event_raw):
    return event_raw.select_one(".title .widget_value").h2.getText()


def get_event_categories(categories):
    category = categories.select_one(".primary_category .label").getText()
    return {"category": category}


def get_event_thumbnail(thumb):
    alt = thumb.get('alt')
    link = emguimaraes_link + thumb.get('src')
    return {"link": link, "alt": alt}


def get_event_location(location_detailed, location_simple, address):
    if location_detailed is None:
        if location_simple is not None:
            return {'place': location_simple.getText()}
    else:
        data = location_detailed.a['data-location']
        del data['id']
        del data['address']
        place = ""
        if address is not None:
            for ad in address.findAll('p'):
                place += ' ' + ad.getText()
        data['address'] = place
        return data


def get_event_title(title, summary):

    title_data = {
        "title":
        title.h2.getText(),
        "summary":
        summary.p.getText().replace("\xa0", ". ")
        if summary is not None else ""
    }
    return title_data


def get_event_date(date, time_table):

    time = time_table.select_one(
        ".writer_text").p.getText() if time_table is not None else "Todo o Dia"
    # start = date.select_one(".begin_date")
    start = date.select_one(".begin_date")
    if start is None:
        start = date.select_one(".date")
    else:
        end = date.select_one(".end_date")
        end_day = end.find(class_="dias").getText()
        end_month = end.find(class_="mes_extenso").getText()
        end_weekday = end.find(class_="dia_semana_extenso").getText()

    start_day = start.find(class_="dias").getText()
    start_month = start.find(class_="mes_extenso").getText()
    start_weekday = start.find(class_="dia_semana_extenso").getText()

    date_formatted = {
        "start_day": start_day,
        "start_month": start_month,
        "start_weekday": start_weekday,
        "end_day": end_day if 'end_day' in locals() else "",
        "end_month": end_month if 'end_month' in locals() else "",
        "end_weekday": end_weekday if 'end_weekday' in locals() else "",
        "time": time
    }
    # print(date_formatted)

    return date_formatted


url = "http://em.guimaraes.pt/agenda"

html_doc = getHTMLdoc(url)

soup = BeautifulSoup(html_doc, 'html.parser')

titulos = soup.findAll('h2')

eventos = {}
# print(soup.select(".cell .linl_block .linl_inner"))
for event in soup.select('.cell .linl_block .linl_inner'):
    # print(event)

    event_data = parse_event(event)

    titulo = event.find('h2').getText()
    # print(event.select_one(".summary").p)
    eventos[titulo] = {
        "titulo": titulo,
        # "subtitulo": event.find('.summary p'),
        # "data": ,
        # "local": ,
        # "tema":
    }

# print(eventos)
