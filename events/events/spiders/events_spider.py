import scrapy

class EventSpider(scrapy.Spider):
    name="events"
    start_urls=[
        r"https://www.katasztrofavedelem.hu/modules/vesz/archivum/?date=2022-11-04&type=date&back=https%3A%2F%2Fwww.katasztrofavedelem.hu%2Fmodules%2Fvesz%2Fesemenyterkep%2F%3Fback%3D%23"
    ]

    def parse(self, event, **kwargs):


        # To get the css tags use the SelectorGadget in Chrome
        # event_info["url"]=response.css(".alert-info").xpath("@href").extract()
        # event_info["title"]=response.css(".alert-info").css(".title::text").extract()
        # event_info["date"]=response.css(".alert-info").css(".date::text").extract()
        # event_info["category"]=response.css(".alert-info").css(".category::text").extract()
        all_events=event.css(".VESZEventArchive").css("a")

        for event in all_events:
            event_info={}
            event_info["url"]=event.xpath("@href").extract_first()
            event_info["title"]=event.css(".title::text").extract_first()
            event_info["date"]=event.css(".date::text").extract_first()
            event_info["category"]=event.css(".category::text").extract_first()
            yield event_info    