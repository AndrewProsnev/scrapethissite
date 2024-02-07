import scrapy


class Ex1Spider(scrapy.Spider):
    name = "ex1"
    allowed_domains = ['scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/ajax-javascript/']

    async def parse(self, response, **kwargs):
        # Парсинг ссылок и формирование запросов для каждого года
        for year in response.xpath('//section/div/div[4]/div/a/text()').extract():
            yield scrapy.Request(
                f'https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={year}',
                callback=self.parse_page,
                cb_kwargs={'year': year})

    async def parse_page(self, response, **kwargs):
        # Обработка полученных данных на странице с фильмами
        # Парсинг данных JSON и добавление их в объект
        item = {
            'year': kwargs['year'],
            'films': response.json(),
        }
        yield item
