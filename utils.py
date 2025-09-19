import re

def normalize_label(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+"," ", s).strip()
    return s