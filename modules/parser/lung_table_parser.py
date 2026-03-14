import pdfplumber
import re


def clean_value(value):

    try:
        value = str(value).replace("%", "").strip()
        return float(value)

    except:
        return None


def parse_table(pdf_file):

    data = {

        "fev1_percent": None,
        "mef25": None,
        "mef50": None,
        "mef75": None,

        "fef25": None,
        "fef50": None,
        "fef75": None,

        "pef": None
    }

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:

                for row in table:

                    row_text = " ".join([str(x) for x in row if x])

                    if re.search(r"FEV1", row_text, re.I):

                        data["fev1_percent"] = clean_value(row[-1])

                    if re.search(r"MEF\s*25", row_text, re.I):

                        data["mef25"] = clean_value(row[-1])

                    if re.search(r"MEF\s*50", row_text, re.I):

                        data["mef50"] = clean_value(row[-1])

                    if re.search(r"MEF\s*75", row_text, re.I):

                        data["mef75"] = clean_value(row[-1])

                    if re.search(r"FEF\s*25", row_text, re.I):

                        data["fef25"] = clean_value(row[-1])

                    if re.search(r"FEF\s*50", row_text, re.I):

                        data["fef50"] = clean_value(row[-1])

                    if re.search(r"FEF\s*75", row_text, re.I):

                        data["fef75"] = clean_value(row[-1])

                    if re.search(r"PEF", row_text, re.I):

                        data["pef"] = clean_value(row[-1])

    return data
