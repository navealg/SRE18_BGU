import argparse
import csv
import os
import numpy as np
# from sklearn.cluster import KMeans
parser = argparse.ArgumentParser(description='Convert kaldi output scores to match the SRE format.')
parser.add_argument('--scores_dir', metavar='s', type=str,
                    help='path to kaldi score dir')
parser.add_argument('--method', metavar='m', type=str,
                    help='avg or max', default='avg')
parser.add_argument('--max_num', metavar='p', type=str,
                    help='number of max to average')
parser.add_argument('--output', metavar='o', type=str,
                    help='path to output sre score file')
parser.add_argument('-all_range', action="store_true", default=True)




args = parser.parse_args()
reference = []
scores = []
path = args.scores_dir
files = os.listdir(path)
# for path, subdirs, files in os.walk(args.scores_dir):
print("num of files: ", len(files))
for name in files:
        if name.endswith("tsv"):
            scores_file_path = os.path.join(path, name)
            temp_data = list(csv.DictReader(open(scores_file_path, 'r'), delimiter='\t'))
            if not reference:
                reference = temp_data
            for i, r in enumerate(temp_data):
                try:
                    scores[i].append(float(r['LLR']))
                except:
                    scores.append([float(r['LLR'])])
            x = 1

[s.sort(reverse=True) for s in scores]
# [s.sort() for s in scores]

if args.method == "max":
    max_num = int(args.max_num)
else:
    max_num = len(scores[0])

# max
if args.all_range:
    rng = range(1, max_num + 1)
else:
    rng = range(max_num, max_num + 1)

for j in rng:
    print("fusing max:\t", j,"\tscores")
    for i, r in enumerate(reference):
        fused_score = np.mean(scores[i][:j])
        # fused_score = np.median(scores[i][:j])
        r['LLR'] = str(fused_score)

    # write to output file
    dest = open(args.output + f"""_fused_max{str(j).zfill(4)}.tsv""", 'w')
    fieldnames = ['modelid', 'segmentid', 'side', 'LLR']
    writer = csv.DictWriter(dest, fieldnames, delimiter='\t')
    writer.writeheader()
    for line in reference:
        writer.writerow(line)
    dest.close()

# # # bins
# if args.all_range:
#     rng = range(1, max_num + 1)
# else:
#     rng = range(1, 2)
#
# for j in rng:
#     print("fusing largest bin from:\t", j,"\tscores")
#     for i, r in enumerate(reference):
#         hist, bins = np.histogram(scores[i], j)
#         edges = bins[hist.argmax():hist.argmax() + 2]
#         bins_scores = []
#         for s in scores[i]:
#             if (s >= edges[0] and s <= edges[1]):
#                 bins_scores.append(s)
#         fused_score = np.mean(bins_scores)
#         r['LLR'] = str(fused_score)
#
#     # write to output file
#     dest = open(args.output + f"""_fused_bin{str(j).zfill(4)}.tsv""", 'w')
#     fieldnames = ['modelid', 'segmentid', 'side', 'LLR']
#     writer = csv.DictWriter(dest, fieldnames, delimiter='\t')
#     writer.writeheader()
#     for line in reference:
#         writer.writerow(line)
#     dest.close()

# # # kmeans
# if args.all_range:
#     rng = range(1, max_num + 1)
# else:
#     rng = range(1, 2)
#
# for j in rng:
#     print("fusing kmeans with k =\t", j)
#     for i, r in enumerate(reference):
#         kmeans = KMeans(n_clusters=j, random_state=0).fit(np.array(scores[i]).reshape(-1, 1))
#         fused_score = kmeans.cluster_centers_[np.histogram(kmeans.labels_, j)[0].argmax()][0]
#         r['LLR'] = str(fused_score)
#
#     # write to output file
#     dest = open(args.output + f"""_fused_kmeans{str(j).zfill(4)}.tsv""", 'w')
#     fieldnames = ['modelid', 'segmentid', 'side', 'LLR']
#     writer = csv.DictWriter(dest, fieldnames, delimiter='\t')
#     writer.writeheader()
#     for line in reference:
#         writer.writerow(line)
#     dest.close()

# --scores_dir /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_bagging/v2/exp/scores/tests --method avg --max_num 3 --output /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_bagging/v2/exp/scores/tests




