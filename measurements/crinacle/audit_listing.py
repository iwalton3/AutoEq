# -*- coding: utf-8 -*-

import os
import os.path
import sys
from glob import glob
import re
import requests

def parse_books():
    """Downloads parses phone books to get names

    Returns:
        NameIndex
    """
    rows = []

    # Ears-711 measurements name index
    # res = requests.get('https://crinacle.com/graphing/data_hp/phone_book.json')
    # hp_book = parse_book(res.json())

    # IEM measurements name index
    res = requests.get('https://crinacle.com/graphing/data/phone_book.json')
    iem_book = parse_book(res.json())

    # Gras measurments name index
    res = requests.get('https://crinacle.com/graphing/data_hp_gras/phone_book.json')
    gras_book = parse_book(res.json())

    return iem_book, gras_book

def parse_book(data):
    """Parses a phone book as dict with false names as keys and true names as values.

    Args:
        data: Phone book object

    Returns:
        Dict with false names and true names
    """
    book = dict()
    for manufacturer in data:
        manufacturer_name = manufacturer['name']
        if 'suffix' in manufacturer:
            manufacturer_name += f' {manufacturer["suffix"]}'
        for model in manufacturer['phones']:
            if type(model) == str:
                # Plain string
                book[model.strip()] = f'{manufacturer_name} {model}'.strip()

            else:
                # Object
                if type(model['file']) == str:
                    # Single file as string, wrap in list
                    model['file'] = [model['file']]

                if 'suffix' in model:
                    for f, suffix in zip(model['file'], model['suffix']):
                        book[f.strip()] = f'{manufacturer_name} {model["name"]} {suffix}'.strip()
                else:
                    for f in model['file']:
                        book[f.strip()] = f'{manufacturer_name} {model["name"]}'.strip()

    return book

def audit_book(data, root, try_names):
    missing = []
    for key in data.keys():
        for try_name in try_names:
            file_name = try_name.format(key)
            if not os.path.exists(os.path.join(root,file_name)):
                missing.append(file_name)

    return missing

def write_results(name, data):
    with open(name, "w") as f:
        f.write("\n".join(data))

iem_try = [
    "{0} L.txt",
    "{0} R.txt"
]

gras_try = [
    "{0} L1.txt",
    "{0} L2.txt",
    "{0} L3.txt",
    "{0} R1.txt",
    "{0} R2.txt",
    "{0} R3.txt"
]

iem, gras = parse_books()

missing_iem = audit_book(iem, "raw_data/IEM Measurements (TSV)", iem_try)
missing_gras = audit_book(gras, "raw_data/FR Data (CSV)", gras_try)

write_results("missing_iem.txt", missing_iem)
write_results("missing_gras.txt", missing_gras)
