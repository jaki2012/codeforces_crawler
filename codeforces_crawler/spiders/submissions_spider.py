import scrapy
import json
import re
import time

from codeforces_crawler.items import CodeforcesSubmissionItem

class SubmissionsSpider(scrapy.Spider):
    name = "cf_submission"
    # pythonify naming styles
    wanted_languages = ['Java 8', 'Python 3', 'Python 2'] # 'GNU C++11'
    wanted_verdicts = ['RUNTIME_ERROR', 'OK']

    round_id_pattern = re.compile(r'''/(\d+)/''')

    # TODO: customize parameters like wanted_languages, problem_urls, etc.
    # def __init__(self, *args, **kwargs):
    #     super(SubmissionsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            'https://codeforces.com/problemset/status/4/problem/C',
            'https://codeforces.com/problemset/status/37/problem/A',
            'https://codeforces.com/problemset/status/430/problem/B',
            'https://codeforces.com/problemset/status/489/problem/C',
            'https://codeforces.com/problemset/status/520/problem/B',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        # generate next-page url
        if response.selector.xpath('//span[@class="inactive"]/text()').extract():
            # '\u2192' is the unicode of 'right arrow' symbol
            if response.selector.xpath('//span[@class="inactive"]/text()')[0].extract() != u'\u2192':
                next_page_href = response.selector.xpath(
                    '//div[@class="pagination"]/ul/li/a[@class="arrow"]/@href')[0]
                next_page_url = response.urljoin(next_page_href.extract())
                yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            next_page_href = response.selector.xpath(
                '//div[@class="pagination"]/ul/li/a[@class="arrow"]/@href')[1]
            next_page_url = response.urljoin(next_page_href.extract())
            yield scrapy.Request(next_page_url, callback=self.parse)
        
        submission_id_list = response.xpath('//tr/@data-submission-id').extract()
        for submission_id in submission_id_list:
            submission_lang = response.xpath(
                '//tr[@data-submission-id=%s]/td[5]/text()' % submission_id)[0].extract().strip()
            # only scrape the submissions written with the specific languages
            if submission_lang not in self.wanted_languages:
                continue
            
            submission_verdict = response.xpath(
                '//tr[@data-submission-id=%s]/td[6]/span/@submissionverdict' % submission_id)[0].extract().strip()
            # only scrape the submissions written with the specific verdictstatuss
            if submission_verdict not in self.wanted_verdicts:
                continue
            
            time.sleep(0.1)
            # request for the code of this solution
            yield scrapy.FormRequest.from_response(response, url='http://codeforces.com/data/submitSource',
                                                    formdata={
                                                        'submissionId': submission_id
                                                    },
                                                    meta={
                                                        'round_id': self.round_id_pattern.search(response.url).group(1),
                                                        'submission_lang': submission_lang,
                                                        'submission_id': submission_id,
                                                        'submission_verdict': submission_verdict
                                                    },
                                                    callback=self.parse_submission)

    def parse_submission(self, response):
        response_json = json.loads(response.body)
        
        item = CodeforcesSubmissionItem()
        
        item['submission_id'] = response.meta['submission_id']
        item['verdict'] = response.meta['submission_verdict']
        item['round_id'] = response.meta['round_id']
        item['problem_name'] = response_json['problemName']
        item['source_code'] = response_json['source']
        item['language'] = response.meta['submission_lang']
        
        yield item
