# codeforces_crawler

A scrapy-based crawler for source code of all submissions on www.codeforces.com

# Basic Usage:
### Step 1 - install all the required dependencies
```
    pip install -r requirements.txt
```

### Step 2 - configure your customized settings, 
e.g., to configure the settings of MongoDB in which the scraped items will be stored
```
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27016
MONGO_DB = 'codeforces_crawler'
MONGO_COLLECTION = 'submissions'
MONGO_USER = 'your_username'
MONGO_PASSWORD = 'your_password'
```

### Step 3 - start crawling
```
scrapy crawl cf_submission
```
or more robustly,
```
scrapy crawl cf_submission -s JOBDIR=crawls/cf_submission-0001
```
then you are able to restore this crawler with the same command, whenever the crawling process is interrupted.