import scrapy
from ..items import EventsItem
import json
import parse

class EventSpider(scrapy.Spider):
    name="events"

    start_urls=[rf"https://www.katasztrofavedelem.hu/modules/vesz/archivum/?yearMonth={year}-{month:02}&type=yearMonth&back=https%3A%2F%2Fwww.katasztrofavedelem.hu%2Fmodules%2Fvesz%2Fesemenyterkep%2F%3Fback%3D" 
    for year in range(2017,2023) for month in range(1,13)]

    def parse(self, response, **kwargs):

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
        script_string=response.css("div.page-text").css("script::text")[-1].extract()
        script_format='{beginning}, {string_dict});'
        parsed=parse.parse(script_format, script_string)

        event_infos=json.loads(parsed["string_dict"])
        event_infos["update_info"] = event_infos.pop("update")
        event_infos["event_id"] = event_infos.pop("id")
        event_infos["event_date"] = event_infos.pop("date")
        event_infos["subtitle"] = event_infos.pop("lead")


        for k in event_infos:
            items[k]=event_infos[k]

        items["event_url"]=response.url

        yield items