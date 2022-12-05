

def get_event_name(event_raw):
    return event_raw.select_one(".title .widget_value").h2.getText()


def get_event_categories(categories):
    category = categories.select_one(".primary_category .label").getText()
    return {"category": category}


def get_event_thumbnail(thumb):
    alt = thumb.get('alt')
    link = emguimaraes_link + thumb.get('src')
    return {"link": link, "alt": alt}


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
