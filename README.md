# Openings

Experimenting with scraping job openings from the web.

# Prerequisites

- Python 3.6+ (was developed using python 3.8)
- pip/virtualenv installed

# Installing

Create a virtualenv and install requirements. You can do this by running

```bash
virtualenv env
. env/bin/activate
pip install -r requirements
```

# Running spiders

There are two spiders that you can use for now, one for Workable-backed career pages and one for Recruitee.

To run Workable-based crawler, edit openings/spiders/workable.py run: 
```bash
scrapy runspider jobscrapper/spiders/workable.py
```

Similarly for recruitee just run:
```bash
scrapy runspider jobscrapper/spiders/recruitee.py
```

All jobs will be stored under `data/`, on a separate file per company.