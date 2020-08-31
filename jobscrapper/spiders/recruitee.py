import scrapy

from jobscrapper.items import JobOpeningItem


class RecruiteeSpider(scrapy.Spider):
    name = "recruitee"
    start_urls = [
        'https://netdata.recruitee.com/',
        'https://ferryhopper.recruitee.com/',
    ]

    def parse(self, response):
        company = response.url[8:].split('.')[0]
        jobs = response.css('div.job')
        for job in jobs:
            yield scrapy.Request(url=response.urljoin(job.css('h5.job-title a::attr(href)')[0].extract()),
                                 meta={
                                     'id': job.css('div::attr(id)').extract()[0],
                                     'company': company,
                                     'department': job.css('div.department::text').get(),
                                     'location': job.css('li.job-location::text').get(),
                                 }, callback=self.parse_job)

    def parse_job(self, response):
        yield JobOpeningItem(
            id=response.meta['id'],
            title=response.css('h2.title::text').get(),
            company=response.meta['company'],
            department=response.meta['department'],
            location=response.meta['location'],
            description='\n'.join(response.xpath('//div[@class="description"]')[0].xpath('./*').getall()),
            requirements='\n'.join(response.xpath('//div[@class="description"]')[1].xpath('./*').getall()),
            link=response.url
        )
