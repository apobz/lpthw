import csv
import os.path

def popl(f_csv, addition):
    # addition = {'usrnm': 'foo', 'pw': 'bar', 'h_score': 0}
    fields = ['usrnm', 'pw', 'h_score']
    with open(f_csv, 'a+') as f:
        reader = csv.DictReader(f)
        is_dupl = any(row['usrnm'] == addition['usrnm'] for row in reader)
        if not is_dupl:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow(addition)
        # return True if there is a dulicate, False otherwise
        return is_dupl
