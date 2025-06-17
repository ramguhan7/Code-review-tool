import re

def check_uppercase_keywords(sql):
    keywords = re.findall(r'\b(select|from|where|join|as|on|and|or)\b', sql)
    return [f"Keyword '{kw}' should be uppercase." for kw in keywords]

def check_select_star(sql):
    return ["Avoid using SELECT *"] if re.search(r'\bSELECT\s+\*\b', sql, re.IGNORECASE) else []
