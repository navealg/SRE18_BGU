import argparse
import csv
import os
import numpy as np
import re
parser = argparse.ArgumentParser(description='Convert kaldi output scores to match the SRE format.')
parser.add_argument('--rttn', metavar='t', type=str,
                    help='rttn file')
parser.add_argument('--org-data-dir', metavar='m', type=str,
                    help='avg or max', default='avg')
parser.add_argument('--target-data-dir', metavar='p', type=str,
                    help='number of max to average')

args = parser.parse_args()

rttn = open(args.rttn).readlines()
file = [r.split(' ')[1] for r in rttn]
time = [re.findall("\d+\.\d+", r) for r in rttn]
id = [int(re.findall("\d+", r)[-1]) for r in rttn]

start = [t[0] for t in time]
end = [str(float(t[0]) + float(t[1])) for t in time]
file = [f + '.sph' for f in file]



max_id = max(id)


complete_dict = dict()
for i in range(len(file)):
    if file[i] not in complete_dict.keys():
        complete_dict[file[i]] = dict()
        complete_dict[file[i]]['time'] = []
        complete_dict[file[i]]['id'] = []
    complete_dict[file[i]]['time'].append(float(time[i][-1]))
    complete_dict[file[i]]['id'].append(id[i])

for k in complete_dict.keys():
    complete_dict[k]['max_id'] = max(complete_dict[k]['id'])
    l = [np.sum(np.where(np.equal(complete_dict[k]['id'], j), complete_dict[k]['time'][:][-1], 0)) for j in range(1, complete_dict[k]['max_id'] + 1)]
    complete_dict[k]['argmax_id'] = np.argmax(l) + 1



run_file_name = f"""test_diarization_argmax.sh"""
lines = []
lines.append(f"""mkdir -p test/temp/\n""")

last_name = file[0]
i = 0
diar_parts_list = []
for f, s, e, idx in zip(file, start, end, id):
    if idx == complete_dict[f]['argmax_id']:
        if f != last_name:
            row_parts = ''
            for p in diar_parts_list:
                row_parts += p + " "
            lines.append(f"""sox {row_parts} test/{last_name}\n""")
            last_name = f
            i = 0
            diar_parts_list = []
        part = f"""test/temp/{i}{f}"""
        lines.append(f"""sph2pipe test_org/{f} -t {s}:{e} {part}\n""")
        diar_parts_list.append(part)
        i += 1

row_parts = ''
for p in diar_parts_list:
    row_parts += p + " "
lines.append(f"""sox {row_parts} test/{last_name}\n""")
lines.append(f"""rm -r test/temp\n""")

f = open(run_file_name, 'w')
f.writelines(lines)
f.close()



#
# for curr_id in range(1, max_id + 1):
#     run_file_name = f"""test_diarization_{curr_id}.sh"""
#     lines = []
#     lines.append(f"""mkdir -p test/temp/\n""")
#
#     last_name = file[0]
#     i = 0
#     diar_parts_list = []
#     for f, s, e, idx in zip(file, start, end, id):
#         if ((idx == 1 and curr_id > complete_dict[f]['max_id']) or idx == curr_id):
#             if f != last_name:
#                 row_parts = ''
#                 for p in diar_parts_list:
#                     row_parts += p + " "
#                 lines.append(f"""sox {row_parts} test/{last_name}\n""")
#                 last_name = f
#                 i = 0
#                 diar_parts_list = []
#             part = f"""test/temp/{i}{f}"""
#             lines.append(f"""sph2pipe test_org/{f} -t {s}:{e} {part}\n""")
#             diar_parts_list.append(part)
#             i += 1
#
#     row_parts = ''
#     for p in diar_parts_list:
#         row_parts += p + " "
#     lines.append(f"""sox {row_parts} test/{last_name}\n""")
#     lines.append(f"""rm -r test/temp\n""")
#
#     f = open(run_file_name, 'w')
#     f.writelines(lines)
#     f.close()


x = 1
