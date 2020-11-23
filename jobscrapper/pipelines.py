# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter

from jobscrapper.items import JobOpeningItem


class JobOpeningsPipeline:
    def _clean(self, value):
        if value:
            return ' '.join(value.split())

        return value

    def process_item(self, item, spider):
        item = JobOpeningItem(item)
        for field in ('title', 'location', 'department'):
            item[field] = self._clean(item[field])
        return item


class PerCompanyExportPipeline:
    """Distribute items across multiple XML files according to their 'year' field"""

    def __init__(self, path=None):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('JOBS_PATH', '.'))

    def open_spider(self, spider):
        self.company_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.company_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        company = adapter['company']
        if company not in self.company_to_exporter:
            f = open(os.path.join(self.path, f'{company}.json'), 'wb')
            exporter = JsonItemExporter(f, indent=4)
            exporter.start_exporting()
            self.company_to_exporter[company] = exporter
        return self.company_to_exporter[company]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
