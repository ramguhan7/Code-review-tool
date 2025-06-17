import re

# ✅ Rule 1: UPPERCASE SQL keywords
def check_uppercase_keywords(sql):
    keywords = re.findall(r'\b(select|from|where|join|as|on|and|or|insert|update|delete)\b', sql)
    return [f"Keyword '{kw}' should be uppercase." for kw in keywords]

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
    
    # Extract SELECT block only
    select_match = re.search(r'\bSELECT\b\s+(.*?)\bFROM\b', sql, re.IGNORECASE | re.DOTALL)
    if not select_match:
        return []

    select_block = select_match.group(1)

    # Split columns while ignoring commas inside parentheses (e.g., CAST(...))
    columns = re.split(r',(?![^\(]*\))', select_block)

    for col in columns:
        col = col.strip()
        alias_match = re.search(r'\bAS\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', col, re.IGNORECASE)
        if alias_match:
            alias = alias_match.group(1)
            if not re.search(r'(_ID|_CD|_CNT|_DSC|_FLG|_AMT|_PCT|_DTS|_NBR)$', alias):
                issues.append(f"Alias `{alias}` does not use an approved uppercase suffix (_ID, _CD, etc.)")

    return issues