import scrapy
import scrapy.http

from urllib.parse import urljoin

from jobscrapper.items import JobOpeningItem

WORKABLE_API_URL = 'https://careers-page.workable.com'
WORKABLE_ACCOUNTS_API_URL = urljoin(WORKABLE_API_URL, 'api/v3/accounts')
WORKABLE_JOB_API_URL = urljoin(WORKABLE_API_URL, 'api/v2/accounts')


class WorkableSpider(scrapy.Spider):
    name = "workable"
    start_urls = [
        'https://apply.workable.com/lensesio/',
        'https://apply.workable.com/blueground/',
        'https://apply.workable.com/e-food/',
        'https://apply.workable.com/skroutz/',
        'https://apply.workable.com/orfium/',
    ]

    def start_requests(self):
        for url in self.start_urls:
            company = url.split('/')[-2]
            yield scrapy.Request(url=f'{WORKABLE_ACCOUNTS_API_URL}/{company}/jobs',
                                 meta={'base_url': url},
                                 method='POST',
                                 callback=self.parse)

    def parse(self, response):
        company = response.url.split("/")[-2]
        data = response.json()
        for job in data.get('results', []):
            yield scrapy.Request(url=f'{WORKABLE_JOB_API_URL}/{company}/jobs/{job["shortcode"]}',
                                 meta={
                                     **job,
                                     **response.meta,
                                     'company': company
                                 },
                                 callback=self.parse_job)

        # Handle paging
        if 'nextPage' in data:
            yield scrapy.http.JsonRequest(url=f'{WORKABLE_ACCOUNTS_API_URL}/{company}/jobs',
                                          meta=response.meta,
                                          data={"token": data['nextPage'], "query": "", "location": [],
                                                "department": [],
                                                "worktype": [], "remote": []},
                                          callback=self.parse)

    def parse_job(self, response):
        job = response.json()
        yield JobOpeningItem(
            id=job.get('id'),
            title=job.get('title'),
            company=response.meta['company'],
            department=job.get('department')[0] if job.get('department') else '',
            location=job.get('location', {}).get('city'),
            description=job.get('description'),
            requirements=job.get('requirements'),
            link=urljoin(response.meta['base_url'], f'j/{response.meta["shortcode"]}')
        )
