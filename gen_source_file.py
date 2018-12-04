# -*- coding:UTF-8 -*-
from ast import literal_eval
import os
import sys

def create_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)


EXTENTIONS_DICT = {
    'GNU C'        : 'c'       ,
    'GNU C11'      : 'c'       ,
    'GNU C++'      : 'cc'      ,
    'GNU C++11'    : 'cc'      ,
    'GNU C++0x'    : 'cc'      ,
    'MS C++'       : 'cpp'     ,
    'FPC'          : 'pp'      ,
    'Delphi'       : 'pas'     ,
    'Haskell'      : 'hs'      ,
    'Java 8'       : 'java'    ,
    'Java 7'       : 'java'    ,
    'Java 6'       : 'java'    ,
    'Python 3'     : 'py'      ,
    'Python 2'     : 'py'      ,

    # adation to lyoi_crawler
    'C'            : 'c'       ,
    'C++'          : 'cpp'     ,
    'C++11'        : 'cpp'     
}

if len(sys.argv) < 3:
    print("Error, please check your parameters, and" + 
            "explicitly specify the corresponding paths")
    print("Usage: ")
    print("=======================")
    print("python gen_source_file.py <your_submissions_file> <output_dir_name>")
    print("e.g. python gen_source_file.py submissions-20181130.json source code")


json_file_path = sys.argv[1]
output_dir_name = sys.argv[2]

with open(json_file_path, 'r') as f:
    submissions = literal_eval(f.read())

create_directory(output_dir_name)
# s means submission
for s in submissions:
    # the key content - source code
    source_code = s['source_code']
    # the programming language
    language = s['language']
    # extention name 
    ext = EXTENTIONS_DICT[language]

    # adpation to lyoi_crawler
    if 'round_id' not in s.keys():
        s['round_id'] = 'LYOI'

    # what if the problem name contains '/'
    # lyoi_#62. 「LYOI2016 Summer」A / B Problem_15154.cpp
    # if '/' in s['problem_name']:
    #     print('yes')
    #     print(s['problem_name'])

    # TODO: HANDLE UNICODE ENCODING IN SOURCEFILE
    s['problem_name'] = s['problem_name'].replace('/', 'divide')

    src_file_name = '{}_{}_{}.{}'.format(s['round_id'], s['problem_name'], s['submission_id'], ext)

    print("Generating: %s" % src_file_name)
        
    create_directory('./{}/{}/{}/{}'.format(output_dir_name, s['round_id'], s['problem_name'], s['language']))
    with open('./{}/{}/{}/{}/{}'.format(output_dir_name, s['round_id'], s['problem_name'], s['language'],
                                        src_file_name), 'w', encoding="utf-8") as output:
        output.write(source_code)