import re

# ✅ Rule 1: UPPERCASE SQL keywords
def check_uppercase_keywords(sql):
    # Remove inline (--) and block (/* */) comments before checking
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    sql = re.sub(r'--.*', '', sql)

    keywords = re.findall(r'\b('
        r'select|from|where|join|inner join|left join|right join|full join|on|and|or|'
        r'insert|into|values|update|set|delete|create|alter|drop|truncate|'
        r'distinct|group by|order by|having|limit|offset|'
        r'union|union all|intersect|except|exists|not|in|is null|is not null|'
        r'like|between|case|when|then|else|end|as|'
        r'cast|try_cast|coalesce|nullif|if|with|top|over|partition by|'
        r'rank|dense_rank|row_number|'
        r'dateadd|datediff|current_date|current_timestamp|now|year|month|day|'
        r'weekofyear|dayofweek|'
        r'cache|uncache|refresh|optimize|zorder|using|options|tablesample|'
        r'merge|when matched|when not matched|copy into|autoloader|streaming|'
        r'watermark|trigger|output mode|struct|array|map|explode|posexplode|'
        r'lateral view|input_file_name|monotonically_increasing_id|'
        r'to_date|to_timestamp|date_trunc|date_format|lag|lead|ntile|first|last|'
        r'greatest|least|size|element_at|get_json_object'
        r')\b', sql, flags=re.IGNORECASE)

    return [f"Keyword '{kw}' should be uppercase." for kw in keywords if kw != kw.upper()]


# ✅ Rule 2: Avoid SELECT *
def check_select_star(sql):
    return ["Avoid using SELECT *"] if re.search(r'\bSELECT\s+\*\b', sql, re.IGNORECASE) else []

# ✅ Rule 3: Use AS for aliasing
def check_alias_with_as(sql):
    select_block = re.search(r'\bSELECT\s+(.*?)\bFROM\b', sql, re.IGNORECASE | re.DOTALL)
    if not select_block:
        return []
    columns = select_block.group(1).split(',')
    violations = []
    for col in columns:
        if re.search(r'\s+\w+$', col) and ' AS ' not in col.upper():
            violations.append(f"Column alias should use 'AS': `{col.strip()}`")
    return violations

# ✅ Rule 4: Avoid non-ANSI joins (*= or =*)
def check_non_ansi_joins(sql):
    if '*=' in sql or '=*' in sql:
        return ["Avoid non-ANSI join syntax (*= or =*)"]
    return []

# ✅ Rule 5: Preceding comma formatting
def check_column_formatting(sql):
    issues = []

    # Extract the SELECT block only (between SELECT and FROM)
    select_match = re.search(r'\bSELECT\b\s+(.*?)\bFROM\b', sql, re.IGNORECASE | re.DOTALL)
    if not select_match:
        return issues

    select_block = select_match.group(1)
    lines = [line.strip() for line in select_block.strip().splitlines() if line.strip()]

    for i, line in enumerate(lines):
        if i == 0:
            continue  # Skip first line after SELECT
        if not line.startswith(',') and not line.startswith('--'):
            issues.append(f"Column line should begin with a comma: `{line}`")

    return issues


# ✅ Rule 6: No ISNULL()
def check_no_isnull(sql):
    return ["Use COALESCE() instead of ISNULL()"] if re.search(r'\bISNULL\s*\(', sql, re.IGNORECASE) else []

# ✅ Rule 7: Use single quotes for string constants
def check_string_constants(sql):
    issues = []
    double_quotes = re.findall(r'"([^"]*?\d+[^"]*?)"', sql)
    for match in double_quotes:
        issues.append(f"Use single quotes instead of double quotes for: \"{match}\"")
    return issues

# ✅ Rule 8: Require table aliases in FROM
def check_missing_table_alias(sql):
    issues = []
    pattern = re.compile(r'FROM\s+([a-zA-Z_][\w\.]*)\s*(?:,|\n|$)', re.IGNORECASE)
    for match in pattern.findall(sql):
        if not re.search(rf'\b{re.escape(match)}\s+[a-zA-Z_]\w*', sql):
            issues.append(f"Table `{match}` is missing an alias.")
    return issues

# ✅ Rule 9: Column must be prefixed with table alias
def check_columns_use_alias(sql):
    issues = []
    select_block = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
    if select_block:
        columns = [c.strip() for c in select_block.group(1).split(',')]
        for col in columns:
            if col and not col.lower().startswith('--') and '.' not in col and ' as ' not in col.lower():
                issues.append(f"Column `{col}` is not qualified with a table alias.")
    return issues

# ✅ Rule 10: Column alias must end in UPPERCASE suffix
def check_column_alias_suffix(sql):
    issues = []
    suffixes = ['ID', 'NM', 'CD', 'CNT', 'DSC', 'FLG', 'AMT', 'PCT', 'DTS', 'NBR', 'TXT','SEQ']

    # Extract SELECT block only
    select_match = re.search(r'\bSELECT\b\s+(.*?)\bFROM\b', sql, re.IGNORECASE | re.DOTALL)
    if not select_match:
        return issues

    select_block = select_match.group(1)
    columns = re.split(r',(?![^\(\)]*\))', select_block)

    for col in columns:
        col = col.strip()
        match = re.search(r'\bAS\s+([a-zA-Z_][a-zA-Z0-9_]*)$', col, re.IGNORECASE)
        if match:
            alias = match.group(1)
            if not any(alias.upper().endswith(suffix) for suffix in suffixes):
                issues.append(
                    f"Alias `{alias}` does not end with an approved suffix ({', '.join(suffixes)})"
                )

    return issues


# ✅ Rule 11: Enforce block comments
def check_line_comment_usage(sql):
    issues = []
    lines = sql.splitlines()
    for i, line in enumerate(lines, start=1):
        if '--' in line and not line.strip().startswith('--'):
            issues.append(f"Line {i}: Use block comments (/* */) instead of inline '--': `{line.strip()}`")
    return issues

# ✅ Rule 12: Enforce parameterization
def check_hardcoded_database_names(sql):
    issues = []
    # Define hardcoded database prefixes
    banned_dbs = {
        'shca_source_data': '{{source_data}}',
        'shca_data_marts_dev': '{{data_marts}}',
        'shca_data_marts_test': '{{data_marts}}',
        'shca_data_marts': '{{data_marts}}'
    }

    for db, expected in banned_dbs.items():
        pattern = re.compile(rf'\b{re.escape(db)}\.', re.IGNORECASE)
        matches = pattern.findall(sql)
        for _ in matches:
            issues.append(
                f"Hardcoded DB `{db}` detected. Use `{expected}` instead."
            )

    return issues

# ✅ Rule 13: Alias suffixes check
def check_missing_alias_suffix(sql):
    issues = []
    approved_suffixes = ['ID', 'NM', 'CD', 'CNT', 'DSC', 'FLG', 'AMT', 'PCT', 'DTS', 'NBR', 'TXT', 'SEQ']

    select_match = re.search(r'\bSELECT\b\s+(.*?)\bFROM\b', sql, re.IGNORECASE | re.DOTALL)
    if not select_match:
        return issues

    select_block = select_match.group(1)
    columns = re.split(r',(?![^\(\)]*\))', select_block)

    for col in columns:
        col = col.strip()
        # Check if there's an AS alias
        match = re.search(r'\bAS\s+([a-zA-Z_][a-zA-Z0-9_]*)$', col, re.IGNORECASE)
        if match:
            alias = match.group(1)
            if not any(alias.upper().endswith(suffix) for suffix in approved_suffixes):
                issues.append(
                    f"Alias `{alias}` does not end with an approved suffix ({', '.join(approved_suffixes)})"
                )
        else:
            issues.append(f"Column `{col}` is missing an alias with an approved suffix.")

    return issues

# ✅ Rule 14: Title comment block 
def check_title_comment_block(sql, file_path=None):
    """
    Checks whether the SQL file begins with the expected standard title comment block.
    """
    issues = []

    # Get the top portion of the SQL
    top_lines = '\n'.join(sql.strip().splitlines()[:20])

    # Check that the block starts and ends correctly
    if not top_lines.startswith("/**") or "Entity Name:" not in top_lines or "Author:" not in top_lines or "Description:" not in top_lines or "Change Log:" not in top_lines or not top_lines.strip().endswith("*/"):
        issues.append(
            "Missing or improperly formatted title comment block. Expected block with Entity Name, Author, Description, and Change Log."
        )

    return issues
