import re

def extract_value(pattern, text):

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        try:
            return float(match.group(1))
        except:
            return None

    return None


def parse_chinese_lung_function(text):

    data = {}

    # FEV1
    data["fev1_percent"] = extract_value(
        r"FEV1[^%0-9]*([0-9]+\.?[0-9]*)\s*%pred", text
    )

    if data["fev1_percent"] is None:
        data["fev1_percent"] = extract_value(
            r"FEV1[^0-9]*([0-9]+\.?[0-9]*)", text
        )

    # PEF
    data["pef"] = extract_value(
        r"PEF[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    # MEF
    data["mef25"] = extract_value(
        r"MEF\s*25[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    data["mef50"] = extract_value(
        r"MEF\s*50[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    data["mef75"] = extract_value(
        r"MEF\s*75[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    # FEF
    data["fef25"] = extract_value(
        r"FEF\s*25[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    data["fef50"] = extract_value(
        r"FEF\s*50[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    data["fef75"] = extract_value(
        r"FEF\s*75[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    # FEV1/FVC
    data["fev1_fvc"] = extract_value(
        r"FEV1/FVC[^0-9]*([0-9]+\.?[0-9]*)", text
    )

    return data
