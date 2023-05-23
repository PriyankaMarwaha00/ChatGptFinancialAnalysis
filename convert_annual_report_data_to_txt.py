# This program converts annal report data to txt file
# The annual reports are in pdf format present in the folder
# annual_report_data/GOOGL/yyyy-Annual_Report.pdf

import os
import re
import pdftotext
import json
# Define the tickers and date range
tickers = ['GOOGL', 'MSFT', 'AMZN', 'AAPL']

def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text

def pdf_to_text(path):
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
    text_list = []
    for page_text in pdf:
        page_text = preprocess(page_text)
        text_list.append(page_text)
    return text_list

def python_to_txt(pdf_file, txt_file):
    text_list = pdf_to_text(pdf_file)
    text_json = json.dumps(text_list)
    with open(txt_file, 'w') as f:
        f.write(text_json)

for ticker in tickers:
    annual_reports = os.listdir(f'annual_report_data/{ticker}_pdf')
    annual_reports = [report for report in annual_reports if report.endswith('.pdf')]
    json_dir = f'annual_report_data/{ticker}_json'
    os.makedirs(json_dir, exist_ok=True)
    for report in annual_reports:
        report_path = os.path.join(f'annual_report_data/{ticker}_pdf', report)
        report_txt_path = os.path.join(json_dir, f'{report[:-4]}.json')
        python_to_txt(report_path, report_txt_path)
