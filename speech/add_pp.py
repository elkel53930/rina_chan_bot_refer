import csv
import sys
import pp

t_file = sys.argv[1]

rep_dict = [
    ("se[tsu]sai", "[setsu]na"),
    ("ri]nachaN#bo[odo", "ri[nachaN#[bo]odo"),
]

with open(t_file, 'r') as f:
    reader = csv.reader(f)
    transcript = []
    for row in reader:
        if len(row) == 2:
            row.append("")
        _, phoneme = pp.pp(row[1])

        for old, new in rep_dict:
            phoneme = phoneme.replace(old, new)

        row[2] = phoneme
        transcript.append(row)

with open(t_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(transcript)

