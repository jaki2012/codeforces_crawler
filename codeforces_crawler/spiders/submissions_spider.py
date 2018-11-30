import scrapy
import json
import re
import time
from scrapy.spidermiddlewares.httperror import HttpError
from codeforces_crawler.items import CodeforcesSubmissionItem

class SubmissionsSpider(scrapy.Spider):
    name = "cf_submission"
    # pythonify naming styles
    wanted_languages = ['Java 8', 'Python 3'] # 'GNU C++11', 'Java 7', 'Java 6', 'Python 2'
    wanted_verdicts = ['RUNTIME_ERROR', 'OK'] # 
    round_id_pattern = re.compile(r'''/(\d+)/''')

    # TODO: customize parameters like wanted_languages, problem_urls, etc.
    # def __init__(self, *args, **kwargs):
    #     super(SubmissionsSpider, self).__init__(*args, **kwargs)

    def __init__(self):
        self.csrf_token = "74b7483cfd78e25b10b2fd80b18e2d34"
        self.cookie = "JSESSIONID=84161C8132F49575182A59A1BBFF0BD2-n1; 39ce7=CFPIQlgp"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        self.headers = {
            "X-Csrf-Token": self.csrf_token,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": self.user_agent,
            "Cookie": self.cookie
        }

    def start_requests(self):

        # self.handles_num = 0
        urls = [
            'https://codeforces.com/problemset/status/141/problem/A/page/523?order=BY_ARRIVED_DESC',
            'https://codeforces.com/problemset/status/492/problem/B/page/788?order=BY_ARRIVED_DESC',
            'https://codeforces.com/problemset/status/446/problem/A/page/577?order=BY_ARRIVED_DESC'
            # 'https://codeforces.com/problemset/status/276/problem/C',
            # 'https://codeforces.com/problemset/status/141/problem/A',
            # 'https://codeforces.com/problemset/status/492/problem/B',
            # 'https://codeforces.com/problemset/status/721/problem/B',
            # 'https://codeforces.com/problemset/status/446/problem/A',
            # 'https://codeforces.com/problemset/status/522/problem/A',
            # 'https://codeforces.com/problemset/status/986/problem/A',
            # 'https://codeforces.com/problemset/status/605/problem/B',
            # 'https://codeforces.com/problemset/status/886/problem/C',
            # 'https://codeforces.com/problemset/status/913/problem/B',
            # 'https://codeforces.com/problemset/status/1056/problem/D',
            # 'https://codeforces.com/problemset/status/567/problem/C',
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies={'JSESSIONID':'84161C8132F49575182A59A1BBFF0BD2-n1','39ce7':'CFPIQlgp'}, callback=self.parse)

    def parse(self, response):
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
            # print(submission_verdict)
            time.sleep(0.1)
            # request for the code of this solution
            yield scrapy.FormRequest.from_response(response, url='http://codeforces.com/data/submitSource',
                                                    formdata={
                                                        'submissionId': submission_id,
                                                        'csrf_token': self.csrf_token
                                                    },
                                                    headers = self.headers,
                                                    meta={
                                                        'dont_merge_cookies': True,
                                                        'round_id': self.round_id_pattern.search(response.url).group(1),
                                                        'submission_lang': submission_lang,
                                                        'submission_id': submission_id,
                                                        'submission_verdict': submission_verdict
                                                    },
                                                    callback=self.parse_submission,
                                                    errback=self.print_errlog)
        # generate next-page url
        if response.selector.xpath('//span[@class="inactive"]/text()').extract():
            # '\u2192' is the unicode of 'right arrow' symbol
            if response.selector.xpath('//span[@class="inactive"]/text()')[0].extract() != u'\u2192':
                next_page_href = response.selector.xpath(
                    '//div[@class="pagination"]/ul/li/a[@class="arrow"]/@href')[0]
                next_page_url = response.urljoin(next_page_href.extract())
                yield scrapy.Request(next_page_url, headers=self.headers, callback=self.parse)
        else:
            next_page_href = response.selector.xpath(
                '//div[@class="pagination"]/ul/li/a[@class="arrow"]/@href')[1]
            next_page_url = response.urljoin(next_page_href.extract())
            yield scrapy.Request(next_page_url, headers=self.headers, callback=self.parse)


    def print_errlog(self, failure):
        self.logger.error(repr(failure))

        err_request = failure.value.response.request
        print(err_request.headers)

    def parse_submission(self, response):
        try:
            response_json = json.loads(response.body)
            
            item = CodeforcesSubmissionItem()
            
            outputs = { }
            for key in response_json: 
                if "output" in key:
                    outputs[key] = response_json[key]
            
            item['submission_id'] = response.meta['submission_id']
            item['verdict'] = response.meta['submission_verdict']
            item['round_id'] = response.meta['round_id']
            item['problem_name'] = response_json['problemName']
            item['source_code'] = response_json['source']
            item['outputs'] = outputs
            item['language'] = response.meta['submission_lang']
            
            yield item
        except Exception as e:
            # print (response.meta['submission_id'])
            print(e)
            return
