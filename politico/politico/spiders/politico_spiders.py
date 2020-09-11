import scrapy
from scrapy import Spider
from scrapy import Selector

from politico.items import PoliticoItem


class PoliticoSpider(scrapy.Spider):
    name = 'politico'
    allowed_domains = ['elcomercio.com','ecuavisa.com','ecuavisa.com','rts.com.ec','tctelevision.com','eltelegrafo.com.ec','teleamazonas.com','eluniverso.com']
    start_urls = [
    'https://www.elcomercio.com/actualidad',
    'https://www.elcomercio.com/data',
    'https://www.elcomercio.com/tendencias',
    'https://www.ecuavisa.com/noticias/nacional',
    'https://www.ecuavisa.com/noticias/politica',
    'https://www.ecuavisa.com/historico/noticias/politica',
    'http://www.rts.com.ec/noticias/actualidad-1',
    'https://www.tctelevision.com/noticias',
    'https://www.tctelevision.com/politica',
    'https://www.eltelegrafo.com.ec/contenido/categoria/1/politica',
    'http://www.teleamazonas.com/noticiero-24-horas/noticias-nacionales'
    ]
    #Add all url pages
    for i in range(1,100):
        start_urls.append('https://www.eluniverso.com/politica?page='+str(i))
        start_urls.append('https://www.ecuavisa.com/historico/noticias/nacional?page='+str(i))
        start_urls.append('https://www.ecuavisa.com/historico/noticias/politica?page='+str(i))
        start_urls.append('https://www.tctelevision.com/noticias/page/'+str(i))
        start_urls.append('https://www.tctelevision.com/politica/page/'+str(i))
        k=i*12
        start_urls.append('https://www.eltelegrafo.com.ec/contenido/categoria/1/politica?start='+str(k))

    def parse(self, response):
        item=PoliticoItem()
        headlines=Selector(response).xpath('//div[@class="article articulo-grande"]')
        for headline in headlines:
            item['message']=headline.xpath('a/text()').extract()[0]
            item['url']=headline.xpath('a/@href').extract()[0]
            yield item
        headlines=Selector(response).xpath('//div[@class="views-field views-field-title"]')
        for headline in headlines:
            item['message']=headline.xpath('span/a/text()').extract()[0]
            item['url']='https://www.ecuavisa.com'+headline.xpath('span/a/@href').extract()[0]
            yield item
        headlines=Selector(response).xpath('//div[@class="col-12 col-sm-8 col-md-8 col-lg-8 col-xl-8 pd-left-ultimas-noticias"]')
        for headline in headlines:
            item['message']=headline.xpath('a/h2/text()').extract()[0]
            item['url']=headline.xpath('a/@href').extract()[0]
            yield item
        headlines=Selector(response).xpath('//div[@class="qt-itemcontents"]')
        for headline in headlines:
            item['message']=headline.xpath('h5/a/text()').extract()[0]
            item['url']=headline.xpath('h5/a/@href').extract()[0]
            yield item
        headlines=Selector(response).xpath('//div[@class="bp-head"]')
        for headline in headlines:
            item['message']=headline.xpath('h2/a/text()').extract()[0]
            item['url']=headline.xpath('h2/a/@href').extract()[0]
            yield item
        headlines=Selector(response).xpath('//div[@class="summary views-fieldset"]')
        for headline in headlines:
            item['message']=headline.xpath('h2/a/text()').extract()[0]
            item['url']='www.eluniverso.com'+headline.xpath('h2/a/@href').extract()[0]
            yield item