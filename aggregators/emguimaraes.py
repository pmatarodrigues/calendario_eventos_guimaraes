from datetime import datetime
from bs4 import BeautifulSoup
import json
from utils.EventScrapper import EventScrapper
from utils.EventParser import EventParser

class Emguimaraes:
    baseUrl = "https://em.guimaraes.pt/"

    @classmethod
    def get_events(cls):
        eventos = {}
        page = 1
        date = datetime.today()

        while (True):
            url = f'{cls.baseUrl}agenda?geo_events_list_29_page={str(page)}&paginating=true&start_date={str(date)}'
            html_doc = EventScrapper.getHTMLdoc(url)
            soup = BeautifulSoup(html_doc, 'html.parser')

            event_data = {}

            for event in soup.select('.cell .linl_block .linl_inner'):
                date = {
                    "dates": event.select_one(".dates .widget_value"),
                    "timetable": event.select_one(".timetable .widget_value")
                }
                title = {
                    "title": event.select_one(".title .widget_value"),
                    "summary": event.select_one(".summary .widget_value")
                }
                location = {
                    "venue_id": event.select_one(".venue_id .widget_value"),
                    "descriptive_location": event.select_one(
                        ".descriptive_location .widget_value"),
                    "address": event.select_one(".address .widget_value .writer_text")
                }
                thumbnail = event.select_one(".thumbnail .widget_value img")
                categories = event.select_one(".categories_list .widget_value")

                event_data = EventParser.parse(cls, date, title, location, thumbnail, categories)
                title = event.find('h2').getText()

                eventos[title] = event_data

            if event_data == {}: break

            page += 1

        return eventos


    @classmethod
    def get_event_name(cls, event_raw):
        return event_raw.select_one(".title .widget_value").h2.getText()

    @classmethod
    def get_event_categories(cls,categories):
        category = categories.select_one(".primary_category .label").getText()
        return {"category": category}

    @classmethod
    def get_event_thumbnail(cls, thumb):
        alt = thumb.get('alt')
        link = f'{cls.baseUrl}{thumb.get("src")}'
        return {"link": link, "alt": alt}

    @classmethod
    def get_event_location(cls, location_detailed, location_simple, address):
        if location_detailed is None:
            if location_simple is not None:
                return {'place': location_simple.getText()}
        else:
            data = json.loads(location_detailed.a['data-location'])
            del data['id']
            del data['address']
            place = ""
            if address is not None:
                for ad in address.findAll('p'):
                    place += ' ' + ad.getText()
            data['address'] = place
            data = json.dumps(data)
            return data

    @classmethod
    def get_event_title(cls, title, summary):

        title_data = {
            "title":
            title.h2.getText(),
            "summary":
            summary.p.getText().replace("\xa0", ". ")
            if summary is not None else ""
        }
        return title_data

    @classmethod
    def get_event_date(cls, date, time_table):
        time = time_table.select_one(
            ".writer_text").p.getText() if time_table is not None else "Todo o Dia"
        start = date.select_one(".begin_date")
        isFullDayEvent = start is None

        if isFullDayEvent:
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

        return date_formatted
