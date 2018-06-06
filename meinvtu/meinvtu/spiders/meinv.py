# -*- coding: utf-8 -*-
import scrapy
from meinvtu.items import MeinvtuItem


class MeinvSpider(scrapy.Spider):
    name = 'meinv'
    allowed_domains = ['www.27270.com']
    start_urls = ['http://www.27270.com/ent/meinvtupian/list_11_1.html']

    def parse(self, response):
        items = []
        url_splits = []
        atlas_tags = response.xpath('//div[@class="MeinvTuPianBox"]/ul/li')
        for atlas_tag in atlas_tags:
            item = MeinvtuItem()
            item['img_urls'] = []
            item['atlas_names'] = atlas_tag.xpath('./a[@class="tit"]/@title').extract_first()
            item['atlas_urls'] = atlas_tag.xpath('./a[@class="tit"]/@href').extract_first()
            url_split = item['atlas_urls'].split('/')
            url_splits.append(url_split)
            items.append(item)

        for num in range(len(items)):
            item = items[num]
            url_split = url_splits[num]
            yield scrapy.Request(item['atlas_urls'], meta={'item1': item, 'url_split': url_split},
                                 callback=self.parse_item)
        #yield item

        new_page = response.xpath('//div[@class="NewPages"]/ul/li')
        # url_head = 'http://www.27270.com/ent/meinvtupian/'
        url_end = new_page[-2].xpath('./a/@href').extract_first()
        next_url = 'http://www.27270.com/ent/meinvtupian/' + url_end
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse)
        #yield item

    def parse_item(self, response):
        item = response.meta['item1']
        # item['img_urls'] = []
        img_url = response.xpath('//div[@class="articleV4Body"]/p/a/img/@src').extract_first()
        item['img_urls'].append(img_url)
        url_split = response.meta['url_split']
        url_mid = url_split[-2]
        next_url = response.xpath('//ul[contains(@class,"articleV4Page")]/li[@id="nl"]/a/@href').extract_first()
        if next_url is not '##':
            next_urls = 'http://www.27270.com/ent/meinvtupian/%s/%s' % (url_mid, next_url)
            yield scrapy.Request(next_urls, meta={'item1': item, 'url_split': url_split}, callback=self.parse_item)
        yield item