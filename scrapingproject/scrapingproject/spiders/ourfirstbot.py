# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import urllib
from random import choice 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class OurfirstbotSpider(scrapy.spiders.CrawlSpider):
    name = 'ourfirstbot'
    allowed_domains = ['rottentomatoes.com']
    start_urls = [
        'https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=1',
        "https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular?page=1"

    ]
    # regex for atmost 4 of slashes 
    rules = (
        Rule(LinkExtractor(deny=r"https:\/\/www.rottentomatoes.com\/m\/.*\/.*", allow=r"https:\/\/www.rottentomatoes.com\/m\/.*"), callback='parse_item', follow=True),
    )
    def parse_item(self, response):
        # extract the title of the page
        title = response.css('title::text').get()
        if not title:
            return
        title = str(title)
        #url of the response
        url = response.url 
        for item in zip(title, url):
            all_items = {
                'url': url,
                'headings' : title,
            }            
            yield all_items

    '''def parse(self, response):
        #yield response
        headings = response.css('.mw-headline').extract()       
        datas = response.css('ul').extract()               
        for item in zip(headings, datas):
            all_items = {
                'url': response.url,
                'headings' : BeautifulSoup(item[0]).text,
                'datas' : BeautifulSoup(item[1]).text,
            }            
            yield all_items
        return
        # get all the links on the page
        all_links = response.css('a::attr(href)').extract()
        all_links = [link for link in all_links if link.startswith("/wiki/")]
        # randomly choose one of the linnk
        random_link = choice(all_links)
        all_links.remove(random_link)
        # construct the absolute url to the next page
        print("Random link is: ", "\n"*100, random_link)
        next_page = response.urljoin(random_link)
        # yield scrapy.Request object for the next page
        self.parse(next_page)'''