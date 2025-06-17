import os
from sql_review_tool.rules.formatting_rules import *


def review_file(file_path):
    with open(file_path, 'r') as f:
        sql = f.read()
    issues = []
    issues += check_uppercase_keywords(sql)
    issues += check_select_star(sql)
    issues += check_alias_with_as(sql)
    issues += check_non_ansi_joins(sql)
    issues += check_column_formatting(sql)
    issues += check_no_isnull(sql)
    issues += check_string_constants(sql)
    issues += check_missing_table_alias(sql)
    issues += check_columns_use_alias(sql)
    issues += check_column_alias_suffix(sql)
    issues += check_line_comment_usage(sql)
    issues += check_hardcoded_database_names(sql)
    issues += check_missing_alias_suffix(sql)



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
