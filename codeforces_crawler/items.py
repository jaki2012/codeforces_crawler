# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CodeforcesSubmissionItem(scrapy.Item):
    # submissionID 
    submission_id = scrapy.Field()
    # judge status of this submission
    verdict = scrapy.Field()
    round_id = scrapy.Field()
    problem_name = scrapy.Field()
    # the content of the source code
    source_code = scrapy.Field()
    # the programming language of this solution
    language = scrapy.Field()