import scrapelib
import lxml

class Scraper(scrapelib.Scraper):
    '''Rename me to something more descriptive'''

    def _spider(self):
        '''yield lxml.html pages'''
        ...
        

    def scrape(self):
        '''yield dictionaries of data'''
        for page in self._spider():
            ...


if __name__ == '__main__':
    import argparse
    import pathlib
    import json

    parser = argparse.ArgumentParser(description='Scrape your site')
    parser.add_argument('output_dir',  type=pathlib.Path)

    args = parser.parse_args()

    scraper = Scraper()

    for result in scraper:
        result_id = result['id']
        file_name = f'{result_id}.json'
        file_path = args.output_dir / file_name
        with file_path.open() as f:
            json.dump(f, result)
        

        
        
