import scrapy
from ..items import EventsItem

class EventSpider(scrapy.Spider):
    name="events"
    start_urls=[
        r"https://www.katasztrofavedelem.hu/modules/vesz/archivum/?date=2022-11-04&type=date&back=https%3A%2F%2Fwww.katasztrofavedelem.hu%2Fmodules%2Fvesz%2Fesemenyterkep%2F%3Fback%3D%23"
    ]

    def parse(self, event, **kwargs):

        items=EventsItem()

        # To get the css tags use the SelectorGadget in Chrome
        # event_info["url"]=response.css(".alert-info").xpath("@href").extract()
        # event_info["title"]=response.css(".alert-info").css(".title::text").extract()
        # event_info["date"]=response.css(".alert-info").css(".date::text").extract()
        # event_info["category"]=response.css(".alert-info").css(".category::text").extract()
        all_events=event.css(".VESZEventArchive").css("a")

        for event in all_events:
            items["url"]=event.xpath("@href").extract_first()
            items["title"]=event.css(".title::text").extract_first()
            items["date"]=event.css(".date::text").extract_first()
            items["category"]=event.css(".category::text").extract_first()

            

            if not all(items.values()):
                continue
            yield items    