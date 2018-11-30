# CodeForces-Crawler 
[![Build Status](https://travis-ci.org/jaki2012/codeforces_crawler.svg?branch=master)](https://travis-ci.org/jaki2012/codeforces_crawler)


A scrapy-based crawler for all **submissions** (including source code) of any specific problems on www.codeforces.com.

Since the [provided APIs](https://codeforces.com/api/help/objects) of CodeForces is not so strong as Github, I endeavored to process the front-end requests within Codeforces websites. Now the crawler is not limited to API restrictions.  

**Prerequisites**:  
- [Python 3 or above](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-by-codebabes.svg)](https://forthebadge.com)

# Usage:
### Step 0 - Set up the virtual enviroment (Optional)
This is an optional (but really **recommended**) step.
```
pip3 install virtualenv

cd your_workspace # 

virtualenv --no-site-packages venv # create an independent, clean enviroment

source venv/bin/activate # activate the enviroment
```
For more info about *virtualenv*, visit https://virtualenv.pypa.io/en/latest/

### Step 1 - Install all the required dependencies
```
    pip3 install -r requirements.txt
```

### Step 2 - Configure your customized settings 
e.g., to configure the settings of MongoDB in which the scraped items will be stored
```
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27016
MONGO_DB = 'codeforces_crawler'
MONGO_COLLECTION = 'submissions'
MONGO_USER = 'your_username'
MONGO_PASSWORD = 'your_password'
```

### Step 3 - Start crawling
```
scrapy crawl cf_submission
```
or more robustly,
```
scrapy crawl cf_submission -s JOBDIR=crawls/cf_submission-0001
```
then you are able to restore this crawler with the **same command**, whenever the crawling process is interrupted.


# About the scraped item - *Submission*
An scraped entity represents a submission with the structure below:

| Key           | Required     | Type   | Description                                                                                                                    |
| ------------- | ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| submission_id | yes          | String | the ID of this submission                                                                                                      |
| verdict       | yes          | String | the status of this submission (e.g., "OK","RUNTIME_ERROR")                                                                                                  |
| round_id      | yes          | String | the round number of the problem                                                                                                |
| problem_name  | yes          | String | the name of the problem                                                                                                        |
| problem_url   | no, optional | String | the link url of the problem (yet not crawled)                                                                                       |
| source_code   | yes          | String | critical, the stringify content of the source code                                                                             |
| outputs       | yes          | Object | record all the outputs came with this submission (for "RUNTIME_ERROR" submission, the **last output** record the **stack information**) |
| language      | yes          | String | the programming language of the source code (e.g., "GNU C++11")   |
 
We also provide two examples:

query by `db.getCollection('submissions').find({"verdict":"OK", "language": "Python 3"})`
```
{
    "_id" : ObjectId("5c002203970c2930e28adb13"),
    "submission_id" : "44930215",
    "problem_name" : "(C) Geometric Progression",
    "language" : "Java 8",
    "round_id" : "567",
    "outputs" : {
        "output#2" : "1\r\n",
        "output#3" : "6\r\n",
        "output#1" : "4\r\n",
        "output#6" : "5\r\n",
        "output#7" : "1333313333400000\r\n",
        "output#4" : "5\r\n",
        "output#5" : "3\r\n",
        "output#8" : "java.lang.NullPointerException\r\n\tat B.main(B.java:24)\r\n"
    },
    "verdict" : "RUNTIME_ERROR",
    "source_code" : "import java.util.HashMap;\r\nimport java.util.Map;\r\nimport java.util.Scanner;\r\n\r\npublic class B {\r\n\r\n\tpublic static Scanner scanner = new Scanner(System.in);\r\n\tprivate static int n, k;\r\n\tprivate static long res = 0;\r\n\tprivate static long[] sol = new long[300010];\r\n\tprivate static Map<Long, Integer> right = new HashMap<>();\r\n\tprivate static Map<Long, Integer> left = new HashMap<>();\r\n\r\n\tpublic static void main(String[] args) {\r\n\t\tn = scanner.nextInt();\r\n\t\tk = scanner.nextInt();\r\n\r\n\t\tfor(long i=0;i<300010;i++) {\r\n\t\t\tright.put(i, 0);\r\n\t\t\tleft.put(i, 0);\r\n\t\t}\r\n\t\tfor (int i = 0; i < n; i++) {\r\n\t\t\tsol[i] = scanner.nextInt();\r\n\t\t\tright.put(sol[i], right.get(sol[i])+1);\r\n\t\t}\r\n\r\n\t\tfor (int i = 0; i < n; i++) {\r\n\t\t\tlong k1 = 0, k2;\r\n\r\n\t\t\tif (sol[i] % k == 0) k1 = left.get(sol[i] / k);\r\n\t\t\tright.put(sol[i], right.get(sol[i]) - 1);\r\n\r\n\t\t\tk2 = right.get(sol[i] * k);\r\n\r\n\t\t\tres += k1 * k2;\r\n\r\n\t\t\tleft.put(sol[i], left.get(sol[i]) + 1);\r\n\t\t}\r\n\r\n\t\tSystem.out.println(res);\r\n\t}\r\n}\r\n"
}

{
    "_id" : ObjectId("5c002161970c2930e28adb01"),
    "submission_id" : "46344244",
    "problem_name" : "(A) Amusing Joke",
    "language" : "Python 3",
    "round_id" : "141",
    "outputs" : {
        "output#21" : "NO\r\n",
        "output#20" : "NO\r\n",
        "output#23" : "NO\r\n",
        "output#22" : "NO\r\n",
        "output#25" : "NO\r\n",
        "output#24" : "NO\r\n",
        "output#27" : "NO\r\n",
        "output#26" : "NO\r\n",
        "output#29" : "NO\r\n",
        "output#28" : "NO\r\n",
        "output#54" : "NO\r\n",
        "output#18" : "NO\r\n",
        "output#19" : "NO\r\n",
        "output#50" : "NO\r\n",
        "output#51" : "NO\r\n",
        "output#52" : "NO\r\n",
        "output#53" : "NO\r\n",
        "output#10" : "NO\r\n",
        "output#11" : "NO\r\n",
        "output#12" : "YES\r\n",
        "output#13" : "YES\r\n",
        "output#14" : "YES\r\n",
        "output#15" : "YES\r\n",
        "output#16" : "YES\r\n",
        "output#17" : "YES\r\n",
        "output#32" : "YES\r\n",
        "output#33" : "YES\r\n",
        "output#30" : "NO\r\n",
        "output#31" : "NO\r\n",
        "output#36" : "YES\r\n",
        "output#37" : "YES\r\n",
        "output#34" : "YES\r\n",
        "output#35" : "YES\r\n",
        "output#38" : "YES\r\n",
        "output#39" : "YES\r\n",
        "output#2" : "NO\r\n",
        "output#3" : "NO\r\n",
        "output#1" : "YES\r\n",
        "output#6" : "YES\r\n",
        "output#7" : "YES\r\n",
        "output#4" : "YES\r\n",
        "output#5" : "YES\r\n",
        "output#8" : "YES\r\n",
        "output#9" : "NO\r\n",
        "output#43" : "NO\r\n",
        "output#42" : "NO\r\n",
        "output#41" : "YES\r\n",
        "output#40" : "YES\r\n",
        "output#47" : "NO\r\n",
        "output#46" : "NO\r\n",
        "output#45" : "NO\r\n",
        "output#44" : "NO\r\n",
        "output#49" : "NO\r\n",
        "output#48" : "NO\r\n"
    },
    "verdict" : "OK",
    "source_code" : "a = input()\nb = input()\nc = input()\nd = ''\nfor i in a:\n    d = d + i\nfor q in b:\n    d = d + q\nc = list(c)\nc.sort()\nd = list(d)\nd.sort()\nif c == d:\n    print('YES')\nelse:\n    print('NO')"
}

```
