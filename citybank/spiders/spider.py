import scrapy

from scrapy.loader import ItemLoader

from ..items import CitybankItem
from itemloaders.processors import TakeFirst


class CitybankSpider(scrapy.Spider):
	name = 'citybank'
	start_urls = ['https://www.city.bank/about-us/news']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="sfpostsList sfpostListTitleDateSummary"]/li')
		for post in post_links:
			title = post.xpath('.//h2/a/text()').get()
			description = post.xpath('.//p//text()[normalize-space()]').getall()
			description = [p.strip() for p in description]
			description = ' '.join(description).strip()
			date = post.xpath('.//div[@class="sfpostAuthorAndDate"]/text()').get()

			item = ItemLoader(item=CitybankItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()

		next_page = response.xpath('//ul[@class="blog-archives"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)
