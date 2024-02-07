import scrapy
from urllib.parse import urljoin
from scrapy.http import TextResponse


class Ex2Spider(scrapy.Spider):
    name = "ex2"
    allowed_domains = ['scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/forms/']

    async def parse(self, response, **kwargs):
        # Если ответ не является объектом TextResponse, преобразуем его
        if not isinstance(response, TextResponse):
            response = TextResponse(url=response.url, body=response.body, encoding='utf-8')

        # Отправляем форму запроса с данными ("q": "New York") и передаем управление в метод after_response
        yield scrapy.FormRequest.from_response(
            response,
            formdata={"q": "New York"},
            callback=self.after_response
        )

    async def after_response(self, response):
        # Извлекаем ссылки на страницы, исключая ссылку "Next"
        for pages_link in response.xpath(
                '//section/div/div[5]/div[1]/ul/li/a[not(@aria-label="Next")]/@href').extract():
            # Отправляем запрос на каждую страницу и передаем управление в метод parse_page
            yield scrapy.Request(urljoin(response.url, pages_link), callback=self.parse_page)

    async def parse_page(self, response):
        # Извлекаем данные из таблицы
        table_rows = response.xpath('//table/tr')
        headers = [value.strip() for value in table_rows[0].xpath('./th//text()').extract()]
        for row in table_rows[1:]:
            data = [value.strip() for value in row.xpath('./td//text()').extract()]
            # Выводим данные в формате словаря
            yield dict(zip(headers, data))
