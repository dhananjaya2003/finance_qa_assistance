import pdfplumber
import pandas as pd
from io import BytesIO
import tempfile
import camelot
import re

def _clean_text(t):
    return re.sub(r"\s+"," ", t).strip()


def extract_from_pdf(file_obj):
    raw_text = []
    tables = []
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_text.append(text)
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        tmp.write(file_obj.getvalue())
        tmp.close()
        tables_found = camelot.read_pdf(tmp.name, pages='all', flavor='stream')
        for t in tables_found:
            df = t.df.replace('', pd.NA).dropna(how='all')
            tables.append(df)
    except Exception:
        pass
    return (_clean_text("\n".join(raw_text)), tables)


def extract_from_excel(file_obj):
    xls = pd.ExcelFile(BytesIO(file_obj.getvalue()))
    tables = []
    text_parts = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        tables.append(df)
        text_parts.append(f"Sheet: {sheet}\n"+df.head(50).to_csv(index=False))
    return ("\n".join(text_parts), tables)