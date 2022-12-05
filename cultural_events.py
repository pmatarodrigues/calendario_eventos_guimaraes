

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
