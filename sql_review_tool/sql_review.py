from rules.formatting_rules import *

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
    # 🔽 New Rules
    issues += check_missing_table_alias(sql)
    issues += check_columns_use_alias(sql)
    issues += check_column_alias_suffix(sql)
    return issues
