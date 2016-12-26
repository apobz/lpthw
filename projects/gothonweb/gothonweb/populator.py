import csv
import os.path

fields = ['usrnm', 'pw', 'h_score']

def auth(f_csv, usrnm, pw):
    with open(f_csv, 'r') as f:
        reader = csv.reader(f)
        is_match = any((row[0] == usrnm and row[1] == pw) for row in reader)
        return is_match

def create_db(path):
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

def popl(f_csv, addition):
    # addition = {'usrnm': 'foo', 'pw': 'bar', 'h_score': 0}
    # fields = ['usrnm', 'pw', 'h_score']
    with open(f_csv, 'a+') as f:
        reader = csv.DictReader(f)
        is_dupl = any(row['usrnm'] == addition['usrnm'] for row in reader)
        if not is_dupl:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow(addition)
        # return True if there is a duplicate, False otherwise
        return is_dupl
