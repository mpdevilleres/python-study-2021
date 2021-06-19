# -*- coding: utf-8 -*-
import os
import re
import shutil
import csv

base_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = os.path.join(base_dir, 'tmp')
output_file = os.path.join(base_dir, 'output.csv')

header = ['Region/Ledger:', 'Asset Type:', 'Account:', 'Cost Centre:',
          'Asset Number - Description', 'Date Placed in Service',
          'Date Retired', 'Cost Retired', 'Net Book Value Retired',
          'Proceeds of Sale', 'Removal Cost', 'Gain/Loss', 'Trans Number']


def prep():
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)


def get_text_from_file(location=base_dir, directory='', filename=None):
    file_path = os.path.join(location, directory, filename)
    with open(file_path, mode='r') as infile:
        text = infile.read()

    return text


def save_text(text, filename):
    outfile = open(os.path.join(tmp_dir, filename), "w")
    outfile.write(text)
    outfile.close()


def process_data(text):
    header_file_data = {}
    # EXTRACTING HEADER OF THE FILE
    patterns = ['Region/Ledger:', 'Asset Type:', 'Account:', 'Cost Centre:']
    for pattern in patterns:
        regex = re.compile(r'%s%s' % (pattern, r'(.*)'))
        searched = regex.search(text)
        if searched:
            header_file_data[pattern] = searched.group(1).strip()
        else:
            header_file_data[pattern] = ''

    # EXTRACTING ROWS/DATA OF THE FILE
    rows = []
    pattern = r'(\d+ - .*)'
    regex = re.compile(pattern)
    all_searched = regex.findall(text)
    if all_searched:
        for searched in all_searched:
            rows.append(searched.strip())

    # SANITATION OF ROW DATA
    pattern = r'(.*?-.*?) (\d{2}-\w{3}-\d{4}.*)'
    regex = re.compile(pattern)
    sanitized_rows = []
    for r in rows:
        sanitized_row = {}
        searched = regex.search(r)
        sanitized_row['Asset Number - Description'] = searched.group(1).strip()

        group_2 = searched.group(2).split()
        sanitized_row['Date Placed in Service'] = group_2[0].strip()
        sanitized_row['Date Retired'] = group_2[1].strip()
        sanitized_row['Cost Retired'] = group_2[2].strip()
        sanitized_row['Net Book Value Retired'] = group_2[3].strip()
        sanitized_row['Proceeds of Sale'] = group_2[4].strip()
        sanitized_row['Removal Cost'] = group_2[5].strip()
        sanitized_row['Gain/Loss'] = group_2[6].strip()
        sanitized_row['Trans Number'] = group_2[7].strip()

        sanitized_row.update(header_file_data)
        sanitized_rows.append(sanitized_row)

    return sanitized_rows


def create_output_file():
    if os.path.isfile(output_file):
        os.remove(output_file)
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()


def append_to_output(data=None):
    with open(output_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, header)
        writer.writerows(data)


def main():
    prep()
    create_output_file()
    text = get_text_from_file(filename='sample_report.txt')

    # SPLITS TEXT IN TO INDIVIDUAL FILES
    split_word = 'XXXXX COMPANY'
    splitted_text = text.split(split_word)
    for i in range(0, len(splitted_text)):
        save_text(split_word + splitted_text[i], '{0:03d}.txt'.format(i))

    # # OPEN INDIVIDUAL FILES
    for i in os.listdir(os.path.join(base_dir, 'tmp')):
        text = get_text_from_file(directory='tmp', filename=i)
        data = process_data(text)
        if data:
            append_to_output(data)
            print(i)
        else:
            print(i)


if __name__ == '__main__':
    main()
