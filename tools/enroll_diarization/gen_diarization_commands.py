import csv
import argparse
import os
parser = argparse.ArgumentParser(description='generate runfile for enrollemnt diarization.')
parser.add_argument('--key', metavar='k', type=str,
                    help='enrollment diarization key')

args = parser.parse_args()
os.makedirs("enrollment_after_diarization/temp/")
run_file_name = "enroll_diarization.sh"
diarization_list = list(csv.DictReader(open(args.key, 'r'), delimiter='\t'))

file_name = [d['segmentid'].split('.')[0] + ".sph" for d in diarization_list]
start = [d['start'] for d in diarization_list]
end = [d['end'] for d in diarization_list]

lines = []

last_name = file_name[0]
i = 0
diar_parts_list = []
for f, s, e in zip(file_name, start, end):
    if f != last_name:
        row_parts = ''
        for p in diar_parts_list:
            row_parts += p + " "
        lines.append(f"""sox {row_parts} enrollment_after_diarization/{last_name}\n""")
        last_name = f
        i = 0
        diar_parts_list = []
    part = f"""enrollment_after_diarization/temp/{i}{f}"""
    lines.append(f"""sph2pipe enrollment/{f} -t {s}:{e} {part}\n""")
    diar_parts_list.append(part)
    i += 1

row_parts = ''
for p in diar_parts_list:
    row_parts += p + " "
lines.append(f"""sox {row_parts} enrollment_after_diarization/{last_name}\n""")
lines.append(f"""rm -r enrollment_after_diarization/temp\n""")

f = open(run_file_name, 'w')
f.writelines(lines)
f.close()
x = 1