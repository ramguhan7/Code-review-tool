import os
from rules.formatting_rules import *

def review_file(file_path):
    with open(file_path, 'r') as f:
        sql = f.read()
    issues = []
    issues += check_uppercase_keywords(sql)
    issues += check_select_star(sql)
    return issues

def review_directory(directory):
    report = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.sql'):
                path = os.path.join(root, file)
                issues = review_file(path)
                if issues:
                    report[path] = issues
    return report
