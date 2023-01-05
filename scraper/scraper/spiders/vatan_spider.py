import scrapy

class vatanSpider(scrapy.Spider):
    name = "vatan"
    start_urls = ["https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=%d" % i for i in range (1,11)]

    def parse (self,response):
        for products in response.css("div.product-list.product-list--list-page"):
                yield {
                    "seller":"Vatan Bilgisayar",
                    "name":products.css("div.product-list__product-name h3::text").get(),
                    "price":products.css("span.product-list__price::text").get().replace(".",""),
                    "link":"https://www.vatanbilgisayar.com" + products.css("a.product-list__image-safe-link.sld").attrib["href"]
                }