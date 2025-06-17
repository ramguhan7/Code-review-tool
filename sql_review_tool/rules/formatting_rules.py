import re

# Rule: Table alias is required for FROM/JOIN clauses
def check_missing_table_alias(sql):
    issues = []
    pattern = re.compile(r'FROM\s+([a-zA-Z_][\w\.]*)\s*(?:,|\n|$)', re.IGNORECASE)
    for match in pattern.findall(sql):
        if not re.search(rf'\b{re.escape(match)}\s+[a-zA-Z_]\w*', sql):
            issues.append(f"Table `{match}` is missing an alias.")
    return issues

# Rule: Column references should be qualified with alias (e.g., o.column)
def check_columns_use_alias(sql):
    issues = []
    # Simplified assumption: If SELECT has bare column names without ".", flag them
    select_block = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
    if select_block:
        columns = [c.strip() for c in select_block.group(1).split(',')]
        for col in columns:
            if col and not col.lower().startswith('--') and '.' not in col and ' as ' not in col.lower():
                issues.append(f"Column `{col}` is not qualified with a table alias.")
    return issues

# Rule: Column alias must end in uppercase suffix (e.g., _ID, _CD, _CNT, _DSC)
def check_column_alias_suffix(sql):
    issues = []
    matches = re.findall(r'\s+AS\s+([a-zA-Z_]\w+)', sql, re.IGNORECASE)
    for alias in matches:
        if not re.search(r'(_ID|_CD|_CNT|_DSC|_FLG|_AMT|_PCT|_DTS)$', alias):
            issues.append(f"Alias `{alias}` does not use an approved uppercase suffix (_ID, _CD, etc.)")
    return issues
