# Scraping

## Libraries
DataMade prefers that web scrapers use the [`scrapy` framework](https://scrapy.org/). Here's what we appreciate about scrapy:

1. Fast. `scrapy` wants to fetch data in parallel, and so it can pull a lot of data very quickly.
2. Opinionated. `scrapy` scrapers expect files to be organized in particular ways. This is good for reviewing PRs.
3. Popular. `scrapy` is the most popular scraping framework, so you can find lots of QAs and extensions on the internet.
4. Extensible. If you need a scrapy that can run some javascript, you can stay within the `scrapy` framework and use middleware like [`scrapy-playwright`](https://github.com/scrapy-plugins/scrapy-playwright). If you need IP rotation or more advanced anti-bot circumventions, there is a good migration path from a normal scrapy script to [Zyte](https://scrapy-zyte-api.readthedocs.io/en/latest/).

There are downside to `scrapy`. 

1. Callback-heck. If you need to traverse a number of pages in order to get the final pages to scrape, `scrapy`'s callback-based requests dispatching can hard to trace. An example of this type of traversal is if you need to visit a search page in order to get some cookies, then post to search page, then visit the search results. `scrapy` is [getting support for async/await syntax](https://docs.scrapy.org/en/latest/topics/coroutines.html), so this may be nicer in the future.
2. Tolerant error handling. With most of the serial, `requests`-based scrapers DataMade has written, if there is an exception, everything comes to a grinding halt and the process exits with a non-zero exit code. This is sometimes annoying, but makes it quite clear that something has gone wrong and it is easy to incorporate into longer data pipelines that should continue or not based upon exit codes (Makefiles, github actions are two examples). `scrapy` has another different philosophy, and every request you make could fail and the process would still exit successfully. If you only want to scrape without errors, then you need to affirmatively change a setting to exit on the first error, and [you need to do something like this](https://github.com/scrapy/scrapy/issues/1231#issuecomment-102409470) to change the exit code if there is an error.
3. Cache eviction. If you used `scrapy`'s caching mechanism, and you want to remove a small number of cached responses, it's pretty tricky to do the surgery to find the files and remove them.

We can put together a cookie cutter to help address some of those downsides.

## Scraping philosophy
DataMade generally prefers that scrapers be only responsible for the Extraction of the Extract, Transform, Load path. Generally, your scraper should emit `json` representations of just the information you need from the website in a form that is substantially similar to how it is represented on the website. We usually like the final output for the scraper to be new-line delimited `json` we can then hand off to other tools to transform.
