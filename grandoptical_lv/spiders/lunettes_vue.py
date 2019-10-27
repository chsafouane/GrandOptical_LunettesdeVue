# -*- coding: utf-8 -*-
import scrapy


class LunettesVueSpider(scrapy.Spider):
    name = 'lunettes_vue'
    allowed_domains = ['www.grandoptical.com']
    start_urls = ['https://www.grandoptical.com/toutes-nos-lunettes/lunettes-de-vue/c/59/']

    def parse(self, response):
        for product in response.xpath("//div[@class='product-list--item--wrapper--simple-product']"):
            brand = product.xpath(".//span[@class='product_brand']/text()").get()
            model = product.xpath(".//span[@class='product_name head product-list--name product-list--name--simple-product']/span/text()").get()
            new_price = product.xpath(".//div[@class='new-price hide product-list--price--new product-list--price--new--simple-product']/text()").get()
            old_price = product.xpath(".//div[@class='old-price hide product-list--price--old product-list--price--old--simple-product']/text()").get()
            price = product.xpath(".//div[@class='simple-price   product-list--price product-list--price--simple  product-list--price--simple-glass product-list--price--simple--simple-product']/text()").get()
            
            yield {
                "brand": brand,
                "model": model,
                "new_price": new_price,
                "old_price": old_price,
                "price": price
            }

        
        next_one = response.xpath("//li[@class='first active']/span/text()").get()
        if next_one is None:
            next_one = response.xpath("//li[@class='active']/span/text()").get()

        next_one = int(next_one) + 1
        next_page = response.xpath(f"//a[starts-with(@href, '/toutes-nos-lunettes/lunettes-de-vue/c/59?page={next_one}')]/@href").get()

        if next_page is not None:
            next_page = "https://www.grandoptical.com" + next_page
            yield scrapy.Request(url = next_page, callback = self.parse)

