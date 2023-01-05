import scrapy

class mediamarktSpider(scrapy.Spider):
    name = "mediamarkt"
    #start_urls = ["https://www.mediamarkt.com.tr/tr/category/_cep-telefonlar%C4%B1-504171.html"]
    start_urls = ["https://www.mediamarkt.com.tr/tr/category/_cep-telefonlar%C4%B1-504171.html?searchParams=&sort=suggested&view=&page=1"]
    def parse (self,response):
        for products in response.css("div.product-wrapper"):
            try:
                yield {
                    "seller":"Mediamarkt",
                    "name":products.css("div.content h2 a::text").get().replace("\r\n\t\t\t\t",""),
                    "price":products.css("div.price.small::text").get().replace(",-",""),
                    "link":"https://www.mediamarkt.com.tr" + products.css("div.content h2 a").attrib["href"]
                }
            except:
                yield {
                    "seller":"Mediamarkt",
                    "name":products.css("div.content h2 a::text").get().replace("\r\n\t\t\t\t",""),
                    "price":"Ürün Mevcut değil",
                    "link":"https://www.mediamarkt.com.tr" + products.css("div.content h2 a").attrib["href"]
                }
            next_page = response.css("li.pagination-next a").attrib["href"]
            if next_page is not None:
                yield response.follow(next_page, callback = self.parse)
