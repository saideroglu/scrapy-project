import scrapy

class teknosaSpider(scrapy.Spider):
    name = "teknosa"
    start_urls = ["https://www.teknosa.com/cep-telefonu-c-100001?s=%3Arelevance&page="+str(x)+"" for x in range(1,11)]

    def parse (self,response):
        for products in response.css("div.prd"):
                yield {
                    "seller":"Teknosa",
                    "name":products.css("div.prd").attrib["data-product-name"],
                    "price":products.css("div.prd").attrib["data-product-discounted-price"].replace(".0",""),
                    "link":"https://www.teknosa.com" + products.css("div.prd").attrib["data-product-url"]
                }