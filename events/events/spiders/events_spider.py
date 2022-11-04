import scrapy
from ..items import EventsItem

class EventSpider(scrapy.Spider):
    name="events"
    # start_urls=[
    #     r"https://www.katasztrofavedelem.hu/modules/vesz/archivum/?date=2022-11-04&type=date&back=https%3A%2F%2Fwww.katasztrofavedelem.hu%2Fmodules%2Fvesz%2Fesemenyterkep%2F%3Fback%3D%23"
    # ]

    start_urls=[rf"https://www.katasztrofavedelem.hu/modules/vesz/archivum/?yearMonth={year}-{month:02}&type=yearMonth&back=https%3A%2F%2Fwww.katasztrofavedelem.hu%2Fmodules%2Fvesz%2Fesemenyterkep%2F%3Fback%3D" 
    for year in range(2017,2023) for month in range(1,13)]

    def parse(self, response, **kwargs):


        # To get the css tags use the SelectorGadget in Chrome
        # event_info["url"]=response.css(".alert-info").xpath("@href").extract()
        # event_info["title"]=response.css(".alert-info").css(".title::text").extract()
        # event_info["date"]=response.css(".alert-info").css(".date::text").extract()
        # event_info["category"]=response.css(".alert-info").css(".category::text").extract()
        all_events=response.css(".VESZEventArchive").css("a")

        for event in all_events:
            event_infos={}
            event_infos["url"]=event.xpath("@href").extract_first()
            event_infos["title"]=event.css(".title::text").extract_first()
            event_infos["date"]=event.css(".date::text").extract_first()
            event_infos["category"]=event.css(".category::text").extract_first()


            if not all(event_infos.values()):
                continue

            yield response.follow(url=event_infos["url"], callback=self.parse_event)    

    def parse_event(self,response):

        items=EventsItem()

        items["title"]=response.css("h2::text").extract_first()
        items["url"]=response.url
        items["date"]=response.css(".date::text").extract_first()
        items["category"]=response.css(".category::text").extract_first()
        items["subtitle"]=response.css(".lead::text").extract_first()
        items["content"]=response.css(".VESZEventInfo .content::text").extract_first()
        items["location"]=response.css(".location::text").extract_first()

        yield items