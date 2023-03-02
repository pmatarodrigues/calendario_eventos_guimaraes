class EventParser:
    @classmethod
    def parse(cls, aggregator, date, title, location, thumbnail, categories):
        date = aggregator.get_event_date(date["dates"], date["timetable"])

        title = aggregator.get_event_title(title["title"], title["summary"])

        location = aggregator.get_event_location(
            location["venue_id"],
            location["descriptive_location"],
            location["address"]
        )

        thumbnail = aggregator.get_event_thumbnail(thumbnail)

        categories = aggregator.get_event_categories(categories)

        event_data = {
            "title": title,
            "date": date,
            "location": location,
            "categories": categories,
            "thumbnail": thumbnail
        }

        return event_data
