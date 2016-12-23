import csv
import os.path

def pull(f_csv, a):
    reader = csv.DictReader(f_csv)
    for row in reader:
        a.append({'usrnm': row['usrnm'], 'pw': row['pw'], 'h_score': row['h_score']})
        # print row['usrnm'], row['pw'], row['h_score']


def popl(f_csv, addition):
    # addition = {'usrnm': 'foo', 'pw': 'bar', 'h_score': 0}
    fields = ['usrnm', 'pw', 'h_score']

    # create and setup the csv file if it doesn't exist
    if not os.path.isfile(f_csv):
        with open(f_csv, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerow(addition)
        f.close()
    # append to it
    else:
        with open(f_csv, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow(addition)
        f.close()
